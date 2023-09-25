import typing as tp
from itertools import chain, cycle, islice

if tp.TYPE_CHECKING:
    from immoweb_scraper.batcher.BatchStateHandler import BatchStateHandler


class PostalCodeBatcher:
    def __init__(
        self,
        state_handler: "BatchStateHandler",
        batch_size: tp.Optional[int] = 10,
        dictionaries: tp.Optional[list[dict[str, int]]] = None,
    ):
        self.state_handler = state_handler
        if dictionaries is None:
            from immoweb_scraper.batcher.constants import (
                brussels_postal_codes,
                flemish_brabant_leuven,
                halle_vilvoorde_postal_codes,
            )

            dictionaries = [
                brussels_postal_codes,
                halle_vilvoorde_postal_codes,
                flemish_brabant_leuven,
            ]
        # Compute the length of all_postal_codes
        self.total_postal_codes = sum(len(d) for d in dictionaries)
        self.all_postal_codes = chain.from_iterable(
            map(
                lambda d: d.values(),
                dictionaries,
            )
        )
        self.batch_size = batch_size
        self.current_code_index = self.state_handler.load_state()

    def postal_code_batches(self):
        infinite_postal_codes = cycle(self.all_postal_codes)

        # Start iterating from the last saved position
        sliced_postal_codes = islice(
            infinite_postal_codes, self.current_code_index, None
        )

        current_batch = []
        for code in sliced_postal_codes:
            current_batch.append(code)
            if len(current_batch) == self.batch_size:
                self.state_handler.save_state(
                    self.current_code_index + self.batch_size,
                    total_postal_codes=self.total_postal_codes,
                )
                yield current_batch
                current_batch = []

        # If there are any remaining postal codes in the last batch
        if current_batch:
            self.state_handler.save_state(
                self.current_code_index + len(current_batch),
                total_postal_codes=self.total_postal_codes,
            )
            yield current_batch

    def get_next_batch(self) -> list[str]:
        return list(map(str, next(self.postal_code_batches())))
