import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="FinSight AI Dashboard", layout="wide")
st.title("📊 FinSight AI: Business Analytics & Chatbot Platform")
GEMINI_API_KEY = "your_api_key_here"
# REPLACE THE TEXT BELOW WITH THE API KEY YOU COPIED FROM GOOGLE AI STUDIO

# 2. Load the Dataset
@st.cache_data
def load_data():
    return pd.read_csv("sales_data.csv")

df = load_data()

# 3. Calculate Core Metrics
df["Total_Revenue"] = df["Units_Sold"] * df["Unit_Price"]
total_sales = df["Total_Revenue"].sum()
total_units = df["Units_Sold"].sum()

# 4. Display KPI Summary Cards
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Revenue Generated", value=f"${total_sales:,}")
with col2:
    st.metric(label="Total Units Sold", value=f"{total_units:,}")

st.markdown("---")

# 5. Interactive Selection Filter Dropdown & Chart
st.subheader("Interactive Visual Analytics")
all_regions = ["All"] + list(df["Region"].unique())
selected_region = st.selectbox("Select a region to analyze:", all_regions)

filtered_df = df if selected_region == "All" else df[df["Region"] == selected_region]

fig = px.bar(
    filtered_df, x="Product", y="Total_Revenue", color="Category",
    title=f"Revenue Performance Matrix ({selected_region} Region)"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. Generative AI Chatbot Integration
st.subheader("🤖 Chat with Your Business Data")
st.write("Ask Gemini any questions about your sales data spreadsheet below!")

user_question = st.text_input("Ask a question (e.g., 'Which product has the highest unit price?'):")

if user_question:
    if GEMINI_API_KEY == "your_api_key_here":
        st.warning("Please paste your real Gemini API key into the code to activate the chat!")
    else:
        try:
            # Initialize the official Google GenAI client
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            # Create a contextual prompt feeding the spreadsheet data into the LLM
            context_prompt = f"""
            You are an expert business data analyst assistant. 
            Here is the current company sales spreadsheet data in CSV format:
            
            {df.to_csv(index=False)}
            
            Based strictly on the data above, answer the following user question clearly and concisely:
            "{user_question}"
            """
            
            # Request a generation from Gemini 2.5 Flash
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=context_prompt,
            )
            
            st.success("🤖 Gemini's Analysis:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"An error occurred while connecting to Gemini: {e}")