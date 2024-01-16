class Book:
	def __init__(self, product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, image_url):
		self.product_page_url = product_page_url
		self.universal_product_code = universal_product_code
		self.book_title = book_title
		self.price_including_tax = price_including_tax
		self.price_excluding_tax = price_excluding_tax
		self.quantity_available = quantity_available
		self.product_description = product_description
		self.category = category
		self.review_rating = review_rating
		self.image_url = image_url