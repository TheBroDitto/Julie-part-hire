import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random

order = []
counters = {'total_entries': 0, 'name_count': 0}
ROWS_ABOVE = 6  # Define ROWS_ABOVE globally

def quit_program():
    confirm_window = tk.Toplevel(main_window)
    confirm_window.title("Confirmation")
    confirm_window.geometry("250x100")
    label = tk.Label(confirm_window, text="Are you sure you want to quit?")
    label.pack(pady=10)
    tk.Button(confirm_window, text="Quit", command=main_window.destroy).pack(side=tk.LEFT, padx=20)
    tk.Button(confirm_window, text="Cancel", command=confirm_window.destroy).pack(side=tk.RIGHT, padx=20)

def generate_random():
    global counters
    counters['total_entries'] += 1
    low_number = 1000000
    high_number = 9000000
    random_number = random.randint(low_number, high_number)
    label = tk.Label(hire_window_instance, text=random_number, width=12)
    label.grid(column=1, row=7, sticky=tk.E)

def intro():
    print("This is a party hire program")

def validate_first_name(first_name):
    return first_name.isalpha()

def validate_quantity(quantity):
    if quantity.isdigit():
        quantity = int(quantity)
        if 1 <= quantity <= 500:
            return True
    return False

def display_contents():
    first_name = entry_name.get()
    quantity = entry_quantity.get()

    if not validate_first_name(first_name):
        messagebox.showerror("Invalid Input", "First Name must contain only alphabets.")
        return

    if not validate_quantity(quantity):
        messagebox.showerror("Invalid Input", "Quantity must be a number between 1 and 500")
        return

    result_text.set(f"First Name: {first_name}, Quantity: {quantity}")

def print_order():
    print_order_window = tk.Toplevel(main_window)
    print_order_window.title("Orders")
    print_order_window.geometry("500x500")
    tk.Label(print_order_window, font='bold', text="Row").grid(column=0, row=6)
    tk.Label(print_order_window, font='bold', text="Name").grid(column=1, row=6)
    tk.Label(print_order_window, font='bold', text="Item to hire").grid(column=2, row=6)
    tk.Label(print_order_window, font='bold', text="Number of items hired").grid(column=3, row=6)
    tk.Label(print_order_window, font='bold', text="Receipt").grid(column=4, row=6)
    for i, order_item in enumerate(order, start=1):
        tk.Label(print_order_window, text=i).grid(column=0, row=i + ROWS_ABOVE)
        tk.Label(print_order_window, text=order_item[0]).grid(column=1, row=i + ROWS_ABOVE)
        tk.Label(print_order_window, text=order_item[1]).grid(column=2, row=i + ROWS_ABOVE)
        tk.Label(print_order_window, text=order_item[2]).grid(column=3, row=i + ROWS_ABOVE)

def add_order():
    global order, counters
    first_name = entry_name.get()
    quantity = entry_quantity.get()

    if not validate_first_name(first_name):
        messagebox.showerror("Invalid Input", "First Name must contain only alphabets.")
        return

    if not validate_quantity(quantity):
        messagebox.showerror("Invalid Input", "Quantity must be a number between 1 and 500")
        return

    if counters['name_count'] < counters['total_entries']:
        order.append([first_name, quantity, random.randint(1000, 9999)])
        counters['name_count'] += 1
    else:
        messagebox.showerror("Limit Exceeded", "All entries have been filled.")
        return

    entry_name.delete(0, 'end')
    entry_quantity.delete(0, 'end')

def hire_window():
    global hire_window_instance
    hire_window_instance = tk.Toplevel(main_window)
    hire_window_instance.title("Hire")
    hire_window_instance.geometry("750x200")
    tk.Label(hire_window_instance, text="Name").grid(column=0, row=2)
    tk.Label(hire_window_instance, text="Item Hired").grid(column=0, row=3)
    tk.Label(hire_window_instance, text="Quantity").grid(column=0, row=4)
    tk.Button(hire_window_instance, text="Quit", command=hire_window_instance.destroy, width=12).grid(column=30, row=30)
    tk.Button(hire_window_instance, text="Receipt number", command=generate_random, width=12).grid(column=7, row=7, sticky=tk.E)
    tk.Button(hire_window_instance, text="Print Orders", command=print_order, width=12).grid(column=4, row=7)
    tk.Button(hire_window_instance, text="Add Order", command=add_order, width=12).grid(column=3, row=7)
    tk.Button(hire_window_instance, text="Back", command=hire_window_instance.destroy, width=12).grid(column=30, row=29)
    tk.Label(hire_window_instance, text="").grid(column=0, row=1, sticky=tk.E)
    tk.Label(hire_window_instance, text="").grid(column=1, row=1, sticky=tk.E)

    global entry_name, entry_quantity, result_text
    entry_name = tk.Entry(hire_window_instance)
    entry_name.grid(column=1, row=2)
    entry_quantity = tk.Entry(hire_window_instance)
    entry_quantity.grid(column=1, row=3)
    result_text = tk.StringVar()
    tk.Label(hire_window_instance, textvariable=result_text).grid(column=0, row=5, columnspan=2)

def body():
    tk.Button(main_window, text="Hire", command=hire_window, width=12).grid(column=0, row=1)
    tk.Button(main_window, text="Return", command=None, width=12).grid(column=0, row=2)
    tk.Button(main_window, text="Quit", command=quit_program, width=12).grid(column=0, row=3)
    tk.Label(main_window, text="").grid(column=0, row=1, sticky=tk.E)
    tk.Label(main_window, text="").grid(column=1, row=1, sticky=tk.E)

def main():
    global main_window
    main_window = tk.Tk()
    
    main_window.title("Party Hire Menu")
    main_window.geometry("500x250")
    intro()
    body()
    main_window.mainloop()

main()
