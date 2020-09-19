import random
import _sqlite3


def drop_table():
    cur.execute('DROP TABLE IF EXISTS card')


def create_table():
    cur.execute('''CREATE TABLE card
                    (id INTEGER, 
                    number TEXT,
                    pin TEXT,
                    balance INTEGER DEFAULT 0)''')


def insert_new_acct(number, pin, balance):
    id_calc = cur.execute('SELECT count(*) FROM card')
    acct_id = id_calc.fetchone()[0] + 1
    cur.execute(f'INSERT INTO card VALUES ({acct_id}, {number}, {pin}, {balance})')
    update_database()


def fetch_acct(num, pin):
    # cards = cur.execute('SELECT * FROM card')
    cards = cur.execute('SELECT * FROM card WHERE (number=? and pin=?)', (num, pin,))
    return cards.fetchone()


def update_database():
    # commit changes
    conn.commit()


def check_lyhn(card):
    check_sum = 0  # digit 16-19 depending on card, verification digit

    for index in range(len(card)):
        if index % 2 == 0:
            n = int(card[index]) * 2
            check_sum += n - 9 if n > 9 else n
        else:
            check_sum += int(card[index])

    if check_sum % 10 == 0:
        final_num = 0
    else:
        final_num = 10 - (check_sum % 10)

    return final_num


class BankingSystem:
    def __init__(self):
        self.card_num = 0
        self.pin_num = 0
        self.acct_balance = 0
        self.main_menu()

    def main_menu(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")

            menu_choice = input()

            if menu_choice == "1":
                self.create_account()
            elif menu_choice == "2":
                # pass
                self.acct_login()
            elif menu_choice == "0":
                print()
                print('Bye')
                conn.close()
                exit()
            else:
                print("Invalid Menu Entry")
                print()

    def create_account(self):
        # generate card number
        mii = "4"  # digit 1
        iin = "00000"  # digits 2 - 6
        acct_num = str(random.randint(100000000, 999999998))  # digit 7 to n - 1, with n being between 15 and 18
        self.card_num = str(mii + iin + acct_num)

        check_sum = check_lyhn(self.card_num)
        self.card_num = self.card_num + str(check_sum)

        # generate pin number
        self.pin_num = str(random.randint(0000, 9999)).zfill(4)

        self.acct_balance = 0

        # store new account info
        insert_new_acct(self.card_num, self.pin_num, self.acct_balance)

        # print new account info
        print('Card length')
        print(len(self.card_num))
        print()
        print('Your card has been created')
        print('Your card number:')
        print(self.card_num)
        print('Your card PIN:')
        print(self.pin_num)
        print()

    def acct_login(self):
        print()
        card = input('Enter your card number: \n')
        pin = input('Enter your PIN: \n')

        if fetch_acct(card, pin) is not None:
            print()
            print('You have successfully logged in!')
            print()
            self.login_success()
        else:
            print()
            print("Wrong card number or PIN!")
            print()

    def login_success(self):
        while True:
            print("1. Balance")
            print("2. Log out")
            print("0. Exit")

            customer_menu_choice = input()

            if customer_menu_choice == "1":
                print()
                print(f"Balance: {self.acct_balance}")
                print()
            elif customer_menu_choice == "2":
                print('You have successfully logged out!')
                print()
                self.main_menu()
            elif customer_menu_choice == "0":
                print()
                print('Bye')
                conn.close()
                exit()
            else:
                print("Invalid Menu Entry")
                print()


if __name__ == '__main__':
    conn = _sqlite3.connect('card.s3db')
    cur = conn.cursor()
    drop_table()
    create_table()
    bank = BankingSystem()
