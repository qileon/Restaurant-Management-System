import tkinter as tk  # import the tkinter module for creating GUI applications
from tkinter import ttk  # import ttk module, which provides themed widget set
from tkinter.messagebox import showerror  # import showerror for displaying error messages

class MenuItem:
    def __init__(self, name, price, category):
        self.name = name  # name of the menu item
        self.price = price  # price of the menu item
        self.category = category  # category of the menu item (e.g., food, drinks)

class Order:
    def __init__(self):
        self.items = []  # list to store ordered items
        self.total = 0  # total price of the order

    def add_item(self, item):
        self.items.append(item)  # add item to the order
        self.total += item.price  # increment total price by item price

    def remove_item(self, item):
        self.items.remove(item)  # remove item from the order
        self.total -= item.price  # decrement total price by item price

    def display_order(self):
        order_text = "Order Details:\n"  # start with a header
        for item in self.items:
            order_text += f"- {item.name}: ${item.price:.2f}\n"  # display each item with its price
        order_text += f"Total: ${self.total:.2f}"  # display total price
        return order_text  # return the formatted order details

    def copy(self):
        new_order = Order()  # create a new order object
        new_order.items = self.items.copy()  # copy items list
        new_order.total = self.total  # copy total price
        return new_order  # return the new order object

class Restaurant:
    def __init__(self, root):
        self.root = root  # store reference to the root window
        self.menu = []  # list to store menu items
        self.orders = []  # list to store placed orders
        self.previous_orders = []  # list to store previous orders for undo functionality
        self.current_category = "Food"  # initialize current category to food
        self.current_order = Order()  # initialize current_order to an empty order object

        # create a notebook widget to switch between food and drinks categories
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # create frames for food and drinks categories
        self.food_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.food_frame, text="Food")

        # create a frame for drinks tab in notebook
        self.drink_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.drink_frame, text="Drinks")

        # create a label frame for food menu
        self.food_menu_frame = ttk.LabelFrame(self.food_frame, text="Menu")
        self.food_menu_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # create a label frame for drink menu
        self.drink_menu_frame = ttk.LabelFrame(self.drink_frame, text="Menu")
        self.drink_menu_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # create a canvas for food menu
        self.food_menu_canvas = tk.Canvas(self.food_menu_frame)
        self.food_menu_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        # create a canvas for drink menu
        self.drink_menu_canvas = tk.Canvas(self.drink_menu_frame)
        self.drink_menu_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        # create a scrollbar for food menu
        self.food_menu_scrollbar = ttk.Scrollbar(self.food_menu_frame, orient=tk.VERTICAL, command=self.food_menu_canvas.yview)
        self.food_menu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # create a scrollbar for drink menu
        self.drink_menu_scrollbar = ttk.Scrollbar(self.drink_menu_frame, orient=tk.VERTICAL, command=self.drink_menu_canvas.yview)
        self.drink_menu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure scrollbar for food menu canvas
        self.food_menu_canvas.configure(yscrollcommand=self.food_menu_scrollbar.set)
        self.food_menu_canvas.bind('<Configure>', lambda e: self.food_menu_canvas.configure(scrollregion=self.food_menu_canvas.bbox("all")))

        # configure scrollbar for drink menu canvas
        self.drink_menu_canvas.configure(yscrollcommand=self.drink_menu_scrollbar.set)
        self.drink_menu_canvas.bind('<Configure>', lambda e: self.drink_menu_canvas.configure(scrollregion=self.drink_menu_canvas.bbox("all")))

        # create a frame inside food menu canvas
        self.food_menu_frame_inside = tk.Frame(self.food_menu_canvas)
        self.food_menu_canvas.create_window((0, 0), window=self.food_menu_frame_inside, anchor="nw")

        # create a frame inside drink menu canvas
        self.drink_menu_frame_inside = tk.Frame(self.drink_menu_canvas)
        self.drink_menu_canvas.create_window((0, 0), window=self.drink_menu_frame_inside, anchor="nw")

        # create a label frame for order
        self.order_frame = ttk.LabelFrame(root, text="Order")
        self.order_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # create a text widget for displaying order
        self.order_text = tk.Text(self.order_frame, height=10, width=30)
        self.order_text.pack(pady=5)

        # create an entry widget for adding items to order
        self.add_item_entry = ttk.Entry(self.order_frame)
        self.add_item_entry.pack(pady=5)

        # create a button for adding items to order
        self.add_item_button = ttk.Button(self.order_frame, text="Add Item", command=self.add_item_to_order)
        self.add_item_button.pack(pady=5)

        # create a button for placing order
        self.place_order_button = ttk.Button(self.order_frame, text="Place Order", command=self.place_order)
        self.place_order_button.pack(pady=5)

        # create a button for removing item from order
        self.remove_item_button = ttk.Button(self.order_frame, text="Remove Item", command=self.remove_item_from_order)
        self.remove_item_button.pack(pady=5)

        # bind event to update menu display when notebook tab changes
        self.notebook.bind("<<NotebookTabChanged>>", self.update_menu_display)

    # function to add menu item with name, price, and category
    def add_menu_item(self, name, price, category):
        item = MenuItem(name, price, category)  # create a new MenuItem object
        self.menu.append(item)  # add the item to the menu list

    # function to add item to order
    def add_item_to_order(self, item=None):
        # add provided item to order if exists, otherwise add item from entry widget
        if item:
            self.current_order.add_item(item)
            self.update_order_display()  # update the order display
            self.previous_orders.append(self.current_order.copy()) 
        else:
            item_number = self.add_item_entry.get()
            if item_number.isdigit() and 1 <= int(item_number) <= len(self.menu):
                item = self.menu[int(item_number) - 1]
                if item.category == self.current_category:
                    self.current_order.add_item(item)
                    self.update_order_display()
                    self.previous_orders.append(self.current_order.copy())
                else:
                    showerror("Error", "Item not found in the current category.")
            else:
                showerror("Error", "Invalid item number.")
            self.add_item_entry.delete(0, tk.END)  # clear the entry widget after adding item

    # function to place order
    def place_order(self):
        self.orders.append(self.current_order)  # add the current order to the list of orders
        self.current_order = Order()  # reset current_order to an empty Order object
        self.update_order_display()

    # function to update order display
    def update_order_display(self):
        self.order_text.delete("1.0", tk.END)  # clear the current order display
        self.order_text.insert(tk.END, self.current_order.display_order())  # display the current order

    # function to update menu display
    def update_menu_display(self, event=None):
        self.current_category = self.notebook.tab(self.notebook.select(), "text")

        # clear previous menu items
        for widget in self.food_menu_frame_inside.winfo_children():
            widget.destroy()

        for widget in self.drink_menu_frame_inside.winfo_children():
            widget.destroy()

        # display menu items according to the current category
        for i, item in enumerate(self.menu):
            if item.category == "Food":
                menu_item_label = ttk.Label(self.food_menu_frame_inside, text=f"{i + 1}. {item.name}: ${item.price:.2f}")
                menu_item_label.bind("<Button-1>", lambda event, item=item: self.add_item_to_order(item))
                menu_item_label.pack(fill="x", padx=5, pady=5)
            elif item.category == "Drinks":
                menu_item_label = ttk.Label(self.drink_menu_frame_inside, text=f"{i + 1}. {item.name}: ${item.price:.2f}")
                menu_item_label.bind("<Button-1>", lambda event, item=item: self.add_item_to_order(item))
                menu_item_label.pack(fill="x", padx=5, pady=5)
                
        # display ordered items
        for i, item in enumerate(self.current_order.items):
            order_item_label = ttk.Label(self.order_frame, text=f"{i + 1}. {item.name}: ${item.price:.2f}")
            order_item_label.pack(fill="x", padx=5, pady=5)

    # function to remove item from order
    def remove_item_from_order(self, item=None):
        if item:
            self.current_order.remove_item(item)
            self.update_order_display()
            self.previous_orders.append(self.current_order.copy())
        else:
            item_number = self.add_item_entry.get()
            if item_number.isdigit() and 1 <= int(item_number) <= len(self.current_order.items):
                item = self.current_order.items[int(item_number) - 1]
                self.current_order.remove_item(item)
                self.update_order_display()
                self.previous_orders.append(self.current_order.copy())
            else:
                showerror("Error", "Invalid item number.")
            self.add_item_entry.delete(0, tk.END)

