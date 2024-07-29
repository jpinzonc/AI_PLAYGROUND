import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(page_title="Project Status Dashboard", layout="wide")

# Title
st.title("Project Status Dashboard")

# Project Details
st.sidebar.text("Project Name: IT Career map")
st.sidebar.text("Project Phase: 2 selected")

# Main content
col1, col2 = st.columns(2)

with col1:
    # Project Cost Performance
    st.subheader("Project Cost Performance")
    total_budget = 93332
    actual_cost = 48048
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=actual_cost,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Actual Cost"},
        gauge={'axis': {'range': [None, total_budget]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, total_budget * 0.6], 'color': "lightgreen"},
                   {'range': [total_budget * 0.6, total_budget * 0.8], 'color': "yellow"},
                   {'range': [total_budget * 0.8, total_budget], 'color': "red"}],
               'threshold': {
                   'line': {'color': "red", 'width': 4},
                   'thickness': 0.75,
                   'value': actual_cost}}))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.metric("Total Budget", f"${total_budget:,}")
    st.metric("Actual Cost", f"${actual_cost:,}")

with col2:
    # Project Performance
    st.subheader("Project Performance")
    col2a, col2b = st.columns(2)
    
    with col2a:
        st.metric("SPI", "0.89", delta="-0.11")
    with col2b:
        st.metric("CPI", "0.87", delta="-0.13")
    
    st.metric("Planned Value (PV)", "$46,666.00")
    st.metric("Earned Value (EV)", "$41,579.40")

# Time vs Project Phase
st.subheader("Time vs Project Phase")
phase_data = {
    'Phase': ['Closure Stage', 'Execution Stage', 'Monitor & Control', 'Project Initiation Stage', 'Project Planning Stage'],
    'Hours': [5, 164, 36, 40, 144]
}
df_phase = pd.DataFrame(phase_data)

fig_phase = px.bar(df_phase, x='Hours', y='Phase', orientation='h')
st.plotly_chart(fig_phase, use_container_width=True)

# Project Phase % Completed
st.subheader("Project Phase % Completed")
completion_data = {
    'Phase': ['Project Planning Stage', 'Project Initiation Stage', 'Monitor & Control', 'Execution Stage', 'Closure Stage'],
    'Percentage': [80.0, 100.0, 11.3, 8.0, 0.7]
}
df_completion = pd.DataFrame(completion_data)

fig_completion = px.pie(df_completion, values='Percentage', names='Phase', hole=0.3)
st.plotly_chart(fig_completion, use_container_width=True)