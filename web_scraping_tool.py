import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data
def scrape_data():
    url = url_entry.get()
    item_selector = item_entry.get()
    title_selector = title_entry.get()
    price_selector = price_entry.get()
    
    if not url or not item_selector or not title_selector or not price_selector:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", f"Failed to retrieve the web page: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    data = []
    for item in soup.select(item_selector):
        title = item.select_one(title_selector).text.strip()
        price = item.select_one(price_selector).text.strip()
        data.append({'Title': title, 'Price': price})

    if not data:
        messagebox.showinfo("No Data", "No data found with the provided selectors.")
        return

    display_data(data)

def display_data(data):
    for widget in data_frame.winfo_children():
        widget.destroy()

    df = pd.DataFrame(data)
    text = tk.Text(data_frame, wrap='none')
    text.insert(tk.END, df.to_string(index=False))
    text.pack(expand=True, fill='both')

    save_button = tk.Button(data_frame, text="Save to CSV", command=lambda: save_to_csv(df))
    save_button.pack(pady=10)

def save_to_csv(df):
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Data has been saved to {file_path}")

# Create the main window
root = tk.Tk()
root.title("Web Scraping Tool")

# URL input
tk.Label(root, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Item selector input
tk.Label(root, text="Item Selector:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
item_entry = tk.Entry(root, width=50)
item_entry.grid(row=1, column=1, padx=10, pady=5)

# Title selector input
tk.Label(root, text="Title Selector:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=2, column=1, padx=10, pady=5)

# Price selector input
tk.Label(root, text="Price Selector:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
price_entry = tk.Entry(root, width=50)
price_entry.grid(row=3, column=1, padx=10, pady=5)

# Scrape button
scrape_button = tk.Button(root, text="Scrape Data", command=scrape_data)
scrape_button.grid(row=4, column=0, columnspan=2, pady=10)

# Frame to display data
data_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
data_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Make the data frame expandable
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the main event loop
root.mainloop()
