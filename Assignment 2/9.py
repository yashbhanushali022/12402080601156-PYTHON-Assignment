class Product:

    def __init__(
        self,
        product_id,
        name,
        stock,
        purchase_price,
        selling_price
    ):

        self.product_id = product_id
        self.name = name

        self.stock = int(stock)

        self.purchase_price = float(
            purchase_price
        )

        self.selling_price = float(
            selling_price
        )


    def value(self):

        return (
            self.stock
            * self.purchase_price
        )


class Inventory:

    def __init__(self):

        self.products = {}


    def add_product(self, product):

        self.products[
            product.product_id
        ] = product


    def delete_product(self, product_id):

        if product_id in self.products:

            del self.products[
                product_id
            ]

            return True

        return False


    def update_product(
        self,
        product_id,
        stock,
        purchase_price,
        selling_price
    ):

        if product_id not in self.products:

            return False

        product = self.products[
            product_id
        ]

        product.stock = int(stock)

        product.purchase_price = float(
            purchase_price
        )

        product.selling_price = float(
            selling_price
        )

        return True


    def total_value(self):

        return sum(
            product.value()
            for product in self.products.values()
        )


    # Compare inventories
    def __lt__(self, other):

        return (
            self.total_value()
            <
            other.total_value()
        )


    # Merge inventories
    def __add__(self, other):

        merged = Inventory()


        # Copy first inventory
        for product in self.products.values():

            merged.add_product(
                Product(
                    product.product_id,
                    product.name,
                    product.stock,
                    product.purchase_price,
                    product.selling_price
                )
            )


        # Add second inventory
        for product in other.products.values():

            if product.product_id not in merged.products:

                merged.add_product(
                    Product(
                        product.product_id,
                        product.name,
                        product.stock,
                        product.purchase_price,
                        product.selling_price
                    )
                )

            else:

                existing = merged.products[
                    product.product_id
                ]

                # Combine stock
                existing.stock += (
                    product.stock
                )

                # Keep lower purchase price
                existing.purchase_price = min(
                    existing.purchase_price,
                    product.purchase_price
                )

                # Keep higher selling price
                existing.selling_price = max(
                    existing.selling_price,
                    product.selling_price
                )


        return merged


def read_inventory():

    inventory = Inventory()

    number = int(
        input(
            "Number of products: "
        )
    )


    for _ in range(number):

        parts = input(
            "ID Name Stock Purchase Selling: "
        ).split()


        if len(parts) != 5:

            print(
                "Invalid product."
            )

            continue


        product_id = parts[0]
        name = parts[1]
        stock = parts[2]
        purchase = parts[3]
        selling = parts[4]


        product = Product(
            product_id,
            name,
            stock,
            purchase,
            selling
        )

        inventory.add_product(
            product
        )


    return inventory


# Inventory A
print("Inventory A")

A = read_inventory()


# Inventory B
print("Inventory B")

B = read_inventory()


q = int(
    input(
        "Number of operations: "
    )
)


for _ in range(q):

    command = input().split()

    operation = command[0].upper()


    if operation == "ADD":

        _, pid, name, stock, purchase, selling = command

        A.add_product(
            Product(
                pid,
                name,
                stock,
                purchase,
                selling
            )
        )

        print("ADD_OK")


    elif operation == "DELETE":

        pid = command[1]

        if A.delete_product(pid):

            print("DELETE_OK")

        else:

            print("NOT_FOUND")


    elif operation == "UPDATE":

        (
            _,
            pid,
            stock,
            purchase,
            selling
        ) = command


        if A.update_product(
            pid,
            stock,
            purchase,
            selling
        ):

            print("UPDATE_OK")

        else:

            print("NOT_FOUND")


    elif operation == "COMPARE":

        if A.total_value() > B.total_value():

            print("A_GREATER")

        elif A.total_value() < B.total_value():

            print("B_GREATER")

        else:

            print("EQUAL")


    elif operation == "MERGE":

        merged = A + B


        for pid in sorted(
            merged.products
        ):

            product = merged.products[
                pid
            ]

            print(
                product.product_id,
                product.name,
                "stock=" + str(
                    product.stock
                ),
                "purchase=" + str(
                    product.purchase_price
                ),
                "selling=" + str(
                    product.selling_price
                )
            )


        print(
            "TOTAL_VALUE",
            merged.total_value()
        )