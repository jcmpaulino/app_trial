import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit_authenticator as stauth

# User authentication
names = ['John Doe', 'Jane Smith']
usernames = ['johndoe', 'janesmith']
passwords = ['123', '456']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.title('Stock Return Viewer')

    st.sidebar.header('User Input')
    start_date = st.sidebar.date_input('Start date', pd.Timestamp('2022-01-01'))
    end_date = st.sidebar.date_input('End date', pd.Timestamp('2023-01-01'))
    tickers = st.sidebar.text_input('Stock tickers (comma-separated)', 'AAPL, MSFT')

    if st.sidebar.button('Show Returns'):
        tickers = [ticker.strip().upper() for ticker in tickers.split(',')]
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        returns = data.pct_change().dropna()
        st.write('Returns:')
        st.write(returns)

    authenticator.logout('Logout', 'sidebar')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')