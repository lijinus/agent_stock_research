import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import requests


st.set_page_config(page_title="Stock Real Time Analysis", layout="wide")


st.title("Stock Real Time Analysis")


ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, SPY):", "SPY")
news_api_key = st.secrets.get("newsapi_key", "YOUR_NEWSAPI_KEY")


if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info


    st.header(f"Profile: {info.get('longName', 'N/A')}")
    col1, col2 = st.columns(2)


    with col1:
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
        st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
        st.markdown(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
        st.markdown(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")


    with col2:
        st.markdown(f"**52 Week Range:** {info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.markdown(f"**YTD Return:** {info.get('ytdReturn', 'N/A')}")


    st.subheader("1-Year Historical Price Chart")
    hist = stock.history(period="1y")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title=f"{ticker} - 1 Year Closing Prices",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)",
                      hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Earnings (Yearly)")
    earnings = stock.earnings
    st.dataframe(earnings.tail())


    st.subheader("Recent News")
    company_name = info.get("longName", ticker)
    news_url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&apiKey={news_api_key}&language=en"
    try:
        response = requests.get(news_url)
        articles = response.json().get("articles", [])
        if articles:
            for article in articles[:5]:
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.markdown(f"*{article['source']['name']} - {article['publishedAt']}*")
                st.write(article['description'])
                st.markdown("---")
        else:
            st.info("No recent news found.")
    except Exception as e:
        st.warning("Failed to fetch news. Check your API key and internet connection.")