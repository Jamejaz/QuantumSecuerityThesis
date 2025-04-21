from bs4 import BeautifulSoup
import requests
import csv
import time
import random

URL = "https://quantumcomputing.stackexchange.com/questions"
START_PAGE = 751  # Start scraping from page 451
PAGE_LIMIT = 800  # Scrape up to page 500

# Rotating user-agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://quantumcomputing.stackexchange.com",
    }

def build_url(base_url=URL, page=1):
    return f"{base_url}?tab=newest&page={page}"

def get_question_text_and_date(question_url):
    retry_count = 0
    max_retries = 5
    backoff_factor = 2
    
    while retry_count < max_retries:
        try:
            response = requests.get(question_url, headers=get_headers())
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 10))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retry_count += 1
                continue
            if response.status_code != 200:
                print(f"Failed to retrieve question text from {question_url}: Status code {response.status_code}")
                return "", ""

            soup = BeautifulSoup(response.text, "html.parser")
            question_body = soup.find("div", class_="question js-question")
            if not question_body:
                return "", ""

            # Extract text including links
            parts = []
            for element in question_body.descendants:
                if element.name == "a" and element.get("href"):
                    link_text = element.get_text(strip=True)
                    link_url = element["href"]
                    parts.append(f"{link_text} ({link_url})")
                elif element.name in ["p", "li", "pre", "code"]:
                    parts.append(element.get_text(strip=True))
                elif element.name == "br":
                    parts.append("\n")

            question_text = "\n".join(filter(None, parts))

            # Extract question date
            date_element = soup.find("div", class_="flex--item ws-nowrap mr16 mb8")
            date = ""
            if date_element:
                time_element = date_element.find("time")
                if time_element and time_element.has_attr("datetime"):
                    date = time_element["datetime"]

            return question_text, date

        except Exception as e:
            print(f"Error retrieving question text from {question_url}: {e}")
            retry_count += 1
            time.sleep(backoff_factor ** retry_count)

    print(f"Max retries reached for {question_url}. Skipping.")
    return "", ""

def scrape_page(page=1):
    """Scrapes a specific page for question summaries."""
    try:
        response = requests.get(build_url(page=page), headers=get_headers())
        if response.status_code == 429:  # Rate limiting
            retry_after = int(response.headers.get("Retry-After", 10))  # Default to 10 seconds
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            return scrape_page(page)  # Retry the same page

        print(f"HTTP Status Code for page {page}: {response.status_code}")
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}: Status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        question_summaries = soup.find_all("div", class_="s-post-summary")
        if not question_summaries:
            print(f"No questions found on page {page}. Check if the class names have changed.")
            return []

        page_questions = []
        for summary in question_summaries:
            question_element = summary.find("a", class_="s-link")
            vote_count_element = summary.find("span", class_="s-post-summary--stats-item-number")
    
            # Extract answer count
            answer_count_element = summary.find("div", class_="s-post-summary--stats-item", title=lambda x: "answers" in x if x else False)
            answers_count = answer_count_element.find("span", class_="s-post-summary--stats-item-number").text.strip() if answer_count_element else "0"

            # Extract view count
            view_count_element = summary.find("div", class_="s-post-summary--stats-item", title=lambda x: "views" in x if x else False)
            view_count = view_count_element.find("span", class_="s-post-summary--stats-item-number").text.strip() if view_count_element else "0"

            if question_element:
                question_title = question_element.text.strip()
                question_url = "https://quantumcomputing.stackexchange.com" + question_element['href']
                
                # Fetch question text and date
                question_text, question_date = get_question_text_and_date(question_url)
                
                vote_count = vote_count_element.text.strip() if vote_count_element else "0"

                page_questions.append({
                    "question_title": question_title,
                    "question_text": question_text,
                    "date": question_date,  # New date field
                    "answers": answers_count,
                    "views": view_count,
                    "votes": vote_count,
                    "url": question_url
                })
        return page_questions

    except Exception as e:
        print(f"Error scraping page {page}: {e}")
        return []

def scrape():
    questions = []
    for i in range(START_PAGE, PAGE_LIMIT + 1):
        print(f"Scraping page {i}")
        page_questions = scrape_page(i)
        questions.extend(page_questions)
        time.sleep(random.uniform(10, 20))  # Increased random delay
        if not page_questions:
            break
    return questions

def export_data():
    data = scrape()
    if not data:
        print("No data scraped.")
        return

    with open("Quantum_computing_stackexchange_26.csv", "w", newline='', encoding='utf-8') as data_file:
        fieldnames = ["question_title", "question_text", "date", "answers", "views", "votes", "url"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
        print("Data saved successfully.")

if __name__ == "__main__":
    export_data()
