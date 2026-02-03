import streamlit as st
import pandas as pd
st.title("good morning")
st.write("This is a simple Streamlit app.")
name=st.text_input("Enter your name:")
st.write(f"Hello, {name}!")