import tkinter as tk
from tkinter import ttk
import threading
import time
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure as mplfig


# =========================
# EXE SAFE FOLDER
# =========================

def get_app_folder():

    import sys

    if getattr(sys, 'frozen', False):

        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))


APP_FOLDER = get_app_folder()

ORDERS_FILE = os.path.join(APP_FOLDER, "orders.json")


# =========================
# JSON FUNCTIONS
# =========================

def load_orders():

    if not os.path.exists(ORDERS_FILE):

        return []

    try:

        with open(ORDERS_FILE, "r") as f:

            return json.load(f)

    except:

        return []


def save_orders(data):

    with open(ORDERS_FILE, "w") as f:

        json.dump(data, f, indent=4)

    print("Saved:", data)


# =========================
# PSX SCRAPER
# =========================

def get_price(symbol):

    try:

        url = f"https://dps.psx.com.pk/company/{symbol}"

        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        labels = soup.find_all("div", class_="stats_label")
        values = soup.find_all("div", class_="stats_value")

        for label, value in zip(labels, values):

            if "Last" in label.text:

                price = value.text.replace("Rs.", "").replace(",", "").strip()

                return float(price)

        return None

    except Exception as e:

        print("Scrape error:", e)

        return None



# =========================
# ORDERS EDITOR
# =========================

class OrdersEditor:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        self.window.title("Edit Orders")

        self.window.geometry("500x400")


        input_frame = tk.Frame(self.window)

        input_frame.pack(pady=5)


        tk.Label(input_frame, text="Symbol").grid(row=0, column=0)

        tk.Label(input_frame, text="Shares").grid(row=0, column=1)

        tk.Label(input_frame, text="Buy Price").grid(row=0, column=2)


        self.symbol_entry = tk.Entry(input_frame)

        self.symbol_entry.grid(row=1, column=0)


        self.shares_entry = tk.Entry(input_frame)

        self.shares_entry.grid(row=1, column=1)


        self.price_entry = tk.Entry(input_frame)

        self.price_entry.grid(row=1, column=2)


        tk.Button(

            input_frame,

            text="Add Order",

            command=self.add_order

        ).grid(row=1, column=3)


        columns = ("symbol", "shares", "buy_price")

        self.tree = ttk.Treeview(

            self.window,

            columns=columns,

            show="headings"

        )


        for col in columns:

            self.tree.heading(col, text=col)

            self.tree.column(col, width=120)


        self.tree.pack(fill=tk.BOTH, expand=True)


        btn_frame = tk.Frame(self.window)

        btn_frame.pack()


        tk.Button(btn_frame, text="Delete", command=self.delete).pack(side=tk.LEFT)

        tk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT)


        self.load_tree()


    def load_tree(self):

        self.tree.delete(*self.tree.get_children())

        for row in load_orders():

            self.tree.insert(

                "",

                tk.END,

                values=(

                    row['symbol'],

                    row['shares'],

                    row['buy_price']

                )

            )


    def add_order(self):

        symbol = self.symbol_entry.get().strip()

        shares = self.shares_entry.get().strip()

        price = self.price_entry.get().strip()


        if not symbol:

            return


        try:

            shares = float(shares)

            price = float(price)

        except:

            return


        self.tree.insert("", tk.END, values=(symbol, shares, price))


        self.symbol_entry.delete(0, tk.END)

        self.shares_entry.delete(0, tk.END)

        self.price_entry.delete(0, tk.END)


        self.save()


    def delete(self):

        for item in self.tree.selection():

            self.tree.delete(item)

        self.save()


    def save(self):

        data = []

        for row in self.tree.get_children():

            vals = self.tree.item(row)['values']

            data.append({

                'symbol': vals[0],

                'shares': float(vals[1]),

                'buy_price': float(vals[2])

            })

        save_orders(data)


# =========================
# PNL WINDOW
# =========================

class PnLWindow:

    def __init__(self, root, app):

        self.app = app

        self.window = tk.Toplevel(root)

        self.window.title("PnL")

        self.window.geometry("700x400")


        columns = ("Symbol","Shares","Buy","Current","PnL")

        self.tree = ttk.Treeview(

            self.window,

            columns=columns,

            show="headings"

        )


        for col in columns:

            self.tree.heading(col, text=col)

            self.tree.column(col, width=120)


        self.tree.pack(fill="both", expand=True)


        self.update()


    def update(self):

        self.tree.delete(*self.tree.get_children())

        for row in self.app.latest_rows:

            self.tree.insert("", "end", values=row)

        self.window.after(5000, self.update)


# =========================
# MAIN APP
# =========================

class App:

    def __init__(self, root):

        self.root = root


        tk.Button(root, text="Edit Orders", command=lambda: OrdersEditor(root)).pack()

        tk.Button(root, text="View PnL", command=lambda: PnLWindow(root, self)).pack()


        self.fig = mplfig.Figure()

        self.ax = self.fig.add_subplot(111)


        self.canvas = FigureCanvasTkAgg(self.fig, root)

        self.canvas.get_tk_widget().pack(fill="both", expand=True)


        self.times = []

        self.total_line = []

        self.symbol_lines = {}

        self.latest_rows = []

        self.pending = None


        threading.Thread(target=self.scrape_loop, daemon=True).start()

        self.gui_update()


    def scrape_loop(self):

        while True:

            try:

                orders = load_orders()

                total = 0

                symbol_totals = {}

                rows = []


                for order in orders:

                    price = get_price(order['symbol'])

                    if price is None:

                        continue


                    pnl = (price - order['buy_price']) * order['shares']

                    total += pnl


                    rows.append(

                        (

                            order['symbol'],

                            order['shares'],

                            order['buy_price'],

                            price,

                            round(pnl,2)

                        )

                    )


                    symbol_totals[order['symbol']] = symbol_totals.get(order['symbol'],0)+pnl


                now = datetime.now().strftime("%H:%M:%S")


                self.pending = (now,total,symbol_totals,rows)


            except Exception as e:

                print("Error:", e)


            time.sleep(5)


    def gui_update(self):

        if self.pending:


            now,total,symbol_totals,rows=self.pending


            self.latest_rows=rows


            self.times.append(now)

            self.total_line.append(total)


            for sym,pnl in symbol_totals.items():

                if sym not in self.symbol_lines:

                    self.symbol_lines[sym]=[]

                self.symbol_lines[sym].append(pnl)


            self.draw_chart()

            self.pending=None


        self.root.after(1000,self.gui_update)


    def draw_chart(self):

        self.ax.clear()

        self.ax.plot(self.times,self.total_line,label="TOTAL",linewidth=3)

        for sym,data in self.symbol_lines.items():

            self.ax.plot(self.times,data,label=sym)

        self.ax.legend()

        self.canvas.draw()


# =========================
# START
# =========================

root=tk.Tk()

root.title("PSX Tracker")

root.geometry("900x600")

app=App(root)

root.mainloop()
