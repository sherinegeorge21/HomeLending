import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fredapi import Fred
from openai import OpenAI

# --------- CONFIG ---------
st.set_page_config(layout="wide")
st.title("🏠 Home Lending Data Explorer")

# --------- API KEYS ---------
fred = Fred(api_key=st.secrets["fred_api_key"])

client = OpenAI(api_key=st.secrets["openai_api_key"])

# --------- SECTION 1: Mortgage Rate Data ---------

@st.cache_data
def load_mortgage_data():
    data = fred.get_series('MORTGAGE30US')
    df = pd.DataFrame({"Date": data.index, "Rate": data.values})
    return df

st.subheader("📈 30-Year Fixed Mortgage Rate")
mortgage_df = load_mortgage_data()
fig = px.line(mortgage_df, x="Date", y="Rate", title="30-Year Fixed Mortgage Rate (%)")
st.plotly_chart(fig, use_container_width=True)

if st.button("📣 Explain This Trend"):
    recent_df = mortgage_df.tail(12)
    start_rate = recent_df["Rate"].iloc[0]
    end_rate = recent_df["Rate"].iloc[-1]

    if end_rate > start_rate * 1.05:
        trend = "Mortgage rates have significantly increased over the past year."
    elif end_rate < start_rate * 0.95:
        trend = "Mortgage rates have dropped notably in the past year."
    else:
        trend = "Mortgage rates have stayed relatively stable over the past year."

    user_prompt = f"""
    {trend}
    Based on this trend in 30-year fixed mortgage rates, explain how it might impact:
    - Home loan approvals
    - Borrower behavior
    - Housing affordability
    Use simple terms.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_prompt}]
    )
    explanation = response.choices[0].message.content
    st.markdown("### 🤖 LLM-Powered Explanation:")
    st.write(explanation)

# --------- SECTION 2: User Credibility Checker ---------

st.sidebar.header("🔎 Check User Credibility")
with st.sidebar.form("user_form"):
    income = st.number_input("Monthly Income ($)", value=6000)
    dti = st.slider("Debt-to-Income Ratio (%)", 0, 60, value=36)
    credit_score = st.slider("Credit Score", 300, 850, value=700)
    employment_years = st.slider("Years at Current Job", 0, 30, value=2)
    loan_amount = st.number_input("Loan Amount Requested ($)", value=250000)
    property_price = st.number_input("Property Price ($)", value=300000)
    submit = st.form_submit_button("Evaluate Credibility")

if submit:
    risk_score = 0
    ltv = (loan_amount / property_price) * 100 if property_price > 0 else 0

    if credit_score < 620:
        risk_score += 2
    if dti > 43:
        risk_score += 2
    if income < 3000:
        risk_score += 1
    if employment_years < 1:
        risk_score += 1
    if ltv > 90:
        risk_score += 1

    if risk_score <= 1:
        st.success("🟢 Low Risk — Likely Credible")
    elif risk_score == 2:
        st.warning("🟡 Moderate Risk — Needs Closer Review")
    else:
        st.error("🔴 High Risk — Potential Lending Concern")

    st.markdown("### 🤖 AI-based Explanation:")
    prompt = f"""
    A user is applying for a home loan:
    - Monthly income: ${income}
    - DTI: {dti}%
    - Credit score: {credit_score}
    - Employment: {employment_years} years
    - Loan amount: ${loan_amount}
    - Property price: ${property_price}
    Assess their credibility for a mortgage and explain why in simple terms.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_result = response.choices[0].message.content
    st.write(ai_result)

# --------- FOOTER ---------
st.markdown("---")
st.caption("Built by Sherine George | Home Lending AI Showcase")
