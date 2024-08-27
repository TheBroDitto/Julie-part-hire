import tkinter as tk
from tkinter import ttk, messagebox
import random

orders = []

def confirm_back_to_menu(hire_window_instance):
    if messagebox.askyesno("Confirmation", "Are you sure you want to go back to the menu?"):
        hire_window_instance.destroy()
        main_window.deiconify()  

def quit_menu():
    if messagebox.askyesno("Confirmation", "Are you sure you want to quit?"):
        main_window.destroy()

def confirm_display_order_back(display_orders):
    if messagebox.askyesno("Confirmation", "Are you sure you want to go back to the menu?"):
        main_window.deiconify()

def add_order():
    name = enter_name.get().strip()
    item = enter_item.get().strip()
    numofitem = enter_number_hired.get().strip()

    if validate_order(name, item, numofitem):
        receipt_number = random.randint(1000000, 9000000)
        orders.append((name, item, numofitem, receipt_number))
        enter_name.delete(0, 'end')
        enter_item.set('')
        enter_number_hired.delete(0, 'end')
        messagebox.showinfo("Status", "Order added successfully")
    else:
        messagebox.showwarning("Warning", "Please fill out all fields correctly")

def validate_order(name, item, numofitem):
    if not name.replace(' ','').isalpha():
        messagebox.showwarning("Warning", "Name can only contain alphabets")
        return False
    if not numofitem.isdigit() or not (1 <= int(numofitem) <= 500):
        messagebox.showwarning("Warning", "Number of items that can be hired is up to 500 items")
        return False
    return True

def delete_order(receipt_number):
    global orders
    orders = [order for order in orders if order[3] != receipt_number]
    messagebox.showinfo("Status", f"Order with receipt number {receipt_number} deleted")
    refresh_order_window()

def refresh_order_window():
    for widget in print_order_window.winfo_children():
        widget.destroy()
    display_orders()

def display_orders():
    tk.Label(print_order_window, font='bold', text="Receipt Number").grid(column=0, row=1)
    tk.Label(print_order_window, font='bold', text="Name").grid(column=1, row=1)
    tk.Label(print_order_window, font='bold', text="Item to hire").grid(column=2, row=1)
    tk.Label(print_order_window, font='bold', text="Number of items hired").grid(column=3, row=1)
    tk.Label(print_order_window, font='bold', text="Delete order").grid(column=4, row=1)
    tk.Label(print_order_window, font='bold', text="Back to menu").grid(column=5, row=1)
    

    for i, order_item in enumerate(orders, start=2):
        tk.Label(print_order_window, text=order_item[3]).grid(column=0, row=i)  
        tk.Label(print_order_window, text=order_item[0]).grid(column=1, row=i)
        tk.Label(print_order_window, text=order_item[1]).grid(column=2, row=i)
        tk.Label(print_order_window, text=order_item[2]).grid(column=3, row=i)
        tk.Button(print_order_window, text="Delete", command=lambda rn=order_item[3]: delete_order(rn)).grid(column=4, row=i)
        tk.Button(print_order_window, text="Back to Menu", command=lambda: confirm_display_order_back(display_orders)).grid(column=5, row=i)


def print_order():
    global print_order_window
    print_order_window = tk.Toplevel(main_window)
    print_order_window.title("Orders")
    print_order_window.geometry("425x200")
    display_orders()

def hire_window():
    main_window.withdraw()  
    hire_window_instance = tk.Toplevel(main_window)
    hire_window_instance.title("Hire")
    hire_window_instance.geometry("380x165")

    tk.Label(hire_window_instance, text="Name").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_name
    enter_name = tk.Entry(hire_window_instance)
    enter_name.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(hire_window_instance, text="Item to hire").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item
    enter_item = ttk.Combobox(hire_window_instance, values=items)
    enter_item.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(hire_window_instance, text="Number to hire").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired
    enter_number_hired = tk.Entry(hire_window_instance)
    enter_number_hired.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(hire_window_instance, text="Order", command=add_order).grid(column=1, row=3, padx=10, pady=5, sticky='w')
    tk.Button(hire_window_instance, text="Print Orders", command=print_order).grid(column=1, row=4, padx=10, pady=5, sticky='w')
    tk.Button(hire_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(hire_window_instance)).grid(column=2, row=4, padx=10, pady=5, sticky='w')

def return_window():
    main_window.withdraw()  # Hide the main window
    hire_window_instance = tk.Toplevel(main_window)
    hire_window_instance.title("Return")
    hire_window_instance.geometry("380x165")

    tk.Label(hire_window_instance, text="Name").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_name
    enter_name = tk.Entry(hire_window_instance)
    enter_name.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(hire_window_instance, text="Item to hire").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item
    enter_item = ttk.Combobox(hire_window_instance, values=items)
    enter_item.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(hire_window_instance, text="Number to hire").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired
    enter_number_hired = tk.Entry(hire_window_instance)
    enter_number_hired.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(hire_window_instance, text="Order", command=add_order).grid(column=1, row=3, padx=10, pady=5, sticky='w')
    tk.Button(hire_window_instance, text="Print Orders", command=print_order).grid(column=1, row=4, padx=10, pady=5, sticky='w')
    tk.Button(hire_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(hire_window_instance)).grid(column=2, row=4, padx=10, pady=5, sticky='w')

def quit_program():
    if messagebox.askyesno("Confirmation", "Are you sure you want to quit?"):
        main_window.destroy()

# Main Window
main_window = tk.Tk()
main_window.title("Party Hire Menu")
main_window.geometry("125x145")

# Spacing out buttons vertically
tk.Button(main_window, text="Hire", command=hire_window).grid(column=0, row=0, padx=10, pady=5, sticky='w')
tk.Button(main_window, text="Return", command=return_window).grid(column=0, row=1, padx=10, pady=5, sticky='w')
tk.Button(main_window, text="Check Orders", command=print_order).grid(column=0, row=2, padx=10, pady=5, sticky='w')
tk.Button(main_window, text="Quit", command=quit_program).grid(column=0, row=3, padx=10, pady=5, sticky='w')

main_window.mainloop()
