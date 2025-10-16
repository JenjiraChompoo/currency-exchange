import streamlit as st
import requests
from datetime import datetime
from typing import Dict

st.set_page_config(page_title="Currency Exchange Rates", layout="centered")

st.title("โปรแกรมแสดงอัตราแลกเปลี่ยนสกุลเงิน")
st.caption("ข้อมูลเรียลไทม์จาก exchangerate.host (ไม่มีคีย์)")

# ปรับค่าเริ่มต้น
base = st.selectbox("สกุลเงินฐาน (Base currency)", options=[
    "THB","USD","EUR","JPY","GBP","CNY","AUD","SGD"
], index=0)

symbols_input = st.text_input("สกุลเงินเป้าหมาย (comma-separated, เช่น USD,EUR,JPY)", value="USD,EUR,JPY")
symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

# ฟังก์ชันดึงข้อมูล (cached)
@st.cache_data(ttl=300)
def fetch_rates(base_currency: str, symbols_list) -> Dict:
    # ใช้ exchangerate.host (ฟรี ไม่มีคีย์)
    url = "https://api.exchangerate.host/latest"
    params = {"base": base_currency}
    if symbols_list:
        params["symbols"] = ",".join(symbols_list)
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

try:
    data = fetch_rates(base, symbols)
except Exception as e:
    st.error(f"ไม่สามารถดึงข้อมูลอัตราแลกเปลี่ยนได้: {e}")
    st.stop()

# แสดงข้อมูล
last_update = data.get("date", "")
rates = data.get("rates", {})

col1, col2 = st.columns([2,1])
with col1:
    st.subheader(f"สกุลฐาน: {base}")
    if last_update:
        st.write(f"ข้อมูล ณ วันที่: {last_update}")
    st.write("ผลลัพธ์ (1 base = ? target)")

    if not rates:
        st.info("ไม่มีข้อมูลสำหรับสกุลเงินที่ระบุ")
    else:
        table_rows = []
        for cur, rate in rates.items():
            table_rows.append((cur, f"{rate:.6f}"))
        st.table({"Currency": [r[0] for r in table_rows], "Rate": [r[1] for r in table_rows]})

with col2:
    st.subheader("แปลงค่าอย่างรวดเร็ว")
    amount = st.number_input(f"จำนวน ({base})", min_value=0.0, value=1.0, step=1.0)
    if st.button("แปลง"):
        if not rates:
            st.warning("ไม่มีอัตราเพื่อแปลง")
        else:
            conv = {cur: amount * rate for cur, rate in rates.items()}
            for cur, v in conv.items():
                st.write(f"{amount} {base} = {v:.6f} {cur}")

st.markdown("---")
st.caption("ข้อมูลจาก exchangerate.host — ใช้งานฟรี (ไม่มี API key)")
st.write("")
st.write("Deploy โดย: นักศึกษา — ชื่อ/รหัส: __________________")
