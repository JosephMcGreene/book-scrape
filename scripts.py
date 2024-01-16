import requests as reqs
from bs4 import BeautifulSoup
import csv
from book import Book

scrape_url = "http://books.toscrape.com/"
url_extension = "catalogue/category/books/"
book_urls = []
csv_headers = ["product_page_url", "universal_product_code", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]

def get_book(book_url):
	res = reqs.get(f"{book_url}")

	if res.status_code == 200:
		page_content = res.text
	else:
		return print(f"Oopsie! Status Code: {res.status_code}")
		
	soup = BeautifulSoup(page_content, "html.parser")

	table = soup.find("table")
	table_rows = table.find_all("tr")

	upc = table_rows[0].find("td").text
	title = soup.find("h1").text
	price_with_tax = table_rows[3].find("td").text
	price_without_tax = table_rows[2].find("td").text
	quantity_available = soup.find("p", class_="availability").text.strip()
	description = soup.find(id="product_description").find_next_sibling().text
	category = soup.find("ul", class_="breadcrumb").find_all()[-2].text

	review_ratings = soup.find("p", class_="star-rating").get("class")
	rating = f"{review_ratings[1]} out of Five Stars"

	img_src = soup.find("img").get("src")

	return Book(res.url, upc, title, price_with_tax, price_without_tax, quantity_available, description, category, rating, img_src)


def urls_from_category(category):
	res = reqs.get(f"{scrape_url}/catalogue/category/books/{category}")

	if res.status_code == 200:
		page_content = res.text
	else:
		return print(f"Oopsie! Status Code: {res.state_code}")
		
	soup = BeautifulSoup(page_content, "html.parser")

	books_in_category = soup.find("section").find_all("div")[1].find("ol").find_all("li")

	for book in books_in_category:
		book_url = book.find("article").find("div").find("a").get("href")
		book_urls.append(book_url)
	

def get_details_from_category(category):
	urls_from_category(category)
	csv_data = [csv_headers]
	
	for url in book_urls:
		book = get_book(f"{scrape_url}{url_extension}{category}/{url}")

		book_data = [book.product_page_url, book.universal_product_code, book.book_title, book.price_including_tax, book.price_excluding_tax, book.quantity_available, book.product_description, book.category, book.review_rating, book.image_url]

		csv_data.append(book_data)

	return csv_data


def write_csv(data):
	with open("travel.csv", "w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerows(data)

write_csv(get_details_from_category("travel_2"))
# write_csv(csv_headers)