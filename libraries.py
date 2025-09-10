import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Extracts a filename from the URL or generates a default one."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:  # fallback if no filename in path
        filename = "downloaded_image.jpg"
    return filename

def file_already_exists(filepath, content):
    """Check if the file already exists by comparing hash of content."""
    if not os.path.exists(filepath):
        return False
    with open(filepath, "rb") as f:
        existing_content = f.read()
    return hashlib.md5(existing_content).hexdigest() == hashlib.md5(content).hexdigest()

def fetch_image(url):
    """Fetch and save image from a URL with error handling."""
    try:
        # Fetch the image
        response = requests.get(url, timeout=10, headers={"User-Agent": "UbuntuFetcher/1.0"})
        response.raise_for_status()

        # Check content type header to ensure it's an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped: {url} (not an image, got {content_type})")
            return

        # Create directory if not exists
        os.makedirs("Fetched_Images", exist_ok=True)

        # Extract filename and set path
        filename = get_filename_from_url(url)
        filepath = os.path.join("Fetched_Images", filename)

        # Prevent duplicates
        if file_already_exists(filepath, response.content):
            print(f"✓ Duplicate skipped: {filename}")
            return

        # Save the image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Nature Image Fetcher")
    print("A tool for mindfully collecting Nature images from the web\n")

    # Ask for one or multiple URLs
    urls = input("Please enter one or more Nature image URLs (separated by spaces): ").split()

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Nature-enriched Community.")

if __name__ == "__main__":
    main()
