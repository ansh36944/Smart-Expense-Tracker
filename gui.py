import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date
# from PIL import Image, ImageTK

FILE = "expenses.json"

# ---------- COLORS ----------
BG = "#F3F5F9"
SIDEBAR = "#172554"
PRIMARY = "#2563EB"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"


# ---------- DATA ----------
def load_data():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_data():
    with open(FILE, "w") as file:
        json.dump(expenses, file, indent=4)


expenses = load_data()


# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("1150x720")
root.minsize(950, 600)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=35,
    fieldbackground=WHITE,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#E2E8F0",
    foreground=TEXT,
    font=("Segoe UI", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")]
)


# ---------- HEADER ----------
header = tk.Frame(root, bg=WHITE, height=75)
header.pack(fill="x")

tk.Label(
    header,
    text="  Smart Expense Tracker",
    bg=WHITE,
    fg=SIDEBAR,
    font=("Segoe UI", 21, "bold")
).pack(side="left", padx=20, pady=18)

tk.Label(
    header,
    text="Hi, Mr.Anshul",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 9, "bold")
).pack(side="right", padx=25)


# ---------- MAIN LAYOUT ----------
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg=SIDEBAR, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="MENU",
    bg=SIDEBAR,
    fg="#94A3B8",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", padx=22, pady=(30, 15))

tk.Label(
    sidebar,
    text="▣  Dashboard",
    bg=SIDEBAR,
    fg=WHITE,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=22, pady=12)

tk.Label(
    sidebar,
    text="₹  Expenses",
    bg=SIDEBAR,
    fg="#CBD5E1",
    font=("Segoe UI", 12)
).pack(anchor="w", padx=22, pady=12)

tk.Label(
    sidebar,
    text="▤  Reports",
    bg=SIDEBAR,
    fg="#CBD5E1",
    font=("Segoe UI", 12)
).pack(anchor="w", padx=22, pady=12)

tk.Label(
    sidebar,
    text="Smart Finance App",
    bg=SIDEBAR,
    fg="#94A3B8",
    font=("Segoe UI", 9)
).pack(side="bottom", pady=20)


# ---------- CONTENT ----------
content = tk.Frame(body, bg=BG)
content.pack(side="left", fill="both", expand=True, padx=25, pady=22)

tk.Label(
    content,
    text="Dashboard Overview",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 20, "bold")
).pack(anchor="w")

tk.Label(
    content,
    text="Track and manage your daily spending.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", pady=(3, 18))


# ---------- SUMMARY CARDS ----------
cards = tk.Frame(content, bg=BG)
cards.pack(fill="x", pady=5)

def create_card(parent, title):
    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=18,
        pady=15,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        card,
        text=title,
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w")

    value = tk.Label(
        card,
        text="₹0.00",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 19, "bold")
    )
    value.pack(anchor="w", pady=(8, 0))

    return value


total_label = create_card(cards, "Total Expenses")
count_label = create_card(cards, "Transactions")
average_label = create_card(cards, "Average Expense")


# ---------- ACTION BAR ----------
actions = tk.Frame(content, bg=BG)
actions.pack(fill="x", pady=18)

def add_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=PRIMARY,
        fg=WHITE,
        activebackground="#1D4ED8",
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=9,
        font=("Segoe UI", 10, "bold")
    )


# ---------- SEARCH AND FILTER ----------
search_var = tk.StringVar()
category_var = tk.StringVar(value="All Categories")

search_entry = tk.Entry(
    actions,
    textvariable=search_var,
    font=("Segoe UI", 10),
    width=25,
    relief="solid",
    bd=1
)
search_entry.pack(side="left", ipady=8, padx=(0, 10))

category_box = ttk.Combobox(
    actions,
    textvariable=category_var,
    values=["All Categories", "Food", "Travel",
            "Shopping", "Education", "Bills", "Other"],
    state="readonly",
    width=17
)
category_box.pack(side="left", ipady=5, padx=5)


# ---------- EXPENSE TABLE ----------
table_frame = tk.Frame(content, bg=WHITE)
table_frame.pack(fill="both", expand=True)

tk.Label(
    table_frame,
    text="Recent Transactions",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 13, "bold")
).pack(anchor="w", padx=15, pady=12)

columns = ("title", "amount", "category", "date")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading("title", text="Expense Title")
tree.heading("amount", text="Amount (₹)")
tree.heading("category", text="Category")
tree.heading("date", text="Date")

tree.column("title", width=220)
tree.column("amount", width=130, anchor="center")
tree.column("category", width=150, anchor="center")
tree.column("date", width=130, anchor="center")

tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))


# ---------- CHART ----------
chart_frame = tk.Frame(content, bg=WHITE, padx=15, pady=12)
chart_frame.pack(fill="x", pady=12)

