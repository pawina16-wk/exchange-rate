import streamlit as st
import requests
import pandas as pd

# 🌍 ชื่อหน้า
st.title("💵 อัตราแลกเปลี่ยนเงินตรา (1 USD เท่ากับเท่าไหร่?)")

# 🔗 เรียก API ด้วย key ฟรี
url = "https://v6.exchangerate-api.com/v6/63d73b62648140f32f161085/latest/USD"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # 🪙 แสดงอัตราฐาน
    st.subheader("ฐานอัตราแลกเปลี่ยน: 1 USD")
    
    # 📊 ดึง rates และแปลงเป็น DataFrame
    rates = data.get("conversion_rates", {})
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
    df = df.sort_values(by="Rate", ascending=False).reset_index(drop=True)

    # 🔍 ช่องค้นหา
    st.write("🔎 พิมพ์รหัสสกุลเงิน เช่น THB, JPY, EUR เพื่อค้นหาอัตราเฉพาะ")
    search_currency = st.text_input("ค้นหาสกุลเงิน (เช่น THB):").upper().strip()

    # 💡 ไฮไลต์แถวที่ค้นหา
    def highlight_row(row):
        if search_currency and row["Currency"] == search_currency:
            return ['background-color: #ff4d4d; color: white; font-weight: bold'] * len(row)
        else:
            return [''] * len(row)

    # 💰 แสดงผลลัพธ์การค้นหา
    if search_currency:
        if search_currency in rates:
            rate = rates[search_currency]
            st.success(f"💰 1 USD = {rate} {search_currency}")
        else:
            st.warning("❌ ไม่พบสกุลเงินที่ค้นหา")

    # 📋 แสดงตารางพร้อมไฮไลต์
    styled_df = df.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True)
else:
    st.error("❌ ไม่สามารถเรียก API ได้ กรุณาลองใหม่")
