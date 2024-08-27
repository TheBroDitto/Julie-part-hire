import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import random
import json
import os

# File paths
hire_orders_file = "hire_orders.json"
return_orders_file = "return_orders.json"

# Load orders from file
def load_orders(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

# Save orders to file
def save_orders(file, orders):
    with open(file, "w") as f:
        json.dump(orders, f)

# Load hire and return orders
hire_orders = load_orders(hire_orders_file)
return_orders = load_orders(return_orders_file)

def confirm_back_to_menu(window_instance):
    if messagebox.askyesno("Confirmation", "Are you sure you want to go back to the menu?"):
        window_instance.destroy()
        main_window.deiconify()

def back_to_menu():
    global print_order_window
    if print_order_window:
        print_order_window.destroy()
    main_window.deiconify()

def add_hire_order():
    name = enter_name.get().strip()
    item = enter_item.get().strip()
    numofitem = enter_number_hired.get().strip()

    if validate_order(name, item, numofitem):
        receipt_number = random.randint(1000000, 9000000)
        hire_orders.append((receipt_number, name, item, numofitem))
        enter_name.delete(0, 'end')
        enter_item.set('')
        enter_number_hired.delete(0, 'end')
        save_orders(hire_orders_file, hire_orders)
        messagebox.showinfo("Status", "Hire order added successfully")
        refresh_order_window()
    else:
        messagebox.showwarning("Warning", "Please fill out all fields correctly")

def add_return_order():
    receipt_number = enter_receipt_number.get().strip()
    item = enter_item_return.get().strip()
    numofitem = enter_number_hired_return.get().strip()

    if validate_return_order(receipt_number, item, numofitem):
        return_orders.append((receipt_number, item, numofitem))
        enter_receipt_number.delete(0, 'end')
        enter_item_return.set('')
        enter_number_hired_return.delete(0, 'end')
        save_orders(return_orders_file, return_orders)
        messagebox.showinfo("Status", "Return order added successfully")
        refresh_order_window()
    else:
        messagebox.showwarning("Warning", "Please fill out all fields correctly")

def validate_order(name, item, numofitem):
    if not name.replace(' ', '').isalpha():
        messagebox.showwarning("Warning", "Name can only contain alphabets")
        return False
    if not numofitem.isdigit() or not (1 <= int(numofitem) <= 500):
        messagebox.showwarning("Warning", "Number of items that can be hired is up to 500 items")
        return False
    return True

def validate_return_order(receipt_number, item, numofitem):
    if not receipt_number.isdigit():
        messagebox.showwarning("Warning", "Receipt number must be a number")
        return False
    if not numofitem.isdigit() or not (1 <= int(numofitem) <= 500):
        messagebox.showwarning("Warning", "Number of items that can be returned is up to 500 items")
        return False
    return True

def delete_order(receipt_number, order_list, file_path):
    global hire_orders, return_orders
    if order_list == "hire":
        hire_orders = [order for order in hire_orders if order[0] != receipt_number]
        save_orders(hire_orders_file, hire_orders)
    else:
        return_orders = [order for order in return_orders if order[0] != receipt_number]
        save_orders(return_orders_file, return_orders)
    messagebox.showinfo("Status", f"Order with receipt number {receipt_number} deleted")
    refresh_order_window()

def refresh_order_window():
    global print_order_window, hire_tree, return_tree

    if print_order_window is None or not print_order_window.winfo_exists():
        display_orders()
    else:
        hire_tree.delete(*hire_tree.get_children())
        return_tree.delete(*return_tree.get_children())
        for order_item in hire_orders:
            hire_tree.insert("", tk.END, values=order_item)
        for order_item in return_orders:
            return_tree.insert("", tk.END, values=order_item)

def display_orders():
    global print_order_window, hire_tree, return_tree
    
    if hire_window_instance:
        hire_window_instance.destroy()
    if return_window_instance:
        return_window_instance.destroy()
    
    if print_order_window is not None and print_order_window.winfo_exists():
        print_order_window.destroy()

    print_order_window = tk.Toplevel(main_window)
    print_order_window.title("Orders")
    print_order_window.geometry("900x600")
    print_order_window.configure(background="#7bdff2")

    print_order_window.attributes("-top", True)

    hire_columns = ("Receipt Number", "Name", "Item", "Number of Items Hired")
    return_columns = ("Receipt Number", "Item", "Number of Items, Number of Items retuned")

    tk.Label(print_order_window, text="Hire Orders", bg="#7bdff2", font=("Helvetica", 16)).pack(pady=10)
    hire_tree = ttk.Treeview(print_order_window, columns=hire_columns, show="headings", height=10)
    
    for col in hire_columns:
        hire_tree.heading(col, text=col)
        hire_tree.column(col, width=100, anchor='center')
    
    for order_item in hire_orders:
        hire_tree.insert("", tk.END, values=order_item)
    
    hire_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(print_order_window, text="Return Orders", bg="#7bdff2", font=("Helvetica", 10)).pack(pady=10)
    return_tree = ttk.Treeview(print_order_window, columns=return_columns, show="headings", height=10)

    for col in return_columns:
        return_tree.heading(col, text=col)
        return_tree.column(col, width=100, anchor='center')

    for order_item in return_orders:
        return_tree.insert("", tk.END, values=order_item)

    return_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure("Treeview", background="#7bdff2", foreground="black", rowheight=25, fieldbackground="#7bdff2")
        
    def delete_selected(tree, order_list, file_path):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select an item to delete.")
            return
        receipt_number = tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Confirmation", f"Are you sure you want to delete order with receipt number {receipt_number}?"):
            delete_order(receipt_number, order_list, file_path)
            print_order_window.attributes("-topmost", True)

    tk.Button(print_order_window, text='Delete Selected Hire Order', compound=tk.LEFT, command=lambda: delete_selected(hire_tree, "hire", hire_orders_file), bg="crimson").pack(side=tk.TOP, padx=10, pady=5)
    tk.Button(print_order_window, text='Delete Selected Return Order', compound=tk.LEFT, command=lambda: delete_selected(return_tree, "return", return_orders_file), bg="crimson").pack(side=tk.TOP, padx=10, pady=5)
    tk.Button(print_order_window, text="Back to Menu", command=back_to_menu).pack()

def hire_window(title_text, action_text):
    def add_order_wrapper():
        add_hire_order()

    main_window.withdraw()
    
    global hire_window_instance
    hire_window_instance = tk.Toplevel(main_window)
    hire_window_instance.title(title_text)
    hire_window_instance.geometry("400x165")
    hire_window_instance.configure(background="#7bdff2")
    hire_window_instance.attributes("-topmost", True)

    tk.Label(hire_window_instance, text="Name", bg="#7bdff2").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_name
    enter_name = tk.Entry(hire_window_instance, bg="white")
    enter_name.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(hire_window_instance, text="Item to hire", bg="#7bdff2").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item
    enter_item = ttk.Combobox(hire_window_instance, values=items, width=17)
    enter_item.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(hire_window_instance, text="Number of items hire", bg="#7bdff2").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired
    enter_number_hired = tk.Entry(hire_window_instance, bg="white")
    enter_number_hired.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(hire_window_instance, text=action_text, command=add_order_wrapper).grid(column=1, row=3, padx=10, pady=10, sticky='e')
    tk.Button(hire_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(hire_window_instance)).grid(column=0, row=3, padx=10, pady=10, sticky='w')

def return_window(title_text, action_text):
    def add_order_wrapper():
        add_return_order()

    main_window.withdraw()
    
    global return_window_instance
    return_window_instance = tk.Toplevel(main_window)
    return_window_instance.title(title_text)
    return_window_instance.geometry("400x165")
    return_window_instance.configure(background="#7bdff2")
    return_window_instance.attributes("-topmost", True)

    receipt_numbers = [order[0] for order in hire_orders]

    tk.Label(return_window_instance, text="Receipt Number", bg="#7bdff2").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_receipt_number
    enter_receipt_number = ttk.Combobox(return_window_instance, values=receipt_numbers, width=17)
    enter_receipt_number.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(return_window_instance, text="Item to return", bg="#7bdff2").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item_return
    enter_item_return = ttk.Combobox(return_window_instance, values=items, width=17)
    enter_item_return.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(return_window_instance, text="Number of items to return", bg="#7bdff2").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired_return
    enter_number_hired_return = tk.Entry(return_window_instance, bg="white")
    enter_number_hired_return.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(return_window_instance, text=action_text, command=add_order_wrapper).grid(column=1, row=3, padx=10, pady=10, sticky='e')
    tk.Button(return_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(return_window_instance)).grid(column=0, row=3, padx=10, pady=10, sticky='w')

main_window = tk.Tk()
main_window.title("Party Hire Store")
main_window.geometry("800x600")
main_window.configure(background="#7bdff2")

print_order_window = None
hire_window_instance = None
return_window_instance = None

tk.Label(main_window, text="Party Hire Store", bg="#7bdff2", font=("Helvetica", 24)).pack(pady=20)

tk.Button(main_window, text="Hire", command=lambda: hire_window("Hire Items", "Add Hire Order")).pack(pady=10)
tk.Button(main_window, text="Return", command=lambda: return_window("Return Items", "Add Return Order")).pack(pady=10)
tk.Button(main_window, text="Print Orders", command=display_orders).pack(pady=10)
tk.Button(main_window, text="Exit", command=main_window.quit).pack(pady=10)

main_window.mainloop()
