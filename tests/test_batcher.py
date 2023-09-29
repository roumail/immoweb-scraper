import pytest

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


@pytest.mark.parametrize(
    "batch_size,expected_batches",
    [
        (
            2,
            [
                ["1000", "1030"],
                ["1040", "1790"],
                ["1652", "1730"],
                ["3200", "3460"],
                ["3130", "1000"],
            ],
        ),
        (
            5,
            [
                ["1000", "1030", "1040", "1790", "1652"],
                ["1730", "3200", "3460", "3130", "1000"],
                ["1030", "1040", "1790", "1652", "1730"],
                ["3200", "3460", "3130", "1000", "1030"],
                ["1040", "1790", "1652", "1730", "3200"],
            ],
        ),
    ],
)
def test_get_next_batch(batch_size, expected_batches):
    batcher = PostalCodeBatcher(
        initial_index=0, batch_size=batch_size, dictionaries=batcher_test_dict
    )
    # Call get_next_batch and verify the output
    for i, expected_batch in enumerate(expected_batches):
        if i > len(expected_batches):
            break
        batches = batcher.get_next_batch()
        assert batches == expected_batch
