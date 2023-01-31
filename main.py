from tkinter import *
from tkinter import messagebox
import datetime as dt
import json

# ---------------------------------------------------INITIALS----------------------------------------------------------#

now = dt.datetime.now()
day = now.day
month = now.month
year = now.year
date = f"{day}|{month}|{year}"

initial = True
zero_accounts = False
menu_updated = False

transact_account = ""
transact_type = ""
transact_mode = ""
transact_amount = 0
transact_reason = ""
account_list = []
balance_dict = {}
info_dict = {}
transact_balance = "---"


# ---------------------------------------------------FUNCTIONS---------------------------------------------------------#


def find_json():
    print("find_json")
    global zero_accounts
    try:
        with open("info.json", mode="r"):
            pass
    except FileNotFoundError:
        with open("info.json", mode="w+") as info_json:
            starting_dic = {"accounts": {},
                            "no_of_accounts": 0,
                            "accounts_name": []}
            json.dump(starting_dic, info_json, indent=4)
            zero_accounts = True


def find_csvs():
    print("find_csv")
    for n in account_list:
        j_bal = balance_dict[n]
        try:
            with open(f"{n}_{month}_{year}_ledger.csv", mode="r"):
                pass
        except FileNotFoundError:
            with open(f"{n}_{month}_{year}_ledger.csv", mode="w+") as new_csv:
                new_csv.write(f"date,type,mode,amount,reason,balance\n{date},-,-,-,-,{j_bal}")


def update_account(selected_account):
    """Updates the variable with respect to selected account"""
    print("updated_accounts")
    print(selected_account)
    global transact_account
    balance_update(selected_account)
    transact_account = selected_account
    account_menu.config(text=selected_account)


def update_type(selected_type):
    """Updates the variables with respect to selected type"""
    print("updated_type")
    global transact_type
    transact_type = selected_type
    type_menu.config(text=selected_type)


def update_mode(selected_mode):
    """Updates the variables with respect to selected mode"""
    print("updated_mode")
    global transact_mode
    transact_mode = selected_mode
    mode_menu.config(text=selected_mode)


def update_json_list_dic():
    """Updates the account list and balance dictionary"""
    print("update_json_list_dic")
    global account_list, balance_dict, info_dict
    with open("info.json", mode='r') as dataJ:
        info_dict = json.load(dataJ)
        account_list = info_dict["accounts_name"]
        balance_dict = info_dict["accounts"]


def clear_entries():
    print("clear entries")
    global transact_amount, transact_reason
    amount_entry.delete(0, END)
    reason_entry.delete(0, END)
    transact_amount = 0
    transact_reason = ""


def update_info_json():
    """updates the json"""

    global transact_account, transact_type, info_dict, transact_amount
    try:
        if transact_type == "Debited":
            info_dict["accounts"][transact_account] -= transact_amount
        elif transact_amount == "Credited":
            info_dict["accounts"][transact_account] += transact_amount
        elif transact_type == "" or transact_mode == "" or transact_account == "":
            raise ValueError
        with open("info.json", mode="w") as json_data:
            json.dump(info_dict, json_data, indent=4)
        update_json_list_dic()
        update_csv()

    except ValueError:
        if transact_type == "":
            messagebox.showinfo(title="Error", message="Please select a transaction type")
        elif transact_mode == "":
            messagebox.showinfo(title="Error", message="Please select a transaction mode")
        else:
            messagebox.showinfo(title="Error", message="Please select an account")


def balance_update(account_name):
    global balance_variable
    with open("info.json", mode="r") as json_dic:
        b_within = json.load(json_dic)
        balance_variable.config(text=b_within["accounts"][account_name])

    pass


def update_csv():
    print("csv updated")
    global transact_account, transact_type, transact_mode, transact_amount, transact_reason, balance_dict
    balance = balance_dict[transact_account]
    with open(f"{transact_account}_{month}_{year}_ledger.csv", mode="a") as lede:
        lede.write(f"{date},{transact_type},{transact_mode},{transact_amount},{transact_reason},{balance}\n")
    balance_update(transact_account)
    clear_entries()


def update_account_menu():
    print("account_menu_updated")
    for account in account_list:
        account_menu.menu.add_command(label=account, command=lambda account=account: update_account(account))


def add_account_clicked():
    """A new window for add new account will be created"""
    print("add_account_clicked")
    add_window = Toplevel(pady=50, padx=50, bg=green)
    add_window.title("ADD ACCOUNT")
    Label(add_window, bg=green, fg="#ffffff", text="NAME OF THE ACCOUNT: ").grid(row=0, column=0, pady=7, sticky="e")
    acc_name_entry = Entry(add_window)
    Label(add_window, fg="#ffffff", text="INITIAL BALANCE: ", bg=green).grid(row=1, column=0, pady=7, sticky="e")
    acc_bal_entry = Entry(add_window)
    Button(add_window, text="ADD ACCOUNT", width=16, bg="#ffffff",
           command=lambda: validate_new_account(acc_bal_entry.get(), acc_name_entry.get(),
                                                add_window)).grid(row=2, column=0, pady=7, columnspan=2)
    acc_name_entry.grid(row=0, column=1)
    acc_name_entry.focus_set()
    acc_bal_entry.grid(row=1, column=1)


