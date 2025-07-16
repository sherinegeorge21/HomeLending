# 🏠 Home Lending AI Explorer

This is a Streamlit-powered web app that helps users explore mortgage trends and assess home loan credibility using real-time data and GenAI explanations.

## 🚀 Features

•⁠  ⁠📈 *30-Year Fixed Mortgage Trend Viewer*  
  Visualizes historical U.S. mortgage rate data (via FRED API) with an LLM-generated explanation of current rate trends.

•⁠  ⁠🤖 *LLM-Powered Trend Insights*  
  Uses OpenAI to explain the impact of mortgage rate changes on borrower behavior, housing affordability, and loan approvals.

•⁠  ⁠🔍 *User Credibility Checker*  
  Evaluates a home loan applicant's risk profile using basic underwriting logic (credit score, income, LTV, DTI, etc.) and provides an AI explanation.

## 🧠 Tech Stack

•⁠  ⁠Python, Streamlit, Plotly  
•⁠  ⁠[FRED API](https://fred.stlouisfed.org/) for mortgage data  
•⁠  ⁠[OpenAI API](https://platform.openai.com/) for explanations

## 📦 Setup Instructions

1.⁠ ⁠Clone the repo  
   ```bash
   git clone https://github.com/sherinegeorge21/HomeLending.git
   cd HomeLending
```
2.⁠ ⁠Create and activate virtual environment
   ```bash
 python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```
3.⁠ Install dependencies
```bash
pip install -r requirements.txt
```
4.⁠ ⁠Set up your Streamlit secrets

Create a file .streamlit/secrets.toml and add:

fred_api_key = "your_fred_api_key"
openai_api_key = "your_openai_key"

5. Run the app
```bash
streamlit run app.py
```
