import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
import random
import json
import os

# File paths
hire_orders_file = "hire_orders.json"
return_orders_file = "return_orders.json"

# Global variables
randomList = []
hire_orders = []
return_orders = []
print_order_window = None
hire_window_instance = None
return_window_instance = None
messagebox_active = False  # To keep track if a messagebox is currently active

def load_orders(file):  
    """Load orders from a JSON file."""
    if os.path.exists(file):
        with open(file, "r") as f:
            orders = json.load(f)
            # Convert receipt numbers to integers
            for order in orders:
                order[0] = int(order[0])
            return orders
    return []

def save_orders(file, orders):
    """Save orders to a JSON file."""
    # Convert receipt numbers to strings 
    for order in orders:
        order[0] = str(order[0])
    with open(file, "w") as f:
        json.dump(orders, f)

def initialise_data():
    """Load hire and return orders."""
    global hire_orders, return_orders
    hire_orders = load_orders(hire_orders_file)
    return_orders = load_orders(return_orders_file)

def generate_unique_receipt_number():
    """Generate a unique receipt number."""
    while True:
        receipt_number = random.randint(1000000, 9000000)
        if receipt_number not in randomList:
            randomList.append(receipt_number)
            return receipt_number

def show_message(title, message, message_type="info"):
    """Show a message box and ensure it's modal."""
    global messagebox_active
    if messagebox_active:
        return
    messagebox_active = True
    if message_type == "info":
        messagebox.showinfo(title, message)
    elif message_type == "warning":
        messagebox.showwarning(title, message)
    elif message_type == "error":
        messagebox.showerror(title, message)
    messagebox_active = False

def validate_order(name, numofitem):
    """Validate the hire order input fields."""
    if not name.replace(' ', '').isalpha():
        show_message("Warning", "Name can only contain letters", "warning")
        return False
    if not numofitem.isdigit() or not (1 <= int(numofitem) <= 500):
        show_message("Warning", "Number of items to be hired can only go up to 500", "warning")
        return False
    return True

def validate_return_order(receipt_number, numofitem):
    """Validate the return order input fields."""
    if not numofitem.isdigit() or not (1 <= int(numofitem) <= 500):
        show_message("Warning", "Number of items that can be returned is up to 500 items", "warning")
        return False
    if not any(order[0] == int(receipt_number) for order in hire_orders):
        show_message("Warning", "Receipt number does not exist", "warning")
        return False
    return True

def add_hire_order():
    """Add a new hire order."""
    if messagebox_active:
        return  # Prevent further action while a message box is active

    name = enter_name.get().strip()
    numofitem = enter_number_hired.get().strip()

    if validate_order(name, numofitem):
        receipt_number = generate_unique_receipt_number()
        item = enter_item.get().strip()
        hire_orders.append([receipt_number, name, item, numofitem])
        enter_name.delete(0, 'end')
        enter_item.set('')
        enter_number_hired.delete(0, 'end')
        save_orders(hire_orders_file, hire_orders)
        show_message("Status", "Hire order added successfully", "info")
        refresh_order_window()
    else:
        show_message("Warning", "Please fill out all fields correctly", "warning")

def add_return_order():
    """Add a new return order."""
    if messagebox_active:
        return  

    receipt_number = enter_receipt_number.get().strip()
    numofitem = enter_number_hired_return.get().strip()

    if validate_return_order(receipt_number, numofitem):
        item = enter_item_return.get().strip() 
        return_orders.append([receipt_number, item, numofitem])
        update_hire_order(receipt_number, item, numofitem)
        enter_receipt_number.set('')
        enter_item_return.set('')
        enter_number_hired_return.delete(0, 'end')
        save_orders(return_orders_file, return_orders)
        show_message("Status", "Return order added successfully", "info")
        refresh_order_window()
    else:
        show_message("Warning", "Please fill out all fields correctly", "warning")

