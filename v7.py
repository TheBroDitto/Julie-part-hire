import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

orders_file = "orders.json"

def load_orders():
    if os.path.exists(orders_file):
        with open(orders_file, "r") as file:
            return json.load(file)
    return []

def save_orders():
    with open(orders_file, "w") as file:
        json.dump(orders, file)

def confirm_back_to_menu(hire_window_instance):
    if messagebox.askyesno("Confirmation", "Are you sure you want to go back to the menu?"):
        hire_window_instance.destroy()
        main_window.deiconify()  

def add_order():
    name = enter_name.get().strip()
    item = enter_item.get().strip()
    numofitem = enter_number_hired.get().strip()

    if validate_order(name, item, numofitem):
        receipt_number = random.randint(1000000, 9000000)
        orders.append((receipt_number, name, item, numofitem))
        enter_name.delete(0, 'end')
        enter_item.set('')
        enter_number_hired.delete(0, 'end')
        save_orders()
        messagebox.showinfo("Status", "Order added successfully")
        refresh_order_window()
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
    orders = [order for order in orders if order[0] != receipt_number]
    save_orders()
    messagebox.showinfo("Status", f"Order with receipt number {receipt_number} deleted")
    refresh_order_window()

def refresh_order_window():
    global print_order_window, tree  

    if print_order_window is None or not print_order_window.winfo_exists():
        display_orders()
    else:
        tree.delete(*tree.get_children())  
        for order_item in orders:
            tree.insert("", tk.END, values=order_item)
        lift_orders_window()  

def lift_orders_window():
    if print_order_window:
        print_order_window.lift()

def display_orders():
    
    global print_order_window, tree

    if print_order_window is not None and print_order_window.winfo_exists():
        print_order_window.destroy()

    print_order_window = tk.Toplevel(main_window)
    print_order_window.title("Orders")
    print_order_window.geometry("800x400")

    columns = ("Receipt Number", "Name", "Item Hired", "Number of Items Hired")

    tree = ttk.Treeview(print_order_window, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    for order_item in orders:
        tree.insert("", tk.END, values=order_item)

    tree.pack(fill=tk.BOTH, expand=True)

    def delete_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select an item to delete.")
            return
        receipt_number = tree.item(selected_item)['values'][0]
        
        if messagebox.askyesno("Confirmation", f"Are you sure you want to delete order with receipt number {receipt_number}?"):
            delete_order(receipt_number)

    tk.Button(print_order_window, text="Delete Selected", command=delete_selected).pack()
    tk.Button(print_order_window, text="Back to Menu", command=print_order_window.destroy).pack()

    lift_orders_window()  

def hire_window():
    main_window.withdraw()
    hire_window_instance = tk.Toplevel(main_window)
    hire_window_instance.title("Hire")
    hire_window_instance.geometry("400x165")

    tk.Label(hire_window_instance, text="Name").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_name
    enter_name = tk.Entry(hire_window_instance)
    enter_name.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(hire_window_instance, text="Item to hire").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item
    enter_item = ttk.Combobox(hire_window_instance, values=items)
    enter_item.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(hire_window_instance, text="Number of items hire").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired
    enter_number_hired = tk.Entry(hire_window_instance)
    enter_number_hired.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(hire_window_instance, text="Order", command=add_order).grid(column=1, row=3, padx=10, pady=5, sticky='w')
    tk.Button(hire_window_instance, text="Print Orders", command=display_orders).grid(column=1, row=4, padx=10, pady=5, sticky='w')
    tk.Button(hire_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(hire_window_instance)).grid(column=2, row=4, padx=10, pady=5, sticky='w')

    hire_window_instance.lift()

def quit_program():
    if messagebox.askyesno("Confirmation", "Are you sure you want to quit?"):
        main_window.destroy()

# Load orders from file
orders = load_orders()

# Main Window
main_window = tk.Tk()
main_window.title("Party Hire Menu")
main_window.geometry("200x200")

print_order_window = None
tree = None

tk.Button(main_window, text="Hire", command=hire_window).grid(column=0, row=0, padx=10, pady=5, sticky='w')
tk.Button(main_window, text="Check Orders", command=display_orders).grid(column=0, row=1, padx=10, pady=5, sticky='w')
tk.Button(main_window, text="Return", command=hire_window).grid(column=0, row=2, padx=10, pady=5, sticky='w')
tk.Button(main_window, text="Quit", command=quit_program).grid(column=0, row=3, padx=10, pady=5, sticky='w')

main_window.mainloop()
