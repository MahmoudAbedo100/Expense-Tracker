import tkinter as tk
from tkinter import messagebox

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from expense import Expense
import calendar
import datetime
import csv

class ExpenseTracker:
    def __init__(self, window):
        self.window = window
        self.window.title("Expense Tracker")
        self.window.configure(background='lightgrey')

        # Create a button that will call the get_user_expense function when clicked
        self.button = tk.Button(self.window, text="Enter Expense", command=self.get_user_expense, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.button.pack()

        # Create a canvas for the pie chart
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.fig.patch.set_facecolor('lightgrey')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.canvas.get_tk_widget().pack()

    def get_user_expense(self):
        expense_name = input("Enter expense name: ")
        expense_amount = float(input("Enter expense amount: "))
        expense_categories = [
            "Food",
            "Home",
            "Work",
            "Fun",
            "Misc",
        ]

        while True:
            print("Select a category: ")
            for i, category_name in enumerate(expense_categories):
                print(f"  {i + 1}. {category_name}")

            value_range = f"[1 - {len(expense_categories)}]"
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(
                    name=expense_name, category=selected_category, amount=expense_amount
                )
                self.save_expense_to_file(new_expense, "expenses.csv")
                self.summarize_expenses("expenses.csv", 2000)
                return new_expense
            else:
                print("Invalid category. Please try again!")

    def save_expense_to_file(self, expense: Expense, expense_file_path):
        with open(expense_file_path, "a", encoding='utf-8') as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")

    def summarize_expenses(self, expense_file_path, budget):
        expenses: list[Expense] = []
        with open(expense_file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                )
                expenses.append(line_expense)

        amount_by_category = {}
        for expense in expenses:
            key = expense.category
            if key in amount_by_category:
                amount_by_category[key] += expense.amount
            else:
                amount_by_category[key] = expense.amount

        self.update_pie_chart(amount_by_category)

    def update_pie_chart(self, amount_by_category):
        # Clear the previous pie chart
        self.fig.clear()

        # Add a new subplot to the figure
        ax = self.fig.add_subplot(111)

        # Create the pie chart
        ax.pie(amount_by_category.values(), labels=amount_by_category.keys(), autopct='%1.1f%%')

        # Redraw the pie chart
        self.canvas.draw()

if __name__ == "__main__":
    window = tk.Tk()
    app = ExpenseTracker(window)
    window.mainloop()
