import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def extract_info(post_element):
    """
    Extracts votes, comments and time of post from its html and returns a tuple.
    If any information is not available, it returns 'N/A'.
    """
    vote_count = 'N/A'
    comments_count = 'N/A'
    post_time = 'N/A'

    # votes and comments
    counter_row = post_element.find_next('div', {'data-testid': 'search-counter-row'})
    if counter_row:
        numbers = counter_row.find_all('faceplate-number')
        if len(numbers) >= 2:
            vote_count = numbers[0].get_text().strip()
            comments_count = numbers[1].get_text().strip()

    # post time
    time_element = post_element.find_next('faceplate-timeago')
    if time_element:
        post_time_full = time_element.find('time')['title']
        post_time = ' '.join(post_time_full.split()[:3])  # extract only day, month, year

    return vote_count, comments_count, post_time


def scrape_reddit(subreddit, query, num_scrolls=10):
    url = f"https://www.reddit.com/r/{subreddit}/search/?q={query}"
    posts = []
    seen_posts = set()

    # start selenium driver
    driver = webdriver.Edge()  # poti sa pui Chrome sau Safari aici

    try:
        driver.get(url)
        time.sleep(3)

        for scroll_number in range(num_scrolls):
            print(f"Scroll {scroll_number + 1} of {num_scrolls}")

            # get the count of posts before scrolling
            current_post_count = len(driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="post-title-text"]'))

            # scroll
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)

            # wait for new posts to load by checking if the post count has grown
            new_post_count = current_post_count
            retries = 0
            while new_post_count == current_post_count and retries < 5:
                time.sleep(1)
                new_post_count = len(driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="post-title-text"]'))
                retries += 1

            if new_post_count == current_post_count:
                print("No new posts loaded, stopping scroll.")
                break

            # parse html with beautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            post_elements = soup.find_all('a', {'data-testid': 'post-title-text'})
            print("Number of posts found:", len(post_elements))  # logs number of posts found

            new_posts = 0  # counter for new UNIQUE posts

            for post_element in post_elements:
                post_id = post_element['id']
                if post_id in seen_posts:
                    continue  # skip already seen posts

                seen_posts.add(post_id)
                new_posts += 1

                title = post_element.get_text().strip()

                # extract votes, comments, time
                votes, comments, post_time = extract_info(post_element)

                # adding data to posts list
                posts.append({
                    'subreddit': subreddit,
                    'title': title,
                    'votes': votes,
                    'comments': comments,
                    'post_time': post_time
                })

            print(f"New posts found in this scroll: {new_posts}")

            if new_posts == 0:
                print("No new unique posts found, stopping scroll.")
                break

    finally:
        driver.quit()

    return posts


def save_to_csv(posts, filename):
    df = pd.DataFrame(posts)
    df.to_csv(filename, index=False)
    print(f"Data saved to '{filename}'")



subreddits = ['samsunggalaxy', 'oneui', 'smartphones']
query = 'Samsung'

all_posts = []

for subreddit in subreddits:
    print(f"Scraping subreddit: {subreddit}")
    posts = scrape_reddit(subreddit, query)
    all_posts.extend(posts)

save_to_csv(all_posts, 'reddit_posts.csv')

df = pd.read_csv('reddit_posts.csv')

# print the first few rows of the DataFrame
print("First few rows of the DataFrame:")
print(df.head())
