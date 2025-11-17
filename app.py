import streamlit as st
import pandas as pd
import io
from datetime import datetime
from database import create_orders_table, insert_order, get_recent_orders
from order import load_menu, order, payment_input

st.set_page_config(page_title='Hệ thống bán hàng CTT7', layout='centered')
st.title('Hệ thống bán hàng CTT7')

date = datetime.now().strftime("%d-%m-%Y")

# Load breakfast menu
menu = load_menu('brekkie.json')
reset_id = st.session_state.get('reset_id', 0)

with st.expander('🍳 Menu ăn sáng', expanded=True):
    selected_items, total = order(menu, reset_id)
    paid, change, method, phone = payment_input(total)

if st.button("Xác nhận thanh toán", use_container_width=True):
    if not selected_items:
        st.error("⚠️ Chưa có món nào được chọn!")
    elif method == "Tiền mặt" and change < 0:
        st.error("Số tiền khách đưa không đủ!")
    else:
        if method == "Chuyển khoản":
            paid = total
            change = 0
        elif method == "Tiền mặt":
            change = max(paid - total, 0)

        create_orders_table()
        insert_order(selected_items, total, paid, change, method, phone)
        st.success("✅ Thanh toán thành công và đã lưu đơn hàng!")

        next_reset_id = st.session_state.get('reset_id', 0) + 1
        st.session_state.clear()
        st.session_state['reset_id'] = next_reset_id
        st.rerun()



# 🧾 Recent orders
st.subheader('Đơn hàng gần đây')
try:
    df = get_recent_orders(10)
    if df.empty:
        st.info("Chưa có đơn hàng nào hôm nay.")
    else:
        st.dataframe(df)
except Exception as e:
    st.error(f'Không thể tải đơn hàng: {e}')

# 💾 Download Excel file
if 'df' in locals() and not df.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Orders')

    st.download_button(
        label="💾 Tải file Excel đơn hàng",
        data=output.getvalue(),
        file_name=f"don_hang_ngay_{date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
