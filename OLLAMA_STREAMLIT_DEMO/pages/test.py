import streamlit as st
import matplotlib.pyplot as plt

# Set page title and layout
st.title("TARGET DASHBOARD")
st.markdown("<h1>Subtitle goes here.</h1>", unsafe_allow_html=True)

# Create metrics section
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Metric 1", value=56, delta=None, delta_color="normal")
with col2:
    st.metric(label="Metric 2", value=87, delta=None, delta_color="normal")

# Create graphs section
st.header("Graphs")
col3, col4 = st.columns(2)
with col3:
    fig1 = plt.figure(figsize=(5, 3))
    plt.bar(["Category 1", "Category 2", "Category 3"], [10, 20, 30], color=["#007bff", "#ffffff", "#000000"])
    st.pyplot(fig1)

with col4:
    fig2 = plt.figure(figsize=(5, 3))
    plt.plot([1, 2, 3, 4, 5], label="Trend")
    plt.scatter(2, 10, color="#000000")
    plt.scatter(4, 20, color="#000000")
    plt.legend()
    st.pyplot(fig2)