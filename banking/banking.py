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
    cur.execute(f'INSERT INTO card VALUES ({acct_id}, {number}, "{pin}", {balance})')
    update_database()


def fetch_acct(num, pin):
    cards = cur.execute('SELECT * FROM card WHERE (number=? and pin=?)', (num, pin,))
    return cards.fetchone()


def update_database():
    # commit changes
    conn.commit()


def create_luhn(card):
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


def check_luhn(card_num):
    nums = list(card_num)

    for index in range(len(nums) - 1):
        if index % 2 == 0:
            nums[index] = int(nums[index]) * 2
        else:
            nums[index] = int(nums[index])

    for index in range(len(nums) - 1):
        if int(nums[index]) > 9:
            nums[index] = int(nums[index]) - 9
        else:
            nums[index] = int(nums[index])

    nums[-1] = int(nums[-1])
    nums_sum = sum(nums)

    if nums_sum % 10 == 0:
        return True
    else:
        return False


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

        check_sum = create_luhn(self.card_num)
        self.card_num = self.card_num + str(check_sum)

        # generate pin number
        self.pin_num = str(random.randint(0000, 9999)).zfill(4)

        self.acct_balance = 0

        # store new account info
        insert_new_acct(self.card_num, self.pin_num, self.acct_balance)

        # print new account info
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
            self.card_num = card
            self.pin_num = pin
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
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")

            customer_menu_choice = input()

            if customer_menu_choice == "1":  # print balance
                print()
                print(f"Balance: {self.acct_balance}")
                print()
            elif customer_menu_choice == "2":  # add income
                print()
                print('Enter income:')
                income = int(input())
                self.add_income(income)
                print('Income was added!')
                print()
            elif customer_menu_choice == "3":  # do transfer
                print()
                self.transfer_money()
                print("Success!")
                print()
            elif customer_menu_choice == "4":  # close account
                print()
                self.close_account()
                print('The account has been closed!')
                print()
            elif customer_menu_choice == "5":  # log out
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

    def add_income(self, money):
        account = fetch_acct(self.card_num, self.pin_num)
        self.acct_balance += money

        sql = '''UPDATE card
                SET balance = ?
                WHERE number = ?'''
        cur.execute(sql, (self.acct_balance, account[1]))
        update_database()

    def transfer_money(self):
        current_acct = fetch_acct(self.card_num, self.pin_num)
        print(current_acct)

        print('Enter card number:')
        transfer_num = input()

        transfer_acct = cur.execute('SELECT * FROM card WHERE (number=?)', (transfer_num,))
        fetch_transfer_acct = transfer_acct.fetchone()
        print(fetch_transfer_acct)

        if transfer_num == self.card_num:
            print("You can't transfer money to the same account!")
            print()
        else:
            if check_luhn(transfer_num):
                if fetch_transfer_acct is None:
                    print('Such a card does not exist.')
                    print()
                else:
                    print('Enter how much money you want to transfer:')
                    transfer_amt = int(input())
                    if self.acct_balance < transfer_amt:
                        print('Not enough money!')
                        print()
                    else:
                        # update user balance
                        self.acct_balance -= transfer_amt
                        sql = '''UPDATE card
                                SET balance = ?
                                WHERE number = ?'''
                        cur.execute(sql, (self.acct_balance, current_acct[1]))
                        update_database()

                        # update transfer account
                        print(fetch_transfer_acct[3])

                        transfer_balance = fetch_transfer_acct[3] + transfer_amt
                        print(transfer_balance)
                        sql = '''UPDATE card
                                SET balance = ?
                                WHERE number = ?'''
                        cur.execute(sql, (transfer_balance, fetch_transfer_acct[1]))
                        update_database()
            else:
                print('Probably you made a mistake in the card number. Please try again!')

    def close_account(self):
        cur.execute('DELETE FROM card WHERE number = ?', (self.card_num,))
        update_database()


if __name__ == '__main__':
    conn = _sqlite3.connect('card.s3db')
    cur = conn.cursor()
    drop_table()
    create_table()
    bank = BankingSystem()
