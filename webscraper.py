import requests
from bs4 import BeautifulSoup
import socket

def web_scraper():
    print("---- Welcome to the Simplified Web Scraper ----")

    while True:
        # Get URL input from the user
        url = input("\nEnter the URL of the website to scrape (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Step 1: Get the IP address of the website
        try:
            domain_name = url.split("//")[-1].split("/")[0]  # Extract domain name from the URL
            ip_address = socket.gethostbyname(domain_name)
            print(f"Website's IP Address: {ip_address}")
        except Exception as e:
            print(f"Error getting IP address: {e}")
            continue

        # Step 2: Make a request to the website
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
            print("Successfully accessed the website!")
        except requests.exceptions.ConnectionError:
            print("Failed to connect to the website. Please check the URL or your internet connection.")
            continue
        except requests.exceptions.Timeout:
            print("Request timed out. The website may be too slow or unreachable.")
            continue
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

        # Step 3: Parse the HTML content using BeautifulSoup
        try:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract webpage title
            title = soup.title.string if soup.title else "No title available"
            print(f"Webpage Title: {title}")

            # Extract meta description
            meta_description = soup.find("meta", attrs={"name": "description"})
            description_content = meta_description["content"] if meta_description else "No meta description available"
            print(f"Meta Description: {description_content}")

            # Count occurrences of basic tags
            h1_count = len(soup.find_all('h1'))
            h2_count = len(soup.find_all('h2'))
            p_count = len(soup.find_all('p'))
            print(f"Number of <h1> tags: {h1_count}")
            print(f"Number of <h2> tags: {h2_count}")
            print(f"Number of <p> tags: {p_count}")

            # Scrape specific tags (<h2>)
            headlines = soup.find_all('h2')
            if headlines:
                print("\nScraped Headlines:")
                for idx, headline in enumerate(headlines, start=1):
                    print(f"{idx}. {headline.text.strip()}")
            else:
                print("No <h2> tags found on this website.")
        except Exception as e:
            print(f"Error parsing the website content: {e}")

# Run the scraper
if __name__ == "__main__":
    web_scraper()
