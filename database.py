import pandas as pd
from datetime import datetime
import os

def get_excel_folder():
    """Folder to store all Excel order files"""
    folder = "orders"
    os.makedirs(folder, exist_ok=True)
    return folder

def get_excel_path():
    """Generate a daily Excel file path inside the folder"""
    folder = get_excel_folder()
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(folder, f"orders_{today}.xlsx")

def create_orders_table():
    """Create today's Excel file if not exists"""
    path = get_excel_path()
    if not os.path.exists(path):
        df = pd.DataFrame(columns=['Thời gian', 'Món', 'Tổng', 'Khách đưa', 'Trả lại', 'Phương thức'])
        df.to_excel(path, index=False)
    return path

def insert_order(selected, total, paid, change, method, phone):
    """Append a new order to today's Excel file (with phone number)."""
    path = create_orders_table()
    df = pd.read_excel(path)
    time_now = datetime.now().strftime("%H:%M:%S")

    # List of all dishes in your menu
    menu_items = [
        "Bún cá", "Bánh đa cá", "Mỳ tôm trứng", "Mỳ tôm trứng, xúc xích",
        "Bánh mì sốt vang", "Bún gà", "Miến gà", "Phở gà"
    ]

    # Initialize all dishes as 0
    new_row = {dish: 0 for dish in menu_items}

    # Fill in the ordered quantities
    for item in selected:
        dish = item["name"]
        qty = item["qty"]
        if dish in new_row:
            new_row[dish] = qty

    # Add metadata fields
    new_row.update({
        "Thời gian": time_now,
        "Tổng": total,
        "Khách đưa": paid,
        "Trả lại": change,
        "Phương thức": method,
        "Số điện thoại": phone if method == "Chuyển khoản" else ""  # only save for transfers
    })

    # Define and enforce column order
    cols = ["Thời gian"] + menu_items + ["Tổng", "Khách đưa", "Trả lại", "Phương thức", "Số điện thoại"]
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df = df.reindex(columns=cols)

    # Save to Excel
    df.to_excel(path, index=False)


def get_recent_orders(n=10):
    """Return the most recent orders for *today only*"""
    path = get_excel_path()  # Always points to today's file

    # If today's file doesn't exist, return empty DataFrame
    if not os.path.exists(path):
        return pd.DataFrame(columns=['Thời gian', 'Món', 'Tổng', 'Khách đưa', 'Trả lại', 'Phương thức'])

    # Read only today's orders
    df = pd.read_excel(path)
    return df.tail(n).iloc[::-1]
