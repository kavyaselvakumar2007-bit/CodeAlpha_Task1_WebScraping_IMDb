import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.imdb.com/chart/top/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    with open("imdb_top_movies.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Title", "Year", "Rating"])

        movies = soup.select("li.ipc-metadata-list-summary-item")

        for movie in movies:
            rank_tag = movie.select_one(".ipc-title__text")
            title_tag = movie.select_one("h3.ipc-title__text")
            year_tag = movie.select_one("span.cli-title-metadata-item:nth-of-type(1)")
            rating_tag = movie.select_one("span.ipc-rating-star--rating")

            rank = rank_tag.text.split('.')[0] if rank_tag else ""
            title = title_tag.text.split('. ', 1)[-1] if title_tag else ""
            year = year_tag.text if year_tag else ""
            rating = rating_tag.text if rating_tag else ""

            writer.writerow([rank, title, year, rating])

    print("✅ IMDb data scraped successfully and saved to imdb_top_movies.csv!")
else:
    print("❌ Failed to retrieve IMDb page. Status:", response.status_code)