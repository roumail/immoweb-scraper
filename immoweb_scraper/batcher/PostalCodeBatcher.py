import typing as tp
from itertools import chain

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
            self.dictionaries = dictionaries
        else:
            self.dictionaries = dictionaries
        # Compute the length of all_postal_codes
        self.total_postal_codes = sum(len(d) for d in self.dictionaries)
        self.postal_codes_gen = None  # Initialize the generator as None
        self.batch_size = batch_size
        self.current_code_index = self.state_handler.load_state()

    def get_all_postal_codes(self):
        if self.postal_codes_gen is None:
            self.postal_codes_gen = self._create_postal_codes_gen()
        return self.postal_codes_gen

    def _create_postal_codes_gen(self):
        return chain.from_iterable(
            map(
                lambda d: d.values(),
                self.dictionaries,
            )
        )

    def postal_code_iterator(self, start_index):
        current_index = start_index
        while True:
            try:
                code = next(self.get_all_postal_codes())
                yield code
                current_index += 1
                if current_index >= self.total_postal_codes:
                    current_index = 0
            except StopIteration:
                self.postal_codes_gen = None  # Reset the generator

    def postal_code_batches(self):
        code_iter = self.postal_code_iterator(self.current_code_index)
        current_batch = []
        batches_yielded = 0

        for code in code_iter:
            current_batch.append(code)

            if len(current_batch) == self.batch_size:
                # Increment the current_code_index by batch size
                self.current_code_index += self.batch_size

                # Wrap the index if it exceeds total postal codes
                wrapped_index = self.current_code_index % self.total_postal_codes
                self.state_handler.save_state(wrapped_index)

                yield current_batch
                current_batch = []
                batches_yielded += 1

                # Termination condition: If we've yielded all batches, break the loop
                if batches_yielded * self.batch_size >= self.total_postal_codes:
                    break

    def get_next_batch(self) -> list[str]:
        return list(map(str, next(self.postal_code_batches())))