tk.Label(
    chart_frame,
    text="Category-wise Spending",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

chart = tk.Canvas(
    chart_frame,
    height=125,
    bg=WHITE,
    highlightthickness=0
)
chart.pack(fill="x", pady=5)


# ---------- REFRESH ----------
def refresh():
    total = sum(float(e.get("amount", 0)) for e in expenses)
    count = len(expenses)
    average = total / count if count else 0

    total_label.config(text=f"₹{total:,.2f}")
    count_label.config(text=str(count))
    average_label.config(text=f"₹{average:,.2f}")

    for item in tree.get_children():
        tree.delete(item)

    search = search_var.get().lower()
    category = category_var.get()

    for index, item in enumerate(expenses):
        title = str(item.get("title", ""))
        amount = float(item.get("amount", 0))
        cat = str(item.get("category", "Other"))
        expense_date = item.get("date", "")

        if search not in title.lower():
            continue

        if category != "All Categories" and cat != category:
            continue

        tree.insert(
            "",
            "end",
            iid=str(index),
            values=(title, f"{amount:,.2f}", cat, expense_date)
        )

    draw_chart()


# ---------- CATEGORY CHART ----------
def draw_chart():
    chart.delete("all")

    totals = {}

    for item in expenses:
        category = item.get("category", "Other")
        amount = float(item.get("amount", 0))
        totals[category] = totals.get(category, 0) + amount

    if not totals:
        chart.create_text(
            350, 55,
            text="No expense data available",
            fill=MUTED,
            font=("Segoe UI", 10)
        )
        return

    maximum = max(totals.values())

    for index, (category, amount) in enumerate(totals.items()):
        y = 18 + index * 25
        bar_width = 300 * amount / maximum if maximum else 0

        chart.create_text(
            5, y,
            text=category,
            anchor="w",
            fill=TEXT,
            font=("Segoe UI", 9)
        )

        chart.create_rectangle(
            110, y - 7,
            110 + bar_width, y + 7,
            fill=PRIMARY,
            outline=""
        )

        chart.create_text(
            425, y,
            text=f"₹{amount:,.2f}",
            anchor="w",
            fill=TEXT,
            font=("Segoe UI", 9)
        )


# ---------- ADD EXPENSE ----------
def add_expense():
    window = tk.Toplevel(root)
    window.title("Add New Expense")
    window.geometry("380x420")
    window.configure(bg=WHITE)
    window.resizable(False, False)
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="Add New Expense",
        bg=WHITE,
        fg=SIDEBAR,
        font=("Segoe UI", 18, "bold")
    ).pack(pady=20)

    entries = {}

    fields = ["Expense Title", "Amount"]

    for field in fields:
        tk.Label(
            window,
            text=field,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=35, pady=(8, 3))

        entry = tk.Entry(window, font=("Segoe UI", 11))
        entry.pack(fill="x", padx=35, ipady=7)
        entries[field] = entry

    tk.Label(
        window,
        text="Category",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=35, pady=(12, 3))

    category = ttk.Combobox(
        window,
        values=["Food", "Travel", "Shopping",
                "Education", "Bills", "Other"],
        state="readonly"
    )
    category.set("Food")
    category.pack(fill="x", padx=35, ipady=5)

    def save_expense():
        title = entries["Expense Title"].get().strip()
        amount_text = entries["Amount"].get().strip()

        if not title or not amount_text:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields.",
                parent=window
            )
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid amount greater than zero.",
                parent=window
            )
            return

        expense = {
            "title": title,
            "amount": amount,
            "category": category.get(),
            "date": date.today().strftime("%Y-%m-%d")
        }

        expenses.append(expense)
        save_data()
        refresh()

        messagebox.showinfo(
            "Success",
            "Expense added successfully!",
            parent=window
        )
        window.destroy()

    add_button(window, "Save Expense", save_expense).pack(pady=25)


# ---------- DELETE EXPENSE ----------
def delete_expense():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select an expense first."
        )
        return

    index = int(selected[0])

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Do you want to delete this expense?"
    )

    if confirm:
        expenses.pop(index)
        save_data()
        refresh()


# ---------- BUTTONS ----------
add_button(actions, "+ Add Expense", add_expense).pack(
    side="right", padx=5
)

tk.Button(
    actions,
    text="Delete Selected",
    command=delete_expense,
    bg="#DC2626",
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=9,
    font=("Segoe UI", 10, "bold")
).pack(side="right", padx=5)


# ---------- EVENTS ----------
search_var.trace_add("write", lambda *args: refresh())
category_box.bind("<<ComboboxSelected>>", lambda event: refresh())

refresh()

root.mainloop()
