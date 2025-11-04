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

def insert_order(selected, total, paid, change, method):
    """Append new order to today's Excel file"""
    path = create_orders_table()
    df = pd.read_excel(path)
    time_now = datetime.now().strftime("%H:%M:%S")
    order_list = ', '.join([f"{item['name']} ({item['qty']})" for item in selected])
    new_row = {
        'Thời gian': time_now,
        'Món': order_list,
        'Tổng': total,
        'Khách đưa': paid,
        'Trả lại': change,
        'Phương thức': method
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
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