def update_hire_order(receipt_number, item, numofitem):
    """Update the hire order when items are returned."""
    global hire_orders
    for order in hire_orders:
        if order[0] == int(receipt_number) and order[2] == item:
            remaining_items = int(order[3]) - int(numofitem)
            if remaining_items < 0:
                show_message("Error", "Cannot return more than ordered", "error")
                return
            if remaining_items > 0:
                hire_orders[hire_orders.index(order)] = [order[0], order[1], order[2], str(remaining_items)]
            else:
                hire_orders.remove(order)
            save_orders(hire_orders_file, hire_orders)
            break

def delete_order(receipt_number, order_list):
    """Delete an order from the specified list."""
    global hire_orders, return_orders
    receipt_number = int(receipt_number)  # Ensure receipt number is an integer
    if order_list == "hire":
        hire_orders[:] = [order for order in hire_orders if order[0] != receipt_number]
        save_orders(hire_orders_file, hire_orders)
    elif order_list == "return":
        return_orders[:] = [order for order in return_orders if int(order[0]) != receipt_number]  # Convert to int for comparison
        save_orders(return_orders_file, return_orders)
    show_message("Status", f"Order with receipt number {receipt_number} deleted", "info")
    refresh_order_window()

def refresh_order_window():
    """Refresh the orders window."""
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
    """Display the orders in a new window."""
    global print_order_window, hire_tree, return_tree

    if print_order_window is not None and print_order_window.winfo_exists():
        print_order_window.destroy()

    print_order_window = tk.Toplevel(main_window)
    print_order_window.title("Orders")
    print_order_window.geometry("900x900")
    print_order_window.configure(background="#caf0f8")

    hire_columns = ("Receipt Number", "Name", "Item", "Number of Items Hired")
    return_columns = ("Receipt Number", "Name", "Item", "Number of Items Returned")

    tk.Label(print_order_window, text="Hire Orders", bg="#caf0f8", font=("Comic Sans", 13)).pack(pady=10)
    hire_tree = ttk.Treeview(print_order_window, columns=hire_columns, show="headings", height=10)

    for col in hire_columns:
        hire_tree.heading(col, text=col)
        hire_tree.column(col, width=150, anchor='center')

    for order_item in hire_orders:
        hire_tree.insert("", tk.END, values=order_item)

    hire_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(print_order_window, text="Return Orders", bg="#caf0f8", font=("Helvetica", 10)).pack(pady=10)
    return_tree = ttk.Treeview(print_order_window, columns=return_columns, show="headings", height=10)

    for col in return_columns:
        return_tree.heading(col, text=col)
        return_tree.column(col, width=150, anchor='center')

    for order_item in return_orders:
        return_tree.insert("", tk.END, values=order_item)

    return_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure("Treeview", rowheight=25, fieldbackground="#caf0f8")

    def delete_selected(tree, order_list):
        """Delete the selected item from the tree."""
        selected_item = tree.selection()
        if not selected_item:
            show_message("Error", "Please select an item to delete.", "error")
            return
        receipt_number = tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Confirmation", f"Are you sure you want to delete order with receipt number {receipt_number}?"):
            delete_order(receipt_number, order_list)
            print_order_window.attributes("-top", True)

    tk.Button(print_order_window, text='Delete Selected Hire Order', command=lambda: delete_selected(hire_tree, "hire"), bg="crimson").pack(side=tk.TOP, padx=10, pady=5)
    tk.Button(print_order_window, text='Delete Selected Return Order', command=lambda: delete_selected(return_tree, "return"), bg="crimson").pack(side=tk.TOP, padx=10, pady=5)
    tk.Button(print_order_window, text='Close', command=print_order_window.destroy, bg="gray").pack(side=tk.BOTTOM, padx=10, pady=5)

