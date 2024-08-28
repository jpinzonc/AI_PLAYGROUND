import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up navigation bar
st.title("TARGET_DASHBOARD")
nav_bar = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Project Status", "Schedule", "Phase"]
)

if nav_bar == "Dashboard":
    # Project status section
    project_status = st.container()
    with project_status:
        st.write("PROJECT STATUS")
        st.write(f"Project Name: {st.session_state.project_name}")
        st.write(f"Cost: ${st.session_state.cost}")
        st.write(f"Percentage Performance: {st.session_state.percentage_performance}%")
        st.write(f"Scheduled Phase: {st.session_state.scheduled_phase}")

# Central part of the dashboard
with st.container():
    # Pie chart section
    pie_chart = st.container()
    with pie_chart:
        fig, ax = plt.subplots()
        ax.pie(st.session_state.task_distribution, labels=st.session_state.task_labels, autopct='%1.1f%%')
        st.pyplot(fig)

    # Waterfall chart section
    waterfall_chart = st.container()
    with waterfall_chart:
        fig, ax = plt.subplots()
        ax.barh(range(len(st.session_state.financial_metrics)), st.session_state.financial_metrics)
        ax.set_yticks(range(len(st.session_state.financial_metrics)))
        ax.set_yticklabels(st.session_state.financial_metric_labels)
        st.pyplot(fig)

    # Bar chart section
    bar_chart = st.container()
    with bar_chart:
        fig, ax = plt.subplots()
        ax.bar(st.session_state.performance_bars, st.session_state.performance_values)
        ax.set_title("Project Performance")
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")
        st.pyplot(fig)

    # Gauge chart section
    gauge_chart = st.container()
    with gauge_chart:
        fig, ax = plt.subplots()
        ax.barh(range(len(st.session_state.task_completion)), st.session_state.task_completion)
        ax.set_yticks(range(len(st.session_state.task_completion)))
        ax.set_yticklabels(st.session_state.task_completion_labels)
        st.pyplot(fig)

# Performance section
performance_section = st.container()
with performance_section:
    st.write("PERFORMANCE")
    st.write(f"Metric 1: {st.session_state.metric_1}")
    st.write(f"Metric 2: {st.session_state.metric_2}")

# KPI panel
kpi_panel = st.container()
with kpi_panel:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.kpi_data)
    ax.set_title("KPI")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    st.pyplot(fig)

    # Stacked column chart section
    stacked_column_chart = st.container()
    with stacked_column_chart:
        fig, ax = plt.subplots()
        ax.bar(st.session_state.stacked_column_labels, st.session_state.stacked_column_values)
        ax.set_title("Stacked Column Chart")
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")
        st.pyplot(fig)

# Table section
table_section = st.container()
with table_section:
    df = pd.DataFrame({
        "Task": st.session_state.tasks,
        "Status": st.session_state.statuses,
        "Due Date": st.session_state.due_dates
    })
    st.write(df)