from prettytable import PrettyTable
from prettytable import DOUBLE_BORDER
import csv
import time
from datetime import date
import pandas as pd
import sys
import requests
from tabulate import tabulate


class User:
    class Employee:
        def create(self, name):
            with open(name, "a") as file:
                fieldnames = [
                    "Employee",
                    "Hours",
                    "Pay",
                    "Position",
                    "Hours_required",
                    "last_ran",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                self.employee = input("What is the Employee's name? ").title()
                self.pay = input(f"How much does {self.employee} get paid per hour? ")
                try:
                    int(self.pay)
                except ValueError:
                    self.pay = 0
                self.hours = input(
                    f"Are there any hours you want to log for {self.employee}, type 0 for none: "
                )
                try:
                    int(self.hours)
                except ValueError:
                    self.hours = 0
                self.position = input(
                    f"What position does {self.employee} hold? "
                ).title()
                self.hours_required = input(
                    f"Number of hours {self.employee} is required to work per week: "
                )
                try:
                    int(self.hours_required)
                except ValueError:
                    self.hours_required = 0
                last_ran = date.today()
                writer.writerow(
                    {
                        "Employee": self.employee,
                        "Hours": self.hours,
                        "Pay": self.pay,
                        "Position": self.position,
                        "Hours_required": self.hours_required,
                        "last_ran": last_ran,
                    }
                )
                self.hours_reset(name)
                main()

        def edit(self, name):
            df = pd.read_csv(name)
            employee = input("Please enter the employee you want to edit: ").title()
            while employee not in df.values:
                y = input(
                    "That employee does not exist would you like to create one?, type y for yes: "
                ).lower()
                while y != "y" and y != "n":
                    print("Please try again")
                    y = input(
                        "That employee does not exist would you like to create one?, type y for yes: "
                    ).lower()
                if y == "y":
                    self.create(str(name))
                else:
                    employee = input(
                        "Please enter the employee you want to edit: "
                    ).title()

            create_table(3, employee)
            row_num = df[df["Employee"] == employee]
            row_num = row_num.index.tolist()
            for digit in row_num:
                digit = int(digit)
            value = input("Please select a value: ")

            while (
                value != "h"
                and value != "p"
                and value != "po"
                and value != "hr"
                and value != "b"
            ):
                print("Whoops, I didnt quite catch that! Please try again")
                create_table(3, employee)
                value = input("Please select a value: ")

            if value == "h":
                print(f"{employee} has worked {df.iloc[digit]['Hours']} hours")
                val = input("Whats the new value? ")
                try:
                    val = int(val)
                except ValueError:
                    print("Sorry, I didnt quite get that! Please try again")
                    self.edit(name)
                df.loc[digit, "Hours"] = val

            elif value == "p":
                print(f"{employee} works for {df.iloc[digit]['Pay']} per hour ")
                val = input("Whats the new value? ")
                try:
                    val = int(val)
                except ValueError:
                    print("Sorry, I didnt quite get that! Please try again")
                    self.edit(name)
                df.loc[digit, "Pay"] = val

            elif value == "po":
                print(f"{employee} works as {df.iloc[digit]['Position']} ")
                val = input("Whats the new value? ")
                df.loc[digit, "Position"] = val

            elif value == "hr":
                print(
                    f"{employee} has to work {df.iloc[digit]['Hours_required']} hours per week "
                )
                val = input("Whats the new value? ")
                try:
                    val = int(val)
                except ValueError:
                    print("Sorry, I didnt quite get that! Please try again")
                    self.edit(name)
                df.loc[digit, "Hours_required"] = val

            elif value == "b":
                main()
            df.to_csv(name, index=False)
            print("Value Updated Sucessfully")
            time.sleep(1)
            self.edit(name)

        def log(self, name):
            df = pd.read_csv(name)
            employee = input(
                "Please enter the employee you want to log hours for: "
            ).title()
            while employee not in df.values:
                y = input(
                    "That employee does not exist would you like to create one?, type y for yes: "
                ).lower()
                while y != "y" and y != "n":
                    print("Please try again")
                    y = input(
                        "That employee does not exist would you like to create one?, type y for yes: "
                    ).lower()
                if y == "y":
                    self.create(str(name))
                else:
                    employee = input(
                        "Please enter the employee you want to log hours for: "
                    ).title()
            row_num = df[df["Employee"] == employee]
            row_num = row_num.index.tolist()
            for digit in row_num:
                digit = int(digit)
            n = input(f"How many hours would you like to log for {employee}: ")
            try:
                n = int(n)
            except ValueError:
                self.log()

            df.loc[digit, "Hours"] = int(df.loc[digit, "Hours"]) + n
            df.to_csv(name, index=False)
            print("Value Updated Sucessfully")
            time.sleep(1)
            print(f"{employee} has now worked {df.iloc[digit]['Hours']} hours")

        def interest_rate(self, name):
            api_url = "https://api.api-ninjas.com/v1/interestrate?country=england?central-bank-only=True"
            response = requests.get(
                api_url,
                headers={"X-Api-Key": "BZqW9NXc9mJRpQgzFInUKw==xX3PzDusXIw7V3De"},
            )
            b = response.json()
            rate = float((b["non_central_bank_rates"])[2]["rate_pct"])
            rate = rate / 100
            df = pd.read_csv(name)
            employee = input(
                "Please enter the employee whose pay you want to update: "
            ).title()

            while employee not in df.values:
                y = input(
                    "That employee does not exist would you like to create one?, type y for yes: "
                ).lower()
                while y != "y" and y != "n":
                    print("Please try again")
                    y = input(
                        "That employee does not exist would you like to create one?, type y for yes: "
                    ).lower()
                if y == "y":
                    self.create(str(name))
                else:
                    employee = input(
                        "Please enter the employee you want to log hours for: "
                    ).title()
            row_num = df[df["Employee"] == employee]
            row_num = row_num.index.tolist()
            for digit in row_num:
                digit = int(digit)
            print(f"{employee} currently works for £{df.iloc[digit]['Pay']} per hour")
            year, month, day = df.at[digit, "last_ran"].split("-")
            year = int(year)
            month = int(month)
            day = int(day)
            timepassed = date.today() - date(year, month, day)
            timepassed = timepassed.days / 30
            df.loc[digit, "Pay"] = round(df.at[digit, "Pay"] * (rate**timepassed), 0)
            df.to_csv(name, index=False)
            print("Value Updated Sucessfully")
            time.sleep(1)
            print(f"{employee} now works for £{df.iloc[digit]['Pay']} per hour")
            main()

        def compare(self, name):
            df = pd.read_csv(name)
            hname = ""
            lname = ""
            l = 10000
            h = 0
            for i in range(len(df)):
                if (int(df.iloc[i]["Pay"]) * int(df.iloc[i]["Hours_required"])) > h:
                    h = int(df.iloc[i]["Pay"]) * int(df.iloc[i]["Hours_required"])
                    hname = str(df.iloc[i]["Employee"])
                if (int(df.iloc[i]["Pay"]) * int(df.iloc[i]["Hours_required"])) < l:
                    l = int(df.iloc[i]["Pay"]) * int(df.iloc[i]["Hours_required"])
                    lname = str(df.iloc[i]["Employee"])
            create_table(4)
            val = input("Please select a value")
            if val == "l":
                print(f"{lname} gets paid the lowest at £{l} per week")
            elif val == "h":
                print(f"{hname} gets paid the highest at £{h} per week")
            else:
                main()

            main()

        def compare1(self, name):
            df = pd.read_csv(name)
            hname = ""
            h = 0
            for i in range(len(df)):
                if (int(df.iloc[i]["Hours"]) - int(df.iloc[i]["Hours_required"])) > h:
                    h = int(df.iloc[i]["Hours"]) - int(df.iloc[i]["Hours_required"])
                    hname = str(df.iloc[i]["Employee"])
            print(f"{hname} is the best employee working {h} extra hours per week")
            time.sleep(2)
            main()

        def pay_raise(self, name):
            df = pd.read_csv(name)
            employee = input(
                "Please enter the employee who you want to give a pay raise to: "
            ).title()

            while employee not in df.values:
                y = input(
                    "That employee does not exist would you like to create one?, type y for yes: "
                ).lower()
                while y != "y" and y != "n":
                    print("Please try again")
                    y = input(
                        "That employee does not exist would you like to create one?, type y for yes: "
                    ).lower()
                if y == "y":
                    self.create(str(name))
                else:
                    employee = input(
                        "Please enter the employee you want to give a pay raise to: "
                    ).title()
            row_num = df[df["Employee"] == employee]
            row_num = row_num.index.tolist()
            for digit in row_num:
                digit = int(digit)

            rate = input(
                f"How much of a pay raise in percent do you want to give to {employee}? "
            )
            try:
                rate = rate.removesuffix("%")
                rate = int(rate)
            except ValueError:
                try:
                    int(rate)
                except ValueError:
                    self.pay_raise(name)

            df.loc[digit, "Pay"] = round(df.at[digit, "Pay"] * (1 + (rate / 100)), 0)
            df.to_csv(name, index=False)
            print("Value Updated Sucessfully")
            time.sleep(1)
            print(f"{employee} now works for £{df.iloc[digit]['Pay']} per hour")

        def list(self, name):
            df = pd.read_csv(name)
            print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
            time.sleep(3)
            main()

        def hours_reset(_, name):
            with open(name) as file:
                today = date.today()
                df = pd.read_csv(name)
                for i in range(len(df)):
                    year, month, day = df.at[i, "last_ran"].split("-")
                    year = int(year)
                    month = int(month)
                    day = int(day)
                    timepassed = date.today() - date(year, month, day)
                    timepassed = timepassed.days / 7
                    df.loc[i, "Hours_required"] = round(
                        df.at[i, "Hours_required"] * timepassed, 0
                    )
                    df.loc[i, "last_ran"] = today
                df.to_csv(name, index=False)

    def __init__(self, user):
        self.name = user + ".csv"
        self.employee = self.Employee()

        try:
            file = open(self.name)
            file.close()
        except FileNotFoundError:
            onboarding(user)

    def nominal(self, user_input):
        if user_input == "e":
            self.employee.edit(str(self.name))
        elif user_input == "c":
            self.employee.create(str(self.name))
        elif user_input == "b":
            sys.exit("Thanks for using our EMS")
        elif user_input == "l":
            self.employee.log(str(self.name))
        elif user_input == "i":
            self.employee.interest_rate(str(self.name))
        elif user_input == "m":
            self.employee.compare(str(self.name))
        elif user_input == "h":
            self.employee.compare1(str(self.name))
        elif user_input == "p":
            self.employee.pay_raise(str(self.name))
        elif user_input == "o":
            self.employee.list(str(self.name))


def main():
    create_table(1)
    user = User(input("Username: "))
    user_input(user)


def user_input(user):
    create_table(2)
    user_input = input("Please choose an option: ").lower()
    while (
        user_input != "c"
        and user_input != "e"
        and user_input != "b"
        and user_input != "l"
        and user_input != "i"
        and user_input != "m"
        and user_input != "h"
        and user_input != "p"
        and user_input != "o"
    ):
        user_input = input("Please choose an option: ").lower()

    user.nominal(user_input)
    return 200


def create_table(n, employee=""):
    table = PrettyTable()
    table.set_style(DOUBLE_BORDER)
    table.field_names = ["Key", "Action"]
    if n == 1:
        table.add_row(
            ["Username", "Opens up your profile or creates one if not present"]
        )
    if n == 2:
        table.add_row(["c", "Creates a new employee in your user account"])
        table.add_row(
            [
                "e",
                "Edits an existing employee",
            ]
        )
        table.add_row(["l", "logs a certain number of hours for an employee"])
        table.add_row(
            ["i", "calculates pay with current interest rates for any employee"]
        )
        table.add_row(
            [
                "m",
                "Calculates highest or lowest paid employee based on hours required and pay per hour",
            ]
        )
        table.add_row(["h", "prints best performing employee"])
        table.add_row(["p", "gives a pay raise in precent to an employee"])
        table.add_row(["o", "lists all employees and their values"])
        table.add_row(["b", "exits"])
    if n == 3:
        table.add_row(["h", f"Edits the number of hours {employee} has worked"])
        table.add_row(["p", f"Edits the pay per hour for {employee}"])
        table.add_row(["po", f"Edits {employee}'s position/role in the company"])
        table.add_row(
            [
                "hr",
                f"Edits the number of hours required for {employee} to work per week",
            ]
        )
        table.add_row(["l", "logs a certain number of hours for an employee"])
        table.add_row(["b", "returns to the previous menu"])

    if n == 4:
        table.add_row(["h", "prints highest paid employee"])
        table.add_row(["l", "prints lowest paid employee"])

    if n == 5:
        return 200
    print(table)



def onboarding(user):
    print("Welcome, your account has been added, please enter your username again")
    time.sleep(2)
    name = user + ".csv"
    with open(name, "w") as file:
        fieldnames = [
            "Employee",
            "Hours",
            "Pay",
            "Position",
            "Hours_required",
            "last_ran",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        main()

if __name__ == '__main__':
    main()
