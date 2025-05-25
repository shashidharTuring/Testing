import streamlit as st

st.title("Echo Application")

user_text = st.text_input("Enter some text and press Enter")

if user_text:
    st.write("You entered:", user_text)
