import typing as tp

from immoweb_scraper.db.models import BatchState

if tp.TYPE_CHECKING:
    from immoweb_scraper.db.DBConnection import DBConnection


class BatchStateHandler:
    def __init__(self, db_conn: "DBConnection"):
        self.db_conn = db_conn

    def load_state(self):
        with self.db_conn.session_scope() as session:
            state = session.query(BatchState).first()
        return state.code_index if state else 0

    def save_state(self, code_index):
        with self.db_conn.session_scope() as session:
            state = session.query(BatchState).first()
            if state:
                state.code_index = code_index
            else:
                new_state = BatchState(code_index=code_index)
                session.add(new_state)
