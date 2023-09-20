import typing as tp
from itertools import chain, cycle, islice

from immoweb_scraper.batcher.constants import (
    brussels_postal_codes,
    flemish_brabant_leuven,
    halle_vilvoorde_postal_codes,
)
from immoweb_scraper.db.models import BatchState

if tp.TYPE_CHECKING:
    from immoweb_scraper.db.DBConnection import DBConnection


class PostalCodeBatcher:
    def __init__(self, db_conn: "DBConnection", batch_size: int = 10):
        self.db_conn = db_conn
        # Compute the length of all_postal_codes
        self.total_postal_codes = sum(len(d) for d in self.dictionaries)
        self.all_postal_codes = chain.from_iterable(
            map(
                lambda d: d.values(),
                [
                    brussels_postal_codes,
                    halle_vilvoorde_postal_codes,
                    flemish_brabant_leuven,
                ],
            )
        )
        self.batch_size = batch_size
        self.current_code_index = self._load_state()
        self.current_index = 0

    def _load_state(self):
        with self.db_conn.session_scope() as session:
            state = session.query(BatchState).first()
        if state:
            return state.code_index
        else:
            return 0

    def _save_state(self, code_index):
        with self.db_conn.session_scope() as session:
            state = session.query(BatchState).first()
            if state:
                state.code_index = (
                    code_index % self.total_postal_codes
                )  # Wrap around if exceeds total postal codes
            else:
                new_state = BatchState(code_index=code_index)
                session.add(new_state)

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
                self._save_state(self.current_code_index + self.batch_size)
                yield current_batch
                current_batch = []

        # If there are any remaining postal codes in the last batch
        if current_batch:
            self._save_state(self.current_code_index + len(current_batch))
            yield current_batch

    def get_next_batch(self) -> list[str]:
        return list(map(str, next(self.postal_code_batches())))
