import json
import streamlit as st

def load_menu(menu_file='brekkie.json'):
    with open(menu_file, 'r', encoding='utf-8') as f:
        menu_data = json.load(f)
    return {item['item']: item['Thành tiền'] for item in menu_data}

def order(menu):
    ''' Select items, handling payment and return results'''
    st.subheader('Chọn món menu ăn sáng')
    
    brekkie = st.selectbox('Chọn món', menu.keys(), accept_new_options=True)
    qty = st.number_input('Số lượng:', min_value=1, step=1, value=1)        
    st.write(f'Món được chọn: {brekkie}')
    total = menu[brekkie] * qty
    st.write(f'Tổng cộng: {total:,.0f} VND')

    st.subheader('Thanh toán')
    paid = st.number_input('Nhập số tiền khách đưa:', min_value=0, step=1000)
    change = paid - total
    method = st.radio('Chọn phương thức thanh toán:', ('Tiền mặt', 'Thẻ', 'Ví điện tử'), horizontal=True)

    return brekkie, change, total , paid, method
    