import json
import streamlit as st

def load_menu(path):
    """Load menu JSON file as Python list of dicts"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)   # ✅ CORRECT

def order(menu):
    selected_items = []
    total = 0
    st.subheader('Chọn món')

    for i, item in enumerate(menu):
        qty = st.number_input(
            f"{item['item']} {item['Thành tiền']:,.0f} VND",
            key=f"{item['id']}_qty_{i}",  # <-- unique key per item per render
            min_value=0,
            max_value=20,
            value=0
        )

        # keys = [f"{item['id']}_qty_{i}" for i, item in enumerate(menu)]
        # st.write(keys)  # Just for debugging

        if qty > 0:
            selected_items.append({
                'name': item['item'],
                'qty': qty,
                'price': item['Thành tiền']})
                
        total += item['Thành tiền'] * qty

    st.subheader(f"**Tổng tiền: {total:,.0f} VND**")
    return selected_items, total

def payment_input(total):
    """Handle payment input and method selection"""
    st.subheader('Thanh toán')
    st.write('Chọn phương thức thanh toán')
    method = st.radio("Phương thức thanh toán:", ['Tiền mặt', 'Chuyển khoản'], horizontal=True)

    # Initialize session state and default variables
    if 'transfer_confirmed' not in st.session_state:
        st.session_state['transfer_confirmed'] = False
    if "cash_given" not in st.session_state:
        st.session_state.cash_given = 0

    paid = 0
    change = 0
    phone = ""  # ✅ define this at the start so it always exists

    if method == 'Tiền mặt':
        st.write('Chọn số tiền khách đưa:')
        col1, col2, col3, col4 = st.columns(4)
        presets = [50000, 100000, 200000, 500000]

        for col, val in zip([col1, col2, col3, col4], presets):
            if col.button(f"+{val:,} VND"):
                st.session_state.cash_given += val

        if st.button("🔁 Reset số tiền"):
            st.session_state.cash_given = 0

        custom = st.number_input("Hoặc nhập thêm thủ công:", min_value=0, step=10000)
        paid = st.session_state.cash_given + custom
        change = max(paid - total, 0)

        st.write(f"**Tổng tiền khách đưa: {paid:,.0f} VND**")
        st.write(f"**Tiền thừa: {change:,.0f} VND**")

        st.session_state['transfer_confirmed'] = False

    else:  # Chuyển khoản
        st.info('Khách chọn phương thức chuyển khoản.\nVui lòng xác nhận khi đã nhận đủ tiền.') 
        st.number_input('Nhập số tiền chuyển khoản:', value=total, disabled=True, step=10000)

        # 📱 Ask for customer phone number only for transfers
        phone = st.text_input("📞 Nhập số điện thoại khách hàng:", placeholder="VD: 0912345678")

        if not st.session_state['transfer_confirmed']:
            if st.button("Xác nhận đã nhận chuyển khoản"):
                st.session_state['transfer_confirmed'] = True
                st.success("✅ Khách đã thanh toán đủ")
        else:
            st.success("✅ Khách đã thanh toán đủ")

        if st.session_state['transfer_confirmed']:
            paid = total
            change = 0

    return paid, change, method, phone


    