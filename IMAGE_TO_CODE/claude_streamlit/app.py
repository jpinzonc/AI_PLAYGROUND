import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Project Status Dashboard", layout="wide")

# Title
st.title("Project Status Dashboard")

# Project info
st.sidebar.text("Project Name: IT Career map")
st.sidebar.text("Project Phase: 2 selected")

# Layout
col1, col2 = st.columns(2)

# Project Cost Performance
with col1:
    st.subheader("Project Cost Performance")
    
    total_budget = 93332
    actual_cost = 48048
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=actual_cost,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Actual Cost"},
        gauge={
            'axis': {'range': [None, total_budget]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, total_budget * 0.33], 'color': "lightgreen"},
                {'range': [total_budget * 0.33, total_budget * 0.66], 'color': "yellow"},
                {'range': [total_budget * 0.66, total_budget], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total_budget
            }
        }
    ))
    st.plotly_chart(fig)
    
    st.metric("Total Budget", f"${total_budget:,}")
    st.metric("Actual Cost", f"${actual_cost:,}")

# Project Performance
with col2:
    st.subheader("Project Performance")
    
    col2a, col2b = st.columns(2)
    
    with col2a:
        st.metric("SPI", "0.89", delta="-0.11")
    with col2b:
        st.metric("CPI", "0.87", delta="-0.13")
    
    st.metric("Planned Value (PV)", "$46,666.00")
    st.metric("Earned Value (EV)", "$41,579.40")

# Time vs Project phase
st.subheader("Time vs Project phase")

phase_data = {
    'Phase': ['Closure Stage', 'Execution Stage', 'Monitor & Control', 'Project Initiation Stage', 'Project Planning Stage'],
    'Hours': [5, 164, 36, 40, 144]
}
phase_df = pd.DataFrame(phase_data)

fig = go.Figure(go.Bar(
    x=phase_df['Hours'],
    y=phase_df['Phase'],
    orientation='h'
))
fig.update_layout(height=300)
st.plotly_chart(fig)

# Project Phase % Completed
st.subheader("Project Phase % Completed")

completed_data = {
    'Phase': ['Project Planning Stage', 'Project Initiation Stage', 'Monitor & Control', 'Execution Stage'],
    'Percentage': [80.0, 11.3, 5.0, 3.7]
}
completed_df = pd.DataFrame(completed_data)

fig = go.Figure(go.Pie(
    labels=completed_df['Phase'],
    values=completed_df['Percentage'],
    hole=0.3
))
fig.update_layout(height=300)
st.plotly_chart(fig)