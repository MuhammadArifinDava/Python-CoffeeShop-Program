# Import library PrettyTable untuk membuat tabel yang rapi dan simpel.
import csv
from pwinput import pwinput  
from prettytable import PrettyTable
from datetime import datetime



# Function untuk menampilkan menu yang sudah diurutkan berdasarkan harga.
def display_sorted_menu(menu):
    table = PrettyTable(["Menu", "Price", "Stock"])  
    for item, price in menu.items():         
        stock_quantity = stock.get(item, 0)         
        table.add_row([item, price, stock_quantity]) 
    print("Sorted Coffee Shop Menu (by Price)")
    print(table)

# Function untuk menyimpan menu ke file CSV.
def save_menu(menu):
    with open('menu.csv', mode='w', newline='') as file:  
        fieldnames = ['Item', 'Price']
        writer = csv.DictWriter(file, fieldnames=fieldnames) 
        writer.writeheader()
        for item, price in menu.items():
            writer.writerow({'Item': item, 'Price': price})   

# Function untuk memuat data pengguna dari file CSV.
def load_users():
    users = []    
    with open('users.csv', mode='r') as file:  
        reader = csv.DictReader(file) 
        for row in reader:            
            users.append(row)         
    return users

# Function untuk menyimpan data pengguna ke file CSV.
def save_users(users):
    with open('users.csv', mode='w', newline='') as file:         
        fieldnames = ['Username', 'Password', 'Role', 'Balance']  
        writer = csv.DictWriter(file, fieldnames=fieldnames)      
        writer.writeheader()
        for customer in users:
            writer.writerow(customer) 

# Function pendaftaran pengguna baru.
def register_user():
    username = input("Enter a new username: ") 
    if not username: 
        print("Username cannot be empty. Please choose a valid username.")
        return

    if username == '-1' or username == '0' or username == "-2" or username == "-3" or username == "-4" or username == "-5" : 
        print("Username cannot be '-1, -2 , -3, -4, -5 ' or '0' . Please choose a different username.")
        return

    existing_users = load_users()   
    for customer in existing_users: 
        if customer['Username'] == username:
            print("Username already exists. Please choose a different username.")
            return

    password = pwinput(prompt="Enter a password:") 
    if not password:
        print("Password cannot be empty. Please enter a valid password.")
        return

    if password == '-1' or password == '0' or password == "-2" or password == "-3" or password == "-4" or password == "-5" :
        print("Password cannot be '-1, -2, -3, -4, -5 ' or '0'. Please choose a different password.")
        return

    role = input("Enter the customer role (cashier, manager, customer): ") 
    if role not in ["cashier", "manager", "customer"]:
        print("Invalid role. Please choose from 'cashier', 'manager', or 'customer'.")
        return

    try:
        balance = int(input("Enter the initial E-money balance: "))        
        if balance <= 0:                                                  
            print("Balance cannot be zero or negative. Please enter a positive balance.")
            return
    except ValueError:                                                     
        print("Invalid balance. Please enter a valid numeric balance.")
        return
    except KeyboardInterrupt:
            print("\ninput yang anda masukkan tidak valid")
            

    new_user = {'Username': username, 'Password': password, 'Role': role, 'Balance': balance} 
    existing_users.append(new_user)        
    save_users(existing_users)            
    print("User registered successfully.")  


# Function untuk memuat data stok barang dari file CSV.
def load_stock():
    stock = {}     
    with open('stock.csv', mode='r') as file: 
        reader = csv.DictReader(file)         
        for row in reader:
            stock[row['Item']] = int(row['Quantity']) 
    return stock
stock = load_stock()  

