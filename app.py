import streamlit as st
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from database import create_orders_table, insert_order, get_recent_orders
from order import load_menu, order


# --- AUTHENTICATION SETUP ---
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("ctt7-posapp-d2c04659cc7c.json", scopes=SCOPE)
client = gspread.authorize(creds)


st.set_page_config(page_title='Hệ thống bán hàng CTT7', layout='centered')

st.title('Hệ thống bán hàng CTT7')

date = datetime.now().strftime("%d-%m-%Y")

# load breakfast menu
menu = load_menu('brekkie.json')
with st.expander('Menu ăn sáng', expanded=True):
    selected, total, change, paid, method = order(menu)

    if st.button('Xác nhận thanh toán'):
        if not selected:
            st.error('Chưa có món nào được chọn!')
        elif change < 0:
            st.error('Số tiền khách đưa không đủ!')
        elif change == 0:
            st.success(f'Thanh toán thành công! Khách hàng đưa đủ {total:,.0f} VND.')
        elif change > 0:
            st.success(f'Thanh toán thành công! Trả lại khách hàng: {change:,.0f} VND.') 
            create_orders_table()
            insert_order(selected, total, paid, change, method)
            st.success('Đơn hàng đã được lưu.')

st.subheader('Đơn hàng gần đây')
try:
    df = get_recent_orders(10)
    st.dataframe(df)
except Exception as e:
    st.error(f'Không thể tải đơn hàng: {e}')

if 'df' in locals() and not df.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Orders')
    st.download_button(
        label="Tải file Excel đơn hàng",
        data=output.getvalue(),
        file_name=f"đơn_hàng_ngày_{date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )