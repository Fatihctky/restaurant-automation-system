import csv
from tabulate import tabulate
from datetime import datetime
import os

DATA_DIR = "data"
CART_FILE = os.path.join(DATA_DIR, "cart.csv")
MENU_FILE = os.path.join(DATA_DIR, "efood.csv")
USER_FILE = os.path.join(DATA_DIR, "IdPass.csv")
FEEDBACK_FILE = os.path.join(DATA_DIR, "Feedback.csv")
ORDERS_FILE = os.path.join(DATA_DIR, "Recommendations.csv")


def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))


def append_csv(path, row):
    with open(path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def login():
    users = load_csv(USER_FILE)[1:]
    username = input("Username: ")
    password = input("Password: ")
    for u, p in users:
        if u == username and p == password:
            print("Login successful!\n")
            return True
    print("Invalid credentials.\n")
    return False


def show_menu():
    menu = load_csv(MENU_FILE)
    print(tabulate(menu[1:], headers=menu[0], showindex=True))


def add_to_cart():
    menu = load_csv(MENU_FILE)[1:]
    show_menu()
    index = int(input("Select item number: "))
    qty = int(input("Quantity: "))
    item = menu[index]
    append_csv(CART_FILE, [item[0], qty, item[1]])
    print(f"{item[0]} added to cart.\n")


def view_cart():
    cart = load_csv(CART_FILE)
    if len(cart) <= 1:
        print("Cart is empty.\n")
        return
    total = 0
    print("\n--- Cart ---")
    for i, row in enumerate(cart[1:], 1):
        subtotal = int(row[1]) * float(row[2])
        total += subtotal
        print(f"{i}) {row[0]} x{row[1]} = ₺{subtotal:.2f}")
    print(f"Total: ₺{total:.2f}\n")


def place_order():
    cart = load_csv(CART_FILE)[1:]
    if not cart:
        print("Cart is empty.\n")
        return
    confirm = input("Confirm order (y/n)? ").lower()
    if confirm == 'y':
        for row in cart:
            append_csv(ORDERS_FILE, row + [datetime.now().strftime("%Y-%m-%d %H:%M")])
        open(CART_FILE, "w").write("Item,Quantity,Price\n")
        print("Order placed successfully!\n")
    else:
        print("Order cancelled.\n")


def give_feedback():
    fb = input("Your feedback: ")
    append_csv(FEEDBACK_FILE, [fb, datetime.now().strftime("%Y-%m-%d %H:%M")])
    print("Thank you!\n")


def admin_panel():
    print("\n1) View Orders\n2) View Feedback")
    choice = input("Choice: ")
    if choice == '1':
        data = load_csv(ORDERS_FILE)
        print(tabulate(data[1:], headers=data[0]))
    elif choice == '2':
        data = load_csv(FEEDBACK_FILE)
        print(tabulate(data[1:], headers=data[0]))
    print()


def main():
    if not login():
        return
    while True:
        print("1) Show Menu\n2) Add to Cart\n3) View Cart\n4) Place Order\n5) Feedback\n6) Admin Panel\n0) Exit")
        choice = input("Select: ")
        if choice == '1':
            show_menu()
        elif choice == '2':
            add_to_cart()
        elif choice == '3':
            view_cart()
        elif choice == '4':
            place_order()
        elif choice == '5':
            give_feedback()
        elif choice == '6':
            admin_panel()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
