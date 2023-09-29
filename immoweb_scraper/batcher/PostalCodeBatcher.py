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
        self._postal_codes_gen = None  # Initialize the generator as None
        self.batch_size = batch_size
        self.current_code_index = initial_index

    @property
    def postal_codes_gen(self):
        if self._postal_codes_gen is None:
            self._postal_codes_gen = self._create_postal_codes_gen()
        return self._postal_codes_gen

    @postal_codes_gen.setter
    def postal_codes_gen(self, value):
        self._postal_codes_gen = value

    def _create_postal_codes_gen(self):
        return chain.from_iterable(
            map(
                lambda d: d.values(),
                self.dictionaries,
            )
        )

    def batch_generator(self) -> tuple[int, list[int]]:
        index = self.current_code_index

        while True:
            end_index = index + self.batch_size

            # Handle wrap-around case
            if end_index > self.total_postal_codes:
                remaining = list(
                    islice(self.postal_codes_gen, index, self.total_postal_codes + 1)
                )
                # Reset the generator before calling from start
                self.postal_codes_gen = self._create_postal_codes_gen()
                index = end_index - self.total_postal_codes
                from_start = list(islice(self.postal_codes_gen, 0, index))
                batch = remaining + from_start
            else:
                # Normal case: No wrap-around
                batch = list(islice(self.postal_codes_gen, index, end_index))
                index += 1

            self.current_code_index = index
            yield batch

    def get_current_index(self):
        return self.current_code_index

    def get_next_batch(self) -> list[str]:
        return list(map(str, next(self.batch_generator())))
