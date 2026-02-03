import streamlit as st
import pandas as pd
st.title("good morning")
st.write("This is a simple Streamlit app.")
name=st.text_input("Enter your name:")
st.write(f"Hello, {name}!")
import matplotlib.pyplot as plt
import pandas as pd
url="https://raw.githubusercontent.com/GrandmaCan/ML/main/Resgression/Salary_Data.csv"
data=pd.read_csv(url)
st.write(data)