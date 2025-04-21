import requests
import csv
import time
import random
from bs4 import BeautifulSoup

# Security Stack Exchange search URL
BASE_URL = "https://security.stackexchange.com/search?q=quantum+encryption"
PAGE_LIMIT = 13  # Ensure we attempt all available pages

# Rotating user-agents for bot prevention
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

def get_headers():
    """Return randomized headers to avoid bot detection."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://security.stackexchange.com",
    }

def build_url(page):
    """Constructs the correct paginated URL."""
    return f"{BASE_URL}&page={page}"

def get_question_details(question_url):
    """Extracts full question text, post date, and views from the question page."""
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(question_url, headers=get_headers())

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 10))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retries += 1
                continue  # Retry the request

            if response.status_code != 200:
                print(f"Error {response.status_code} on {question_url}, skipping...")
                return "Unknown", "No details provided.", "Unknown", "0"

            soup = BeautifulSoup(response.text, "html.parser")

            # ✅ Extract the question title
            question_title = "Unknown"
            title_element = soup.find("h1", itemprop="name")
            if title_element:
                question_title = title_element.get_text(strip=True)

            # ✅ Extract the full question text
            question_text = "No details provided."
            question_body = soup.find("div", class_="s-prose js-post-body", itemprop="text")
            if question_body:
                question_text = question_body.get_text(separator="\n", strip=True)

            # ✅ Extract the question date
            post_time = "Unknown"
            time_div = soup.find("div", class_="flex--item ws-nowrap mr16 mb8")
            if time_div and "title" in time_div.attrs:
                post_time = time_div["title"]
            else:
                time_element = time_div.find("time", itemprop="dateCreated") if time_div else None
                if time_element and "datetime" in time_element.attrs:
                    post_time = time_element["datetime"]

            # ✅ Extract views count
            view_count = "0"
            view_div = soup.find("div", class_="flex--item ws-nowrap mb8", title=lambda x: "Viewed" in x if x else False)
            if view_div:
                view_count = view_div.get_text(strip=True).replace("Viewed", "").replace("times", "").strip()

            return question_title, question_text, post_time, view_count

        except Exception as e:
            print(f"Error retrieving question details from {question_url}: {e}")
            retries += 1
            time.sleep(5)  # Wait before retrying

    return "Unknown", "No details provided.", "Unknown", "0"

def scrape_page(page):
    """Scrapes a single page of Security Stack Exchange results."""
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(build_url(page), headers=get_headers())

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 10))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retries += 1
                continue  # Retry the request

            print(f"Scraping page {page} - Status Code: {response.status_code}")
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}, skipping...")
                return []

            soup = BeautifulSoup(response.text, "html.parser")
            question_summaries = soup.find_all("div", class_="s-post-summary")

            if not question_summaries:
                print(f"No questions found on page {page}. Continuing...")
                return []

            questions = []
            for summary in question_summaries:
                question_element = summary.find("a", class_="s-link")

                # ✅ Extract the vote count
                vote_count = "0"
                vote_element = summary.find("div", class_="s-post-summary--stats-item s-post-summary--stats-item__emphasized")
                if vote_element:
                    vote_count_span = vote_element.find("span", class_="s-post-summary--stats-item-number")
                    if vote_count_span:
                        vote_count = vote_count_span.get_text(strip=True)

                # ✅ Extract the answer count
                answer_count = "0"
                answer_element = summary.find("span", title="Answer")
                if answer_element:
                    answer_count = answer_element.get_text(strip=True)

                if question_element:
                    question_url = "https://security.stackexchange.com" + question_element["href"]
                    question_title, question_text, post_time, view_count = get_question_details(question_url)

                    questions.append({
                        "question_title": question_title,
                        "question_text": question_text,
                        "date": post_time,
                        "answers": answer_count,
                        "views": view_count,
                        "votes": vote_count,
                        "url": question_url,
                    })

            return questions

        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            retries += 1
            time.sleep(5)

    return []

def scrape():
    """Scrapes multiple pages and collects questions."""
    all_questions = []

    for page in range(1, PAGE_LIMIT + 1):
        print(f"Scraping page {page}...")
        questions = scrape_page(page)
        all_questions.extend(questions)
        time.sleep(random.uniform(5, 10))  # Random delay to prevent detection

    return all_questions

def export_data():
    """Exports the scraped data to a CSV file."""
    data = scrape()
    if not data:
        print("No data scraped.")
        return

    with open("Quantum_security_stackexchange_encryption_1.csv", "w", newline='', encoding='utf-8') as file:
        fieldnames = ["question_title", "question_text", "date", "answers", "views", "votes", "url"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for question in data:
            writer.writerow(question)

    print("Data successfully saved to Quantum_security_stackexchange.csv")

if __name__ == "__main__":
    export_data()