def hire_window(title_text, action_text):
    """Create and show the hire window."""
    def add_order_wrapper():
        add_hire_order()

    main_window.withdraw()

    global hire_window_instance
    hire_window_instance = tk.Toplevel(main_window)
    hire_window_instance.title(title_text)
    hire_window_instance.geometry("400x165")
    hire_window_instance.configure(background="#caf0f8")
    hire_window_instance.attributes("-topmost", True)

    tk.Label(hire_window_instance, text="Name", bg="#caf0f8").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_name
    enter_name = tk.Entry(hire_window_instance, bg="white")
    enter_name.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(hire_window_instance, text="Item to hire", bg="#caf0f8").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item
    enter_item = ttk.Combobox(hire_window_instance, values=items, state="readonly", width=17)
    enter_item.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(hire_window_instance, text="Number of items hired", bg="#caf0f8").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired
    enter_number_hired = tk.Entry(hire_window_instance, bg="white")
    enter_number_hired.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(hire_window_instance, text=action_text, command=add_order_wrapper).grid(column=1, row=3, padx=10, pady=10, sticky='e')
    tk.Button(hire_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(hire_window_instance)).grid(column=0, row=3, padx=10, pady=10, sticky='w')

def return_window(title_text, action_text):
    """Create and show the return order window."""
    def add_order_wrapper():
        add_return_order()

    main_window.withdraw()

    global return_window_instance
    return_window_instance = tk.Toplevel(main_window)
    return_window_instance.title(title_text)
    return_window_instance.geometry("400x165")
    return_window_instance.configure(background="#caf0f8")
    return_window_instance.attributes("-topmost", True)

    receipt_numbers = [order[0] for order in hire_orders]

    tk.Label(return_window_instance, text="Receipt Number", bg="#caf0f8").grid(column=0, row=0, padx=10, pady=5, sticky='e')
    global enter_receipt_number
    enter_receipt_number = ttk.Combobox(return_window_instance, values=receipt_numbers, state="readonly", width=17)
    enter_receipt_number.grid(column=1, row=0, padx=10, pady=5, sticky='w')

    items = ["balloons", "banners", "confetti"]
    tk.Label(return_window_instance, text="Item to return", bg="#caf0f8").grid(column=0, row=1, padx=10, pady=5, sticky='e')
    global enter_item_return
    enter_item_return = ttk.Combobox(return_window_instance, values=items, state="readonly", width=17)
    enter_item_return.grid(column=1, row=1, padx=10, pady=5, sticky='w')

    tk.Label(return_window_instance, text="Number of items to return", bg="#caf0f8").grid(column=0, row=2, padx=10, pady=5, sticky='e')
    global enter_number_hired_return
    enter_number_hired_return = tk.Entry(return_window_instance, bg="white")
    enter_number_hired_return.grid(column=1, row=2, padx=10, pady=5, sticky='w')

    tk.Button(return_window_instance, text=action_text, command=add_order_wrapper).grid(column=1, row=3, padx=10, pady=10, sticky='e')
    
    tk.Button(return_window_instance, text="Back to Menu", command=lambda: confirm_back_to_menu(return_window_instance)).grid(column=0, row=3, padx=10, pady=10, sticky='w')

def confirm_back_to_menu(window_instance):
    """Confirm if the user wants to go back to the menu."""
    if messagebox.askyesno("Confirmation", "Are you sure you want to go back to the menu?"):
        window_instance.destroy()
        main_window.deiconify()

def back_to_menu():
    """Go back to the main menu."""
    global print_order_window
    if print_order_window:
        print_order_window.destroy()
    main_window.deiconify()

# Main function to set up and run the application
initialise_data()
main_window = tk.Tk()
main_window.title("Party Hire Store")

# Load image and get its dimensions
image_path = "Juile.png"
back = PhotoImage(file=image_path)
image_width = back.width()
image_height = back.height()

# Set window size to image size
main_window.geometry(f"{image_width}x{image_height}")

my_label = Label(main_window, image=back)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Button(main_window, text="Hire", command=lambda: hire_window("Hire Items", "Add Hire Order"),width=17).grid(row=6, column=4, pady=10)
tk.Button(main_window, text="Return", command=lambda: return_window("Return Items", "Add Return Order"),width=17).grid(row=7, column=4, pady=10)
tk.Button(main_window, text="Print Orders", command=display_orders, width=17).grid(row=8, column=4, pady=10)
tk.Button(main_window, text="Exit", command=main_window.quit, width=17).grid(row=9, column=9, pady=10)

main_window.mainloop()
