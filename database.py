import pandas as pd
from datetime import datetime
import os

def get_excel_folder():
    folder = "orders"
    os.makedirs(folder, exist_ok=True)
    return folder

def get_excel_path():
    folder = get_excel_folder()
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(folder, f"orders_{today}.xlsx")

def create_orders_table():
    path = get_excel_path()
    if not os.path.exists(path):
        menu_items = [
            "Bún cá", "Bánh đa cá", "Mỳ tôm trứng", "Mỳ tôm trứng, xúc xích",
            "Bánh mì sốt vang", "Bún gà", "Miến gà", "Phở gà"
        ]
        cols = ["Thời gian"] + menu_items + ["Tổng", "Khách đưa", "Trả lại", "Phương thức", "Số điện thoại"]
        df = pd.DataFrame(columns=cols)
        df.to_excel(path, index=False)
    return path

def insert_order(selected, total, paid, change, method, phone):
    path = create_orders_table()
    df = pd.read_excel(path)
    time_now = datetime.now().strftime("%H:%M:%S")

    menu_items = [
        "Bún cá", "Bánh đa cá", "Mỳ tôm trứng", "Mỳ tôm trứng, xúc xích",
        "Bánh mì sốt vang", "Bún gà", "Miến gà", "Phở gà"
    ]
    new_row = {dish: 0 for dish in menu_items}

    for item in selected:
        dish = item["name"]
        qty = item["qty"]
        if dish in new_row:
            new_row[dish] = qty

    new_row.update({
        "Thời gian": time_now,
        "Tổng": total,
        "Khách đưa": paid,
        "Trả lại": change,
        "Phương thức": method,
        "Số điện thoại": phone if method == "Chuyển khoản" else ""
    })

    cols = ["Thời gian"] + menu_items + ["Tổng", "Khách đưa", "Trả lại", "Phương thức", "Số điện thoại"]
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df = df.reindex(columns=cols)
    df.to_excel(path, index=False)

def get_recent_orders(n=10):
    path = get_excel_path()
    if not os.path.exists(path):
        return pd.DataFrame(columns=['Thời gian'])
    df = pd.read_excel(path)
    return df.tail(n).iloc[::-1]
