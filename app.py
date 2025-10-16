import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Currency Exchange Rates", layout="centered")
st.markdown("<h1 style='font-size:40px;'>โปรแกรมแสดงอัตราแลกเปลี่ยนสกุลเงิน</h1>", unsafe_allow_html=True)
st.caption("ข้อมูลเรียลไทม์จาก ExchangeRate-API")

# กำหนด API key
API_KEY = "5189948707252e7861f96c8f"

# เลือกสกุลเงินฐาน
BASE_CURRENCY = st.selectbox("สกุลเงินต้น (Base currency)", ["USD", "EUR", "THB", "JPY", "GBP"], index=0)

# ดึงข้อมูลจาก API
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"ไม่สามารถดึงข้อมูลได้: {e}")
    st.stop()

if "conversion_rates" in data:
    rates = data['conversion_rates']
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])

    # เลือกสกุลเงินเพื่อเปรียบเทียบ
    selected_currencies = st.multiselect(
        "เลือกสกุลเงินเพื่อเปรียบเทียบ", df["Currency"].tolist(),
        default=["THB", "EUR", "JPY", "GBP","USD"]
    )

    if selected_currencies:
        filtered_df = df[df["Currency"].isin(selected_currencies)]
        st.subheader(f"อัตราแลกเปลี่ยนจาก {BASE_CURRENCY}")
        st.table(filtered_df)

        # แปลงค่าอย่างรวดเร็ว
        st.subheader("แปลงค่าอย่างรวดเร็ว")
        amount = st.number_input(f"จำนวน ({BASE_CURRENCY})", min_value=0.0, value=1.0, step=1.0)
        if st.button("แปลง"):
            for cur in filtered_df["Currency"]:
                rate = rates[cur]
                st.write(f"{amount} {BASE_CURRENCY} = {amount*rate:.6f} {cur}")
    else:
        st.info("เลือกสกุลเงินเพื่อแสดง")
else:
    st.error(f"เกิดข้อผิดพลาดกับ API: {data.get('error-type', 'Unknown Error')}")

st.markdown("---")
st.caption("Deploy โดย: นางสาวเจนจิรา ชมภู 6610886107")


