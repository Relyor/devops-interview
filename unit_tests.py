import unittest
from main import load_products, load_customers, calculate_order_prices, generate_product_customers, calculate_customers_total, generate_customer_ranking


class TestCSVFunctions(unittest.TestCase):
    def test_load_products(self):
        products = load_products()
        self.assertTrue(isinstance(products, dict))
        self.assertTrue(all(isinstance(key, int) for key in products.keys()))
        self.assertTrue(all(isinstance(value, float) for value in products.values()))

    def test_load_customers(self):
        customers = load_customers()
        self.assertTrue(isinstance(customers, dict))
        self.assertTrue(all(isinstance(key, int) for key in customers.keys()))
        self.assertTrue(all(isinstance(value, dict) for value in customers.values()))
        self.assertTrue(all(isinstance(value['firstname'], str) for value in customers.values()))
        self.assertTrue(all(isinstance(value['lastname'], str) for value in customers.values()))

    def test_calculate_order_prices(self):
        products = load_products()
        order_prices = calculate_order_prices(products)
        self.assertTrue(isinstance(order_prices, list))
        self.assertTrue(all(isinstance(item, dict) for item in order_prices))
        self.assertTrue(all('id' in item and 'euros' in item for item in order_prices))

    def test_generate_product_customers(self):
        product_customers = generate_product_customers()
        self.assertTrue(isinstance(product_customers, list))
        self.assertTrue(all(isinstance(item, dict) for item in product_customers))
        self.assertTrue(all('id' in item and 'customer_ids' in item for item in product_customers))

    def test_calculate_customers_total(self):
        products = load_products()
        customer_totals = calculate_customers_total(products)
        self.assertTrue(isinstance(customer_totals, dict))
        self.assertTrue(all(isinstance(key, int) for key in customer_totals.keys()))
        self.assertTrue(all(isinstance(value, float) for value in customer_totals.values()))

    def test_generate_customer_ranking(self):
        products = load_products()
        customers = load_customers()
        customer_totals = calculate_customers_total(products)
        customer_ranking_list = generate_customer_ranking(customer_totals, customers)
        self.assertTrue(isinstance(customer_ranking_list, list))
        self.assertTrue(all(isinstance(item, dict) for item in customer_ranking_list))
        self.assertTrue(all('id' in item and 'firstname' in item and 'lastname' in item and 'total_euros' in item for item in customer_ranking_list))

if __name__ == "__main__":
    unittest.main()
