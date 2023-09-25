import pytest

from immoweb_scraper.batcher.BatchStateHandler import BatchStateHandler
from immoweb_scraper.batcher.PostalCodeBatcher import PostalCodeBatcher

brussels_postal_codes = {
    "BRUXELLES": 1000,
    "SCHAERBEEK": 1030,
    "ETTERBEEK": 1040,
}

halle_vilvoorde_postal_codes = {
    "AFFLIGEM": 1790,
    "ALSEMBERG": 1652,
    "ASSE": 1730,
}

flemish_brabant_leuven = {
    "AARSCHOT": 3200,
    "ASSENT": 3460,
    "BETEKOM": 3130,
}
batcher_test_dict = [
    brussels_postal_codes,
    halle_vilvoorde_postal_codes,
    flemish_brabant_leuven,
]

batch_size = 2


@pytest.fixture
def mock_db_connection(mocker):
    # Create a mock DBConnection instance
    mock_conn = mocker.MagicMock()

    # Mock the session_scope method to yield a mock session
    mock_session = mocker.MagicMock()
    mock_session.query.return_value.first.return_value = (
        None  # Simulate no existing state in the database
    )
    mock_conn.session_scope.return_value.__enter__.return_value = mock_session

    return mock_conn


@pytest.fixture
def batcher(mock_db_connection) -> PostalCodeBatcher:
    state_handler = BatchStateHandler(mock_db_connection)
    return PostalCodeBatcher(
        state_handler, batch_size=2, dictionaries=batcher_test_dict
    )


def test_get_next_batch(batcher: PostalCodeBatcher):
    # Expected results
    expected_batches = [
        ["1000", "1030"],
        ["1040", "1790"],
        ["1652", "1730"],
        ["3200", "3460"],
        ["3130", "1000"],
    ]

    # Call get_next_batch and verify the output
    for i, expected_batch in enumerate(expected_batches):
        if i > len(expected_batches):
            break
        batches = batcher.get_next_batch()
        assert batches == expected_batch