# Function untuk menyimpan data stok barang ke file CSV.
def save_stock(stock):
    with open('stock.csv', mode='w', newline='') as file:
        fieldnames = ['Item', 'Quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item, quantity in stock.items():
            writer.writerow({'Item': item, 'Quantity': quantity}) 

# Menentukan Menu kopi dengan menggunakan dictionary.
menu = {
    "Espresso":  27500,
    "Cappuccino":  30000,
    "Mocha":  35000,
    "Macchiato":  37500,
    "Redvelvet Latte":  40000,
    "Matcha Latte":  35000
}

# Function untuk memuat menu kopi dari file CSV.
def load_menu():
    menu = {}
    with open('menu.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            menu[row['Item']] = int(row['Price']) 
    return menu

menu = load_menu()  
stock = load_stock()  


# Function untuk menyimpan invoice ke dalam file teks yang dapat diedit (txt).
def save_invoice_to_txt(customer_name, customer_order, total_bill, payment, change):
    with open(f'{customer_name}_invoice.txt', 'w') as invoice_file: 
        invoice_file.write("RumahKita CoffeeShop Invoice\n")       
        invoice_file.write(f"Customer Name: {customer_name}\n")

        # Tambahkan detail pesanan ke invoice
        for coffee, quantity in customer_order.items():
            price_per_coffee = menu.get(coffee, 0)
            invoice_file.write(f"{coffee}: {quantity} x Rp. {price_per_coffee:.2f}\n")

        invoice_file.write(f"Total Bill: Rp. {total_bill:.2f}\n")
        invoice_file.write(f"Payment Amount: Rp. {payment:.2f}\n")
        invoice_file.write(f"Change: Rp. {change:.2f}\n")

# Function untuk menghasilkan invoice pembelian pelanggan.
def generate_invoice(customer_name, customer_order, total_bill, payment, change):
    invoice = PrettyTable()
    invoice.field_names = ["RumahKita CoffeeShop", "Invoice"]
    invoice.add_row(["Customer Name:", customer_name])
    invoice.add_row(["Transaction Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]) 

    # Tambahkan detail pesanan ke invoice
    for coffee, quantity in customer_order.items():
        price_per_coffee = menu.get(coffee, 0)
        invoice.add_row([coffee, f"{quantity} x Rp. {price_per_coffee:.2f}"])
    
    invoice.add_row(["Total Bill:", f"Rp. {total_bill:.2f}"])
    invoice.add_row(["Payment Amount:", f"Rp. {payment:.2f}"])
    invoice.add_row(["Change:", f"Rp. {change:.2f}"])
    print(invoice)
    save_invoice_to_txt(customer_name, customer_order, total_bill, payment, change)


# Inisialisasi dictionary untuk menyimpan pesanan customer dan catatan kasir.
customer_orders = {}  
order_records = {}  
users = load_users()  

# Function untuk antarmuka pelanggan.
def customer_interface():
    while True:
        
        total_bill = 0  
        customer_order = {}  
        customer_name = input("Enter your username (or 'X' to exit): ")
        if customer_name == 'X':
            break
        users = load_users()
        customer = next((u for u in users if u['Username'] == customer_name ), None)
        if customer is None:
            print("User not found. Please register or enter a valid username.")
            continue
        password = pwinput("Enter your password: ")
        if customer['Password'] != password :
            print("Invalid credentials. Please try again or register.")
            continue
        if customer['Role'] != 'customer':
            print("Only customers are allowed to login.")
            continue
        print("Login successful.")
        while True:
            print("1. Order Coffee")
            print("2. Sort Menu by Price")
            print("3. Finish Order")
            choice = input("Enter your choice: ")

            if choice == '1':
                while True:
                    display_menu()
                    coffee = input("Enter a coffee item (or 'X' to finish) : ")
                    if coffee == 'X':
                        break  
                    if coffee in menu and coffee in stock and stock[coffee] > 0:         
                        try:
                            quantity = int(input(f"How many {coffee}s would you like? "))
                            if quantity < 1:
                                print("Input is invalid. Please enter a valid quantity.")    
                                continue
                            if quantity <= stock[coffee]:           
                                customer_order[coffee] = quantity   
                                stock[coffee] -= quantity             
                                total_bill += menu[coffee] * quantity 
                                print(f"Your total bill is Rp. {total_bill:.2f}")
                            else:
                                print("Insufficient stock. Please choose a lower quantity.")
                        except ValueError:                                                  
                            print("Invalid input. Please enter a valid quantity.")
                    elif coffee not in menu:                                               
                        print("Invalid coffee selection. Please choose from the menu.")
                    else:
                        print("Coffee item is out of stock.")

                if int(customer['Balance']) - total_bill < 0:                
                    print("Insufficient E-money balance. Please add funds.")
                    for coffee, quantity in customer_order.items(): 
                        stock[coffee] += quantity
                    total_bill = 0       
                    customer_order = {}  
                else:
                    customer_orders[customer_name] = customer_order 
                    print("Order placed successfully.")
                    print(f"Your total bill is Rp. {total_bill:.2f}")

                    while True:
                        try:
                            payment = int(input("Enter the payment amount using E-money: "))
                            if payment >= total_bill:
                                change = payment - total_bill
                                generate_invoice(customer_name, customer_order, total_bill, payment, change)
                                customer['Balance'] = int(customer['Balance']) - total_bill
                                save_users(users)
                                save_stock(stock)
                                order_records[customer_name] = customer_order
                                break
                            else:
                                print("Insufficient payment. Please pay the full amount.")
                        except KeyboardInterrupt:
                            print("\ninput yang anda masukkan tidak valid")
                            continue
                        except:
                            print("Invalid input. Please enter a valid payment amount.")
                            break
            elif choice == '2':
                sorted_menu = dict(sorted(menu.items(), key=lambda item: item[1])) 
                display_sorted_menu(sorted_menu)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

# Function untuk menampilkan catatan pesanan.
def display_orders():
    table = PrettyTable(["Customer", "Order"])     
    for customer, order in customer_orders.items():
        table.add_row([customer, order])          
    print("Customer Orders")
    print(table)

# Function untuk menambahkan kopi baru ke menu.
def add_new_coffee():
    try:
        new_coffee = input("Enter the name of the new coffee: ")
        if new_coffee in menu:
            print(f"{new_coffee} is already in the menu.")
        else:
            price = int(input(f"Enter the price of {new_coffee}: "))
            stock_quantity = int(input(f"Enter the initial quantity of {new_coffee}: "))
            menu[new_coffee] = price
            stock[new_coffee] = stock_quantity  
            save_menu(menu) 
            save_stock(stock) 
            print(f"{new_coffee} has been added to the menu with a price of Rp. {price:.2f} and a stock of {stock_quantity}.")
            display_menu()  
    except ValueError:
        print("Invalid input. Please enter a valid price and quantity.")
    except KeyboardInterrupt:
            print("\ninput yang anda masukkan tidak valid")


# Function untuk mengupdate stok barang.
def update_stock():
    display_menu()
    item = input("Enter the item to update stock: ")
    if item in stock: 
        try:
            quantity = int(input(f"Enter the new quantity for {item}: "))
            stock[item] = quantity
            print(f"Stock for {item} has been updated to {quantity}.")
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")
        except KeyboardInterrupt:
            print("\ninput yang anda masukkan tidak valid")
    else:
        print("Item not found in stock. Please check the item name.")

# Function untuk menandai pesanan sebagai sudah dibayar.
def search_order():
    customer_name = input("Search Order to del if paid : ")  
    if customer_name in customer_orders:
        del customer_orders[customer_name]
        print(f"{customer_name}'s order has been marked as paid.")
    else:
        print("Customer not found. Please check the name.")

# Function untuk memilih peran setelah login
def role_selection(users):
    while True:
        role_table = PrettyTable()
        role_table.field_names = ["Role Selection"]
        role_table.add_row(["1. Customer"])
        role_table.add_row(["2. Cashier"])
        role_table.add_row(["3. Manager"])
        role_table.add_row(["4. Exit"])
        print(role_table)
        choice = input("Enter your choice: ")

        if choice == '1':
            customer_interface()
        elif choice == '2':
            cashier_interface(users)
        elif choice == '3':
            manager_interface(users)
        elif choice == '4':
            print("Terima kasih telah berkunjung ke RumahKita CoffeeShop")
            break
        else:
            print("Invalid choice. Please try again.")

# Function untuk menampilkan catatan total pesanan.
def display_total_orders():
    table = PrettyTable(["Customer", "Order"])
    for customer, order in order_records.items():
        table.add_row([customer, order])
    print("Customer Orders")
    print(table)

# Function untuk menampilkan total stok barang.
def display_total_stock():
    print("Total Stock:")
    for item, quantity in stock.items():
        print(f"{item}: {quantity}")

# Function untuk mengupdate pesanan pelanggan.
def update_orders():
    customer_name = input("Enter the customer's name to update their order or 'X' to exit: ")
    if customer_name in customer_orders:
        print(f"Current order for {customer_name}: {customer_orders[customer_name]}")
        new_order = {} 
        while True:
            coffee = input("Enter a coffee item to update : ")
            if coffee == 'X':
                break
            if coffee in menu:
                try:
                    new_quantity = int(input(f"How many {coffee}s would you like? "))
                    new_order[coffee] = new_quantity   
                except ValueError:
                    print("Invalid input. Please enter a valid quantity.")
                except KeyboardInterrupt:
                    print("\ninput yang anda masukkan tidak valid")
                    continue
            else:
                print("Invalid coffee selection. Please choose from the menu.")
        customer_orders[customer_name] = new_order     
        print(f"Order for {customer_name} has been updated successfully.")
    else:
        print("Customer not found. Please check the name.")

# Function untuk antarmuka kasir.
def cashier_interface(users):
    while True:
        username = input("Enter your username: ")
        password = pwinput("Enter your password: ")
        customer = None
        for u in users:
            if u['Username'] == username:
                customer = u
                break

        if customer and customer['Password'] == password and customer['Role'] == 'cashier':
            print("Login successful.")
            break
        else:
            print("Invalid credentials. Please try again.")
    while True:
        print("Cashier Interface")
        print("1. View Orders")
        print("2. Mark Orders as Paid")
        print("3. Update Stock")
        print("4. Add New Coffee")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            display_orders()
        elif choice == '2':
            search_order()
        elif choice == '3':
            update_stock() 
        elif choice == '4':
            add_new_coffee()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def manager_interface(users):
    while True:
        try:
            username = input("Enter your username: ")
            password = pwinput("Enter your password: ")
            customer = None
            for u in users:
                if u['Username'] == username:
                    customer = u
                    break

            if customer and customer['Password'] == password and customer['Role'] == 'manager':
                print("Login successful.")
                break
            else:
                print("Invalid credentials. Please try again.")
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")

    while True:
        print("Manager Interface")
        print("1. View Total Orders")
        print("2. View Total Stock")
        print("3. Update Orders")
        print("4. Exit")
        try:
            choice = input("Enter your choice: ")

            if choice == '1':
                display_total_orders()
            elif choice == '2':
                display_total_stock()
            elif choice == '3':
                update_orders()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")

# Function untuk menampilkan menu dengan harga dan stok.
def display_menu():
    table = PrettyTable(["Menu", "Price", "Stock"])  
    for item, price in menu.items():
        stock_quantity = stock.get(item, 0)  
        table.add_row([item, price, stock_quantity])  
    print("Coffee Shop Menu")
    print(table)

# Bagian utama program. ( tampilan awal program )
def main_menu(users):
    while True:
        try:
            welcome_table = PrettyTable()
            welcome_table.field_names = ["Welcome to RumahKita CoffeeShop"]
            welcome_table.add_row(["Main Menu"])
            welcome_table.add_row(["1. Login"])
            welcome_table.add_row(["2. Register"])
            welcome_table.add_row(["3. Exit"])
            print(welcome_table)
            choice = input("Enter your choice: ")

            if choice == '1':
                role_selection(users)
            elif choice == '2':
                register_user()
            elif choice == '3':
                print("Terima kasih telah berkunjung ke RumahKita CoffeeShop, keluar dari pemilihan role")
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")


if __name__ == '__main__':
    main_menu(users)