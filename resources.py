from typing import List
import datetime

###

class Account():
    account_instances = []
    def __init__(self, acc_type: str, acc_number: int, holder, holder_name: str, balance: float, transaction_history: List[tuple]):
        Account.account_instances.append(self) ## to record instances of each account
        self.acc_type = acc_type
        self.__acc_number = acc_number
        self.holder = holder
        self.holder_name = holder_name
        self.balance = balance
        self.transaction_history = transaction_history

    def make_deposit(self, amount: float):
        assert amount > 0
        self.balance += amount
        dt_of_deposit = datetime.datetime.now()
        self.transaction_history.append((dt_of_deposit.strftime("%d/%b/%Y %H:%M:%S"), 'deposit  ',amount))

    def make_withdrawl(self, amount: float):
        assert amount > 0 and amount <= self.balance
        self.balance -= amount
        dt_of_withdrawl = datetime.datetime.now()
        self.transaction_history.append((dt_of_withdrawl.strftime("%d/%b/%Y %H:%M:%S"), 'withdrawl', -amount))

    def get_history(self):
        return self.transaction_history

    def get_balance(self):
        return self.balance
    
    def get_acc_type(self):
        return self.acc_type
    
    def get_holder_name(self):
        return self.holder_name
    
    def get_acc_number(self):
        return self.__acc_number
    
    def get_summary(self):
        return self.__dict__


class Holder():
    holder_instances = []
    def __init__(self, name: str):
        Holder.holder_instances.append(self)
        self.name = name
        self.accounts = []

    def display_info(self):
        print("=========================")
        print(f"Name: {self.name}")
        for account in self.accounts:
            print(f"{account.get_acc_type()}: {account.get_balance()}")

    def account_select(self)->Account:
        """ Prompts user to select one of their account or chooses their only account if there is only 1. Returns the selected account object. """
        num_accounts: int = len(self.accounts)
        if num_accounts > 1:
                options = {}
                for idx in range(num_accounts):
                    options[idx+1] = self.accounts[idx]
                #print(options)
                print("-----------------------------")
                print("Please select which account you would like to select:")
                while True:
                    for option, account in options.items():
                        print(f"{option} : {account.get_acc_type()}, Balance: ${account.get_balance()}")
                    print(f"{num_accounts+1} : to exit\n")
                    
                    user_input = input()
                    try: 
                        assert int(user_input)-1 in range(num_accounts+1)
                        user_input = int(user_input)
                        print(user_input)
                        if user_input == (num_accounts + 1):
                            return None
                        else:
                            selected_acc = options[user_input]
                            return selected_acc
                    except: 
                        print("Please only enter a valid option.")
        elif num_accounts == 1:
            return self.accounts[0]
        else:
            return


###

def create_account(new_holder: Holder) -> Account:
    """ Creates an account object for inputed Holder. Prompts user for type of account to open. """
    account_num: int = len(Account.account_instances) + 1
    
    chosen_type: int = int(input("Please enter 1 to open a checking account or 2 to open a savings account:"))
    while True:
        if chosen_type == 1:
            chosen_type_str: str = "checking"
            break
        elif chosen_type == 2:
            chosen_type_str: str = "savings"
            break
        else:
            print("Please only enter a 1 or 2.")
        chosen_type: int = int(input("Please enter 1 to open a checking account or 2 to open a savings account:"))
    
    starting_balance: float = 0.0
    
    new_account = Account(acc_type = chosen_type_str, 
                            acc_number = account_num, 
                            holder = new_holder,
                            holder_name = new_holder.name,
                            balance = starting_balance,
                            transaction_history = [])
    new_holder.accounts.append(new_account)
    print(f"You have succesfully opened a new {new_account.get_acc_type()} account.")
    return new_account
    

def initialize():
    """ Prompts user for name, if name exists as a holder name, returns that Holder obejct, otherwise creates a new Holder and returns it. """
    user: str = input("Please enter your name: ")
    for _holder in Holder.holder_instances:
        if user == _holder.name:
            return _holder
    new_holder = Holder(user)
    return new_holder


def menu(holder: Holder):
    """ Main user interface for the bank app. """

    print("=============================")
    print("|         MAIN MENU         |")
    print("-----------------------------")
    print(f"Welcome {holder.name}!")
    while True:
        print("-----------------------------")
        print("Please enter:\n1 : to open an account\n2 : to check balances\n3 : to make a deposit\n4 : to make a withdrawl")
        print("5 : to check transaction history\n6 : to exit program\n")
        while True:
            user_input = input()
            try:
                user_input = int(user_input)
            except:
                print("Please only select one of the valid options")
            try: 
                assert user_input in [1,2,3,4,5,6]
            except:    
                print("Please only select one of the valid options")
            else:
                break
        if user_input == 1:  #create account
            create_account(holder)

        elif user_input == 2: #balances
            print("-----------------------------\nBalances:")
            for account in holder.accounts:
                print(F"{account.get_acc_type()}: ${account.get_balance()}")

        elif user_input == 3: #deposit
            num_accounts = len(holder.accounts)
            acc_choice = holder.account_select()
            if acc_choice == None:
                print("No account selected or available")
            else:
                print(f"Enter much you would like to deposit in {acc_choice.get_acc_type()} or type x to exit: ")
                while True:
                    try:
                        user_input = input()
                        if user_input in ['x','X']:
                            break
                        amt = float(user_input)
                        acc_choice.make_deposit(amt)
                        break
                    except:
                        print("Please enter a valid amount.")
                    

        elif user_input == 4: #withdraw
            num_accounts = len(holder.accounts)
            acc_choice = holder.account_select()
            if acc_choice == None:
                print("No account selected or available")
            else:
                print(f"Enter how much you would like to withdraw from {acc_choice.get_acc_type()} or type x to exit: ")
                while True:
                    try:
                        user_input = input()
                        if user_input in ['x','X']:
                            break
                        amt = float(user_input)
                        acc_choice.make_withdrawl(amt)
                        break
                    except:
                        print("Please enter a valid amount.")

        elif user_input == 5: #transaction history
            num_accounts = len(holder.accounts)
            acc_choice = holder.account_select()
            if acc_choice == None:
                print("No account selected or available")
            else:
                transaction_hist = acc_choice.get_history()
                print("--------------------------------------------")
                print("  Transaction Date   |   Type    | Amount ")
                print("--------------------------------------------")
                for entry in transaction_hist:
                    print(f"{entry[0]} | {entry[1]} | {entry[2]}")
            
        else:
            print("-----------------------------")
            print("Thank you for using our services!")
            return