# create the main application window
root = tk.Tk()
root.title("Scriptum Pizza")  # set the title of the window

restaurant = Restaurant(root)  # create an instance of the Restaurant class

# add menu items to the restaurant
restaurant.add_menu_item("16' Medium Red Sauce", 18.00, "Food")
restaurant.add_menu_item("16' Medium White Sauce", 18.00, "Food")
restaurant.add_menu_item("16' Medium Pesto", 18.00, "Food")
restaurant.add_menu_item("18' Large Red Sauce", 21.00, "Food")
restaurant.add_menu_item("18' Large Pesto", 21.00, "Food")
restaurant.add_menu_item("18' Large White Sauce", 21.00, "Food")
restaurant.add_menu_item("Gluten Free Red Sauce", 18.95, "Food")
restaurant.add_menu_item("Gluten Free White Sauce", 18.95, "Food")
restaurant.add_menu_item("Gluten Free Pesto", 18.95, "Food")
restaurant.add_menu_item("16' Medium 1/2 Optional", 23.00, "Food")
restaurant.add_menu_item("18' Large 1/2 Optional", 26.00, "Food")
restaurant.add_menu_item("Slice Cheese Pizza", 3.85, "Food")
restaurant.add_menu_item("Slice Pepperoni Pizza", 4.25, "Food")
restaurant.add_menu_item("Slice of the Day", 4.60, "Food")

restaurant.add_menu_item("16 Oz Bottle Coke", 2.75, "Drinks")
restaurant.add_menu_item("16 Oz Bottle Diet Coke", 2.75, "Drinks")
restaurant.add_menu_item("Fanta Grape", 2.95, "Drinks")
restaurant.add_menu_item("Fanta Orange", 3.50, "Drinks")
restaurant.add_menu_item("Bottle Sprite", 2.75, "Drinks")
restaurant.add_menu_item("Bottled Water", 2.25, "Drinks")
restaurant.add_menu_item("Sparkling Water", 3.50, "Drinks")
restaurant.add_menu_item("Iced Tea", 2.95, "Drinks")
restaurant.add_menu_item("Lemonade", 3.50, "Drinks")

restaurant.update_order_display()  # update the order display with the initial state

root.mainloop()  # start the main event loop for the application