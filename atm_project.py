from decimal import Decimal
import sys
import mysql.connector
import random

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password="",  # change if needed
    database="atm_db"
)
cursor = conn.cursor()

# ---------------- Helper Functions ----------------
def get_card(card_number, pin=None):
    """Fetch card details. If pin is None, only check if card exists."""
    if pin:
        cursor.execute("SELECT card_number, pin, balance FROM cards WHERE card_number=%s AND pin=%s",
                       (card_number, pin))
    else:
        cursor.execute("SELECT card_number FROM cards WHERE card_number=%s", (card_number,))
    return cursor.fetchone()

def add_new_card(card_number, pin):
    cursor.execute(
        "INSERT INTO cards (card_number, pin, balance) VALUES (%s, %s, %s)",
        (card_number, pin, Decimal('10000.00'))  # default balance
    )
    conn.commit()

def update_balance(card_number, new_balance):
    cursor.execute("UPDATE cards SET balance=%s WHERE card_number=%s", (new_balance, card_number))
    conn.commit()

def generate_otp():
    return random.randint(1000, 9999)

def record_transaction(card_number, txn_type, amount):
    cursor.execute("INSERT INTO transactions (card_number, type, amount) VALUES (%s, %s, %s)",
                   (card_number, txn_type, amount))
    conn.commit()

def show_mini_statement(card_number):
    cursor.execute("SELECT type, amount, txn_time FROM transactions WHERE card_number=%s ORDER BY txn_time DESC LIMIT 5",
                   (card_number,))
    transactions = cursor.fetchall()
    if not transactions:
        print("No transactions found.")
    else:
        print("\n--- Mini Statement (Last 5) ---")
        for t in transactions:
            print(f"{t[2]} - {t[0].title()} of ₹{t[1]}")
        print("-------------------------------")

def forgot_pin():
    card_number = input("Enter your card number: ").strip()
    if not (card_number.isdigit() and len(card_number) == 16):
        print("Invalid card number format.")
        return

    # Check if card exists
    cursor.execute("SELECT card_number FROM cards WHERE card_number = %s", (card_number,))
    result = cursor.fetchone()
    if not result:
        print("Card number not found.")
        return

    # OTP verification
    otp = generate_otp()
    print(f"Your OTP is: {otp}")
    entered_otp = input("Enter OTP: ").strip()
    if entered_otp != str(otp):
        print("Invalid OTP.")
        return

    # New PIN setup
    new_pin = input("Enter new 4-digit PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("PIN must be 4 digits.")
        return

    cursor.execute("UPDATE cards SET pin=%s WHERE card_number=%s", (new_pin, card_number))
    conn.commit()
    print("PIN updated successfully!")

def change_pin_logged_in(card_number):
    otp = generate_otp()
    print(f"Your OTP is: {otp}")
    entered_otp = input("Enter OTP: ").strip()
    if entered_otp != str(otp):
        print("Invalid OTP.")
        return

    new_pin = input("Enter your new 4-digit PIN: ").strip()
    confirm_pin = input("Confirm your new PIN: ").strip()

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("PIN must be 4 digits.")
        return

    cursor.execute("UPDATE cards SET pin=%s WHERE card_number=%s", (new_pin, card_number))
    conn.commit()
    print("PIN updated successfully! Please login again.")

# ---------------- Main Program ----------------
while True:
    print("\n--- ATM Main Menu ---")
    print("1. Login")
    print("2. Forgot PIN")
    print("3. Exit")
    main_choice = input("Choose an option: ").strip()

    if main_choice == "1":  # Login
        card_number = input("Enter 16-digit card number: ").strip()
        if not (card_number.isdigit() and len(card_number) == 16):
            print("Card number must be 16 digits.")
            continue

        existing_card = get_card(card_number)

        if not existing_card:
            print("Card not found! Starting registration...")
            otp = generate_otp()
            print(f"Your OTP is: {otp}")
            entered_otp = input("Enter OTP: ").strip()
            if entered_otp != str(otp):
                print("Invalid OTP.")
                continue

            new_pin = input("Set your 4-digit PIN: ").strip()
            if not (new_pin.isdigit() and len(new_pin) == 4):
                print("PIN must be 4 digits.")
                continue

            add_new_card(card_number, new_pin)
            balance = Decimal('10000.00')
            print("Card registered successfully! Please login again.")
            continue

        # Existing card → PIN check
        pin = input("Enter 4-digit PIN: ").strip()
        card_data = get_card(card_number, pin)
        if not card_data:
            print("Invalid PIN.")
            continue

        balance = Decimal(card_data[2])

        # Account Menu
        while True:
            print("\n--- Account Menu ---")
            print("1. Withdraw")
            print("2. Balance Enquiry")
            print("3. Mini Statement")
            print("4. New PIN Generation with OTP")
            print("5. Logout")
            sub_choice = input("Choose an option: ").strip()

            if sub_choice == "1":
                amount = input("Enter amount to withdraw: ").strip()
                if not amount.isdigit():
                    print("Invalid amount.")
                    continue
                amount = Decimal(amount)
                if amount <= 0:
                    print("Amount must be greater than zero.")
                elif amount <= balance:
                    balance -= amount
                    update_balance(card_number, balance)
                    record_transaction(card_number, "withdraw", amount)
                    print(f"Withdrawal successful! Remaining balance: ₹{balance}")
                else:
                    print("Insufficient funds.")

            elif sub_choice == "2":
                print(f"Your balance is: ₹{balance}")

            elif sub_choice == "3":
                show_mini_statement(card_number)

            elif sub_choice == "4":
                change_pin_logged_in(card_number)
                break  # force logout after PIN change

            elif sub_choice == "5":
                print("Logging out...")
                break

            else:
                print("Invalid choice.")

    elif main_choice == "2":
        forgot_pin()

    elif main_choice == "3":
        print("Thank you for using the ATM.")
        break

    else:
        print("Invalid choice.")

