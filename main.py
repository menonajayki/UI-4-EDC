import websocket
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import sys
from PIL import Image, ImageTk

def on_message(ws, message):
    print("Received acknowledgment:", json.loads(message))


def on_error(ws, error):
    print("WebSocket error:", error)
    messagebox.showerror("WebSocket Error", str(error))

def on_close(ws):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection established")

def place_order():
    selected_product = product_var.get()
    product_details = {
        "Truck Red 01": {
            "quantity": 10,
            "price": 25.99,
            "color": "Red",
            "size": "Large"
        },
        "Truck Green 02": {
            "quantity": 8,
            "price": 29.99,
            "color": "Green",
            "size": "Medium"
        },
        "Truck Yellow 03": {
            "quantity": 12,
            "price": 22.99,
            "color": "Yellow",
            "size": "Small"
        }
    }

    if selected_product in product_details:
        product_data = product_details[selected_product]

        request_data = {
            "product_name": selected_product,
            "quantity": product_data["quantity"],
            "price": product_data["price"],
            "color": product_data["color"],
            "size": product_data["size"]
        }

        if ws.sock and ws.sock.connected:
            ws.send(json.dumps(request_data))
            messagebox.showinfo("Order Placed", "Your order has been placed successfully!")
        else:
            messagebox.showerror("Error", "WebSocket connection is not open")
            messagebox.showinfo("Order Placed", "Error!")

        product_var.set("Select Product")

def clear_fields():
    product_var.set("Select Product")

def run_websocket():
    ws.run_forever()

def on_closing():
    if ws.sock and ws.sock.connected:
        ws.close()
    root.destroy()
    sys.exit()

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/orders/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    root = tk.Tk()
    root.title("UI 4 EDC")

    icon_path = "favicon.ico"
    root.iconbitmap(default=icon_path)

    primary_color = "#336699"
    secondary_color = "#FFD700"
    text_color = "black"
    background_color = "#f0f0f0"
    root.configure(background=background_color)

    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Primary.TButton", background=primary_color, foreground=text_color)
    style.configure("Secondary.TButton", background=secondary_color, foreground=text_color)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    logo_image = Image.open("logo.png")
    logo_photo = ImageTk.PhotoImage(logo_image)
    interface_label = ttk.Label(root, image=logo_photo)
    interface_label.image = logo_photo  # Keep a reference to the image
    interface_label.pack(pady=20)

    products = ["Truck Red 01", "Truck Green 02", "Truck Yellow 03"]
    product_var = tk.StringVar(root)
    product_var.set("Select Product")
    product_label = ttk.Label(root, text="Please select the product:", background=background_color, foreground=text_color)
    product_label.pack()

    product_menu = ttk.Combobox(root, textvariable=product_var, values=products, state="readonly", width=30)
    product_menu.pack()

    place_order_button = ttk.Button(root, text="Place Order", style="Primary.TButton", command=place_order)
    place_order_button.pack(pady=20)

    clear_fields_button = ttk.Button(root, text="Clear Fields", style="Secondary.TButton", command=clear_fields)
    clear_fields_button.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
