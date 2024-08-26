import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set page title and layout
st.title("TARGET DASHBOARD")
st.markdown("<h1>10-Month Moving Average</h1>", unsafe_allow_html=True)

# Create line chart
fig, ax = plt.subplots()
np.random.seed(0)
months = np.arange(1, 11)
values1 = np.random.rand(10) * 100 + 50
values2 = np.random.rand(10) * 150 + 75

ax.plot(months, values1, label='Data Set 1', color='blue')
ax.plot(months, values2, label='Data Set 2', color='red')

ax.set_xlabel('Month')
ax.set_ylabel('Value')
ax.legend()

# Create bar chart
fig2, ax2 = plt.subplots()
np.random.seed(0)
months = np.arange(1, 11)
values3 = np.random.rand(10) * 100 + 50
values4 = np.random.rand(10) * 150 + 75

ax2.bar(months, values3, label='Data Set 3', color='green')
ax2.bar(months, values4, label='Data Set 4', color='orange')

ax2.set_xlabel('Month')
ax2.set_ylabel('Value')
ax2.legend()

# Display charts
st.subheader("Line Chart")
st.pyplot(fig)

st.subheader("Bar Chart")
st.pyplot(fig2)