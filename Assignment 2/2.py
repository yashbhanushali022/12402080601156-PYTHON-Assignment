from html.parser import HTMLParser
import re


class ProductParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.products = []
        self.current_product = None
        self.current_field = None

    def handle_starttag(self, tag, attrs):

        attrs = dict(attrs)

        if tag == "div" and attrs.get("class") == "product":
            self.current_product = {
                "name": "",
                "price": "",
                "rating": ""
            }

        if self.current_product is not None:
            if tag == "span":
                field = attrs.get("class")

                if field in ["name", "price", "rating"]:
                    self.current_field = field

    def handle_data(self, data):

        if self.current_product and self.current_field:
            self.current_product[self.current_field] += data.strip()

    def handle_endtag(self, tag):

        if tag == "div" and self.current_product:

            if self.current_product["name"]:
                self.products.append(self.current_product)

            self.current_product = None
            self.current_field = None


def normalize_price(price):

    price = re.sub(r"[^0-9.]", "", price)

    if price == "":
        return float("inf")

    return float(price)


p, k = map(int, input().split())

products = {}

for _ in range(p):

    file_path = input().strip()

    parser = ProductParser()

    try:

        with open(file_path, "r", encoding="utf-8") as file:
            html = file.read()

        parser.feed(html)

    except OSError as e:
        print("ERROR:", e)
        continue

    for product in parser.products:

        name = product["name"].strip()
        price = normalize_price(product["price"])

        try:
            rating = float(product["rating"])
        except ValueError:
            continue

        # Keep the lower price for duplicate products
        if name not in products:
            products[name] = (price, rating)

        elif price < products[name][0]:
            products[name] = (price, rating)


ranked = sorted(
    products.items(),
    key=lambda x: (
        -x[1][1],
        x[1][0],
        x[0]
    )
)

for name, (price, rating) in ranked[:k]:

    if price.is_integer():
        price = int(price)

    print(name, price, rating)