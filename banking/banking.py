# Write your code here
import random

all_accounts = {}


def print_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def generate_checksum(acct_num):
    nums = list(acct_num)

    for index in range(len(nums)):
        if index % 2 == 0:
            nums[index] = int(nums[index]) * 2
        else:
            nums[index] = int(nums[index])

    for index in range(len(nums)):
        if int(nums[index]) > 9:
            nums[index] = int(nums[index]) - 9
        else:
            nums[index] = int(nums[index])

    nums_sum = sum(nums)

    if nums_sum % 10 == 0:
        return 0
    else:
        check = nums_sum + (10 - nums_sum % 10)
        return check - nums_sum


def create_account():
    temp_account_num = []

    mii = "4"  # digit 1
    iin = "00000"  # digits 2 - 6
    account_id = [str(random.randint(0, 9)) for _ in range(9)]  # digit 7 to n - 1, with n being between 15 and 18

    temp_pin_num = [str(random.randint(0, 9)) for _ in range(4)]
    balance = "0"

    temp_account_num.append(mii)
    temp_account_num.append(iin)
    temp_account_num.append("".join(account_id))

    generate_account_num = "".join(temp_account_num)

    checksum = generate_checksum(generate_account_num)  # digit 16-19 depending on card, verification digit
    temp_account_num.append(str(checksum))

    account_num = "".join(temp_account_num)
    pin_num = "".join(temp_pin_num)

    all_accounts[account_num] = {'pin': pin_num, 'balance': balance}

    print('Your card has been created')
    print('Your card number:')
    print(account_num)
    print('Your card PIN:')
    print(pin_num)
    print()


def customer_menu(account):
    print()
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")

    customer_menu_choice = input()

    if customer_menu_choice == "1":
        print()
        print(f"Balance: {account['balance']}")
    elif customer_menu_choice == "2":
        print()
        print('You have successfully logged out!')
        print_menu()
    else:
        print()
        print('Bye')
        exit()


def validate_checksum(card_num):
    nums = list(card_num)

    print(nums)
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
    print(nums)
    nums_sum = sum(nums)

    if nums_sum % 10 == 0:
        return True
    else:
        return False


def verify_account(card, pin_num):
    if card in all_accounts:
        if pin_num == all_accounts[card]['pin']:
            if validate_checksum(card):
                print()
                print('You have successfully logged in!')
                customer = all_accounts[card]
                customer_menu(customer)
            else:
                print()
                print("Wrong card number or PIN!")
                print()
                print_menu()
                log_in_account()
        else:
            print()
            print("Wrong card number or PIN!")
    else:
        print()
        print("Wrong card number or PIN!")


def log_in_account():
    card_num = input('Enter your card number: \n')
    user_pin = input('Enter your PIN: \n')

    verify_account(card_num, user_pin)
    print()


def program():
    print_menu()
    user_menu_choice = input()
    print()

    while True:
        if user_menu_choice == "1":
            create_account()
            # print()
        elif user_menu_choice == "2":
            print()
            log_in_account()
        elif user_menu_choice == "0":
            print()
            print('Bye')
            break
        else:
            print("Invalid Menu Entry")
            print()

        print_menu()
        user_menu_choice = input()


program()
