import csv

def write_to_csv(data, filename, fieldnames):
    # Write the result to order_prices.csv
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def load_products():
    products = {}
    with open('products.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products[int(row['id'])] = float(row['cost'])
    return products

def load_customers():
    customers = {}
    with open('customers.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customers[int(row['id'])] = {'firstname': row['firstname'], 'lastname': row['lastname']}
    return customers

#### TASK 1 ####
def calculate_order_prices(products):
    # Process orders to calculate total cost for each order
    order_prices = []
    with open('orders.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            order_id = int(row['id'])
            product_ids = list(map(int, row['products'].split()))
            total_cost = sum(products[product_id] for product_id in product_ids)
            order_prices.append({'id': order_id, 'euros': total_cost})

    return order_prices

#### TASK 2 ####
def generate_product_customers():
    # Initialize a dictionary to store customers for each product
    product_customers = {}

    # Process orders to identify customers for each product
    with open('orders.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_id = int(row['customer'])
            product_ids = map(int, row['products'].split())
            for product_id in product_ids:
                if product_id not in product_customers:
                    product_customers[product_id] = set()
                product_customers[product_id].add(customer_id)

    # Convert the dictionary to a list of dictionaries for writing to CSV
    product_customers_list = [{'id': product_id, 'customer_ids': ' '.join(map(str, customer_ids))}
                              for product_id, customer_ids in product_customers.items()]

    # Sort the list of dictionaries by the 'id' field
    product_customers_list.sort(key=lambda x: x['id'])

    return product_customers_list

### TASK 3 ###
def calculate_customers_total(products):
    # Process orders.csv to calculate total euros spent by each customer
    customer_totals = {}

    with open('orders.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_id = int(row['customer'])
            product_ids = map(int, row['products'].split())
            total_cost = sum(products[product_id] for product_id in product_ids)
            customer_totals[customer_id] = customer_totals.get(customer_id, 0) + total_cost

    return customer_totals

def generate_customer_ranking(customer_totals, customers):
    # Convert customer_totals dictionary to a list of dictionaries for writing to CSV
    customer_ranking_list = [{'id': customer_id, 'firstname': customers[customer_id]['firstname'],
                              'lastname': customers[customer_id]['lastname'], 'total_euros': total_euros}
                             for customer_id, total_euros in customer_totals.items()]

    # Sort the list of dictionaries by the 'total_euros' field in descending order
    customer_ranking_list.sort(key=lambda x: x['total_euros'], reverse=True)

    return customer_ranking_list

def main():
    products = load_products()
    customers = load_customers()

    # task 1
    order_prices = calculate_order_prices(products)
    write_to_csv(order_prices, 'order_prices.csv', ['id', 'euros'])
    print("order_prices.csv has been generated successfully.")

    # task 2
    product_customers = generate_product_customers()
    write_to_csv(product_customers, 'product_customers.csv', ['id', 'customer_ids'])
    print("product_customers.csv has been generated successfully.")

    # task 3
    customer_totals = calculate_customers_total(products)
    customer_ranking_list = generate_customer_ranking(customer_totals, customers)
    write_to_csv(customer_ranking_list, 'customer_ranking.csv', ['id', 'firstname', 'lastname', 'total_euros'])
    print("customer_ranking.csv has been generated successfully.")

if __name__ == "__main__":
    main()
