import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_page(url):
    """Fetch HTML content of a webpage."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text(html):
    """Extract the main text content from a webpage."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text(separator=" ", strip=True)
    return text[:5000]  # Limit text length for LLM processing

if __name__ == "__main__":
    url = input("Enter a website URL: ")
    html_content = fetch_page(url)
    
    if html_content:
        extracted_text = extract_text(html_content)
        print("Extracted Text:", extracted_text)
