import typing as tp
from itertools import chain, islice


class PostalCodeBatcher:
    def __init__(
        self,
        initial_index: int,
        batch_size: tp.Optional[int] = 10,
        dictionaries: tp.Optional[list[dict[str, int]]] = None,
    ):
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
            self.dictionaries = dictionaries
        else:
            self.dictionaries = dictionaries
        # Compute the length of all_postal_codes
        self.total_postal_codes = sum(len(d) for d in self.dictionaries)
        self.batch_size = batch_size
        self.current_code_index = initial_index

    def _create_postal_codes_gen(self):
        return chain.from_iterable(
            map(
                lambda d: d.values(),
                self.dictionaries,
            )
        )

    def postal_code_batches_generator(self) -> list[int]:
        while True:
            end_index = self.current_code_index + self.batch_size
            # Create a new generator starting from the current index
            new_gen = islice(
                self._create_postal_codes_gen(), self.current_code_index, end_index
            )
            batch = list(new_gen)
            if end_index > self.total_postal_codes:
                remaining_count = self.total_postal_codes - self.current_code_index
                wrap_around_count = self.batch_size - remaining_count
                wrap_around_gen = islice(
                    self._create_postal_codes_gen(), wrap_around_count
                )
                batch += list(wrap_around_gen)
                self.current_code_index = wrap_around_count

            else:
                self.current_code_index = end_index
            yield batch

    def get_current_index(self):
        return self.current_code_index

    def get_next_batch(self) -> list[str]:
        return list(map(str, next(self.postal_code_batches_generator())))
