import zipfile

import requests
import typer

app = typer.Typer()


@app.command()
def download_chromedriver(
    version: str = typer.Argument(..., help="Version of ChromeDriver to download."),
    download_dir: str = typer.Option(
        "/usr/bin", help="Directory to download and extract ChromeDriver to."
    ),
):
    # Fetch the JSON data from the provided URL
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    response = requests.get(url)
    data = response.json()

    # Determine the platform (assuming Linux x64 for Docker container)
    platform = "linux64"

    # Get the download URL for the ChromeDriver corresponding to the platform and version
    stable_channel = data["channels"]["Stable"]

    if stable_channel["version"] != version:
        raise ValueError(f"Version {version} not found in the stable channel.")

    chromedriver_url = next(
        entry["url"]
        for entry in stable_channel["downloads"]["chromedriver"]
        if entry["platform"] == platform
    )
    # Download the ChromeDriver zip file
    response = requests.get(chromedriver_url, stream=True)
    zip_filename = "chromedriver.zip"
    with open(zip_filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # Extract the zip file to get the `chromedriver` binary
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(download_dir)

    print(
        f"ChromeDriver for {platform} (version: {version}) downloaded and extracted successfully!"
    )


if __name__ == "__main__":
    app()
