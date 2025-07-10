import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("synthetic_visitor_data_with_formatted_times.csv")

# 🧼 Fix the Date column formatting
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%Y-%m-%d')

# 🏷️ Page Title
st.set_page_config(page_title="Visitor Management Dashboard", layout="wide")
st.title("🏢 Visitor Management Dashboard")

# 📆 Date Range Filter
st.sidebar.header("📅 Filter by Date")
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter based on selected range
filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]

# 📊 KPI Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Visitors", len(filtered_df))
col2.metric("❌ Blacklisted", filtered_df[filtered_df['Blacklisted'] == 'Yes'].shape[0])
col3.metric("📈 Avg Age", round(filtered_df['Age'].mean(), 1))

# 🎯 Purpose of Visit Pie Chart
st.subheader("🎯 Purpose of Visit Distribution")
fig1 = px.pie(filtered_df, names='Purpose of Visit', title='Purpose of Visits')
st.plotly_chart(fig1, use_container_width=True)

# 🧑‍🤝‍🧑 Gender Distribution
st.subheader("🧑‍🤝‍🧑 Gender Distribution")
fig2 = px.bar(filtered_df, x='Gender', title='Visitors by Gender', color='Gender')
st.plotly_chart(fig2, use_container_width=True)

# 🕒 Check-In Time Distribution
st.subheader("🕒 Check-In Time Distribution")
fig3 = px.histogram(filtered_df, x='Check-In Time', title='Check-In Times (e.g., 11 AM, 1 PM)')
st.plotly_chart(fig3, use_container_width=True)

# 🧮 Calculate visit duration (in minutes)
# First, convert Check-In and Check-Out times back to datetime (for same day dummy date)
df['Check-In Time DT'] = pd.to_datetime(df['Check-In Time'], format='%I %p', errors='coerce')
df['Check-Out Time DT'] = pd.to_datetime(df['Check-Out Time'], format='%I %p', errors='coerce')

# Handle overnight cases (if any)
df['Duration (mins)'] = (df['Check-Out Time DT'] - df['Check-In Time DT']).dt.total_seconds() / 60
df['Duration (mins)'] = df['Duration (mins)'].fillna(0).apply(lambda x: x if x >= 0 else x + 720)  # Fix negative durations

# Merge this back to the filtered data
filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]

# 🕓 Duration Plot
st.subheader("🕓 Visitor Duration (in Minutes)")
fig4 = px.histogram(filtered_df, x='Duration (mins)', nbins=20, title='Distribution of Visit Durations')
st.plotly_chart(fig4, use_container_width=True)

# 📋 Visitor Table
st.subheader("📋 Visitor Records")
st.dataframe(filtered_df)

