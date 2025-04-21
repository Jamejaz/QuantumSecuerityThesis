import requests
import csv
import time
import random
from bs4 import BeautifulSoup

# Stack Overflow search URL
URL = "https://math.stackexchange.com/search?q=Quantum+Information"
PAGE_LIMIT = 30  # Adjust as needed

# Rotating user-agents to avoid bot detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

def get_headers():
    """Return random user-agent headers to avoid bot detection."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://math.stackexchange.com",
    }

def build_url(base_url=URL, page=1):
    """Build paginated URL."""
    return f"{base_url}&page={page}"

def get_question_details(question_url):
    """Extract full question text and post time from the question page."""
    try:
        response = requests.get(question_url, headers=get_headers())

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))  # Default to 10 seconds
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            return get_question_details(question_url)  # Retry

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract full question text
        question_body = soup.find("div", class_="s-prose js-post-body", itemprop="text")
        question_text = question_body.get_text(separator="\n", strip=True) if question_body else "No details provided."

        # Extract post time
        post_time = "Unknown"
        time_div = soup.find("div", class_="flex--item ws-nowrap mr16 mb8")
        if time_div and "title" in time_div.attrs:
            post_time = time_div["title"]

        return question_text, post_time

    except Exception as e:
        print(f"Error retrieving question details from {question_url}: {e}")
        return "No details provided.", "Unknown"

def scrape_page(page=1):
    """Scrape a single page of Stack Overflow results."""
    try:
        response = requests.get(build_url(page=page), headers=get_headers())

        # Handle rate limiting (HTTP 429)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))  # Default to 10 seconds
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            return scrape_page(page)  # Retry

        print(f"HTTP Status Code for page {page}: {response.status_code}")
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}: Status code {response.status_code}")
            return []

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        question_summary = soup.find_all("div", class_="s-post-summary")

        if not question_summary:
            print(f"No questions found on page {page}. Check if the class names have changed.")
            return []

        page_questions = []
        for summary in question_summary:
            question_element = summary.find("a", class_="s-link")
            vote_element = summary.find("div", class_="s-post-summary--stats-item s-post-summary--stats-item__emphasized")
            answer_element = summary.find("div", class_="s-post-summary--stats-item has-answers")
            view_element = summary.find("div", class_="s-post-summary--stats-item", title=lambda x: x and "views" in x)

            if question_element:
                question_title = question_element.text.strip()
                question_url = "https://math.stackexchange.com" + question_element['href']
                vote_count = vote_element.find("span", class_="s-post-summary--stats-item-number").text.strip() if vote_element else "0"
                answers_count = answer_element.find("span", class_="s-post-summary--stats-item-number").text.strip() if answer_element else "0"
                view_count = view_element.find("span", class_="s-post-summary--stats-item-number").text.strip() if view_element else "0"

                # Fetch full question text and post time from the question page
                question_text, post_time = get_question_details(question_url)

                # Store data
                page_questions.append({
                    "question_title": question_title,
                    "question_text": question_text,
                    "answers": answers_count,
                    "views": view_count,
                    "votes": vote_count,
                    "time": post_time,
                    "url": question_url
                })
        return page_questions

    except Exception as e:
        print(f"Error scraping page {page}: {e}")
        return []

def scrape():
    """Scrape multiple pages and return a list of questions."""
    questions = []
    for i in range(1, PAGE_LIMIT + 1):
        print(f"Scraping page {i}...")
        page_questions = scrape_page(i)
        questions.extend(page_questions)
        time.sleep(random.uniform(5, 10))  # Random delay to prevent bot detection

        if not page_questions:  # Stop if no more questions found
            break
    return questions

def export_data():
    """Scrape data and save it to a CSV file."""
    data = scrape()
    if not data:
        print("No data scraped.")
        return

    # Save to CSV
    with open("Quantum_math_stackexchange_information.csv", "w", newline='', encoding='utf-8') as data_file:
        fieldnames = ["question_title", "question_text", "answers", "views", "votes", "time", "url"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)

    print("Data saved successfully.")

if __name__ == "__main__":
    export_data()




