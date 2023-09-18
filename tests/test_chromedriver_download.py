import os
import tempfile

from immoweb_scraper.download_chromedriver import download_chromedriver


def test_download_chromedriver():
    version = "117.0.5938.88"

    with tempfile.TemporaryDirectory() as tmpdirname:
        platform = download_chromedriver(version, download_dir=tmpdirname)

        # Check if chromedriver binary exists in the temporary directory
        assert os.path.exists(
            os.path.join(tmpdirname, f"chromedriver-{platform}", "chromedriver")
        )