def validate_new_account(initial_balance, new_acc_name, pop_window):
    """Validates the new account details and terminates the new window if the details are valid"""
    print("Validation_of_details")
    try:
        initial_balance = int(initial_balance)
        if new_acc_name == '':
            raise ValueError
        new_data = {new_acc_name: initial_balance
                    }
        with open("info.json", mode='r') as data:
            data_dict = json.load(data)
            data_dict["accounts"].update(new_data)
            data_dict["no_of_accounts"] = (data_dict["no_of_accounts"] + 1)
            data_dict["accounts_name"].append(new_acc_name)

        with open("info.json", mode="w") as dataa:
            json.dump(data_dict, dataa, indent=4)
        account_menu.menu.add_command(label=new_acc_name, command=lambda: update_account(new_acc_name))

        with open(f"{new_acc_name}_{month}_{year}_ledger.csv", mode="w") as new:
            new.write(f"date,type,mode,amount,reason,balance\n{date},-,-,-,-,{initial_balance}\n")
        update_json_list_dic()
        account_menu.config(text=new_acc_name)
        update_account(new_acc_name)
        pop_window.destroy()

    except ValueError:
        if initial_balance == "" and new_acc_name == "":
            messagebox.showinfo(title="Expecting data",
                                message="Please fill the account name and initial account balance ")
        elif initial_balance == '':
            messagebox.showinfo(title="Expecting data", message="Please fill the initial account balance ")
        elif new_acc_name == '':
            messagebox.showinfo(title="Expecting data", message="Please fill the account name")
        else:
            messagebox.showinfo(title="Expecting input", message="You can only enter numbers as initial balance")


def add_clicked(amount, reason):
    """Updates the amount and reason, further calling the next action"""
    print("add_clicked")
    global transact_amount, transact_reason
    try:
        transact_amount = int(amount)
        if reason == "":
            raise ValueError
        transact_reason = reason
        update_json_list_dic()
        update_info_json()

    except ValueError:
        if reason == "":
            messagebox.showinfo(title="Error", message="Reason is mandatory")
        else:
            messagebox.showinfo(title="Error", message="Amount should only contain numbers")


# ----------------------------------------------------START_CHECK------------------------------------------------------#

if initial:
    find_json()
    update_json_list_dic()
    find_csvs()
    initial = False

# ----------------------------------------------------UI-SETUP---------------------------------------------------------#


background = "#b0cbf7"
green = "#556278"
txt_font = ("Roboto", 13)

window = Tk()
window.title("Ledger Entry")
window.config(bg=background, pady=50, padx=50)

canvas = Canvas(width=310, height=334, bg=background, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(155, 167, image=logo)

date_label = Label(text=f"Date: {date}", bg=background, font=("Roboto", 15))

type_label = Label(text="Type: ", font=txt_font, bg=background)

type_menu = Menubutton(window, text="Select Type", width=19, relief="raised", bg="#ffffff")
type_menu.menu = Menu(type_menu, tearoff=0)
type_menu["menu"] = type_menu.menu
type_menu.menu.add_command(label="Debited", command=lambda: update_type("Debited"))
type_menu.menu.add_command(label="Credited", command=lambda: update_type("Credited"))

mode_label = Label(text="Mode: ", bg=background, font=txt_font)

mode_menu = Menubutton(window, text="Select Mode", width=19, relief="raised", bg="#ffffff")
mode_menu.menu = Menu(mode_menu, tearoff=0)
mode_menu["menu"] = mode_menu.menu
mode_menu.menu.add_command(label="UPI", command=lambda: update_mode("UPI"))
mode_menu.menu.add_command(label="Cash", command=lambda: update_mode("Cash"))

amount_label = Label(text="Amount: ", bg=background, font=txt_font)
amount_entry = Entry(relief="flat")

reason_label = Label(text="Reason: ", bg=background, font=txt_font)
reason_entry = Entry(relief="flat")

add_button = Button(text="ADD", width=41, bg="#ffffff",
                    command=lambda: add_clicked(amount_entry.get(), reason_entry.get()))

account_menu = Menubutton(window, text="CHoose account", font=txt_font, bg=background, activebackground=background,
                          activeforeground="#fbfb9b", relief="flat", justify="right")
account_menu.menu = Menu(account_menu, tearoff=0)
account_menu["menu"] = account_menu.menu
account_menu.menu.add_command(label="Add Account", command=lambda: add_account_clicked())

balance_label = Label(text="Balance: ", bg=background, font=txt_font)
balance_variable = Label(text=f"{transact_balance}", bg=background, font=txt_font)

if not menu_updated:
    update_account_menu()
    menu_updated = True

canvas.grid(row=0, column=0, rowspan=10, padx=15)
date_label.grid(row=3, column=1, columnspan=2, sticky="w")
account_menu.grid(row=3, column=3, columnspan=2)
type_label.grid(row=4, column=1, sticky="e")
type_menu.grid(row=4, column=2, padx=(0, 20))
mode_label.grid(row=4, column=3, sticky="e")
mode_menu.grid(row=4, column=4)
amount_label.grid(row=5, column=1, sticky="e")
amount_entry.grid(row=5, column=2, padx=(0, 20))
reason_label.grid(row=5, column=3, sticky="e")
reason_entry.grid(row=5, column=4)
add_button.grid(row=6, column=2, columnspan=3)
balance_label.grid(row=7, column=2, rowspan=2, sticky='e')
balance_variable.grid(rowspan=2, column=3, row=7, sticky='w', columnspan=2)

window.mainloop()
