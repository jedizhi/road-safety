import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_gsheets import GSheetsConnection

# Set page configuration
st.set_page_config(
    page_title="Jafurah Weekly Road Safety Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Function to load and clean data (reusing logic from preprocess.py)
@st.cache_data
def load_data(sheet_url):
    # Read the Google Sheet, skipping the first row which is just a title
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=sheet_url, header=None, skiprows=1)
    except Exception as e:
        st.error(f"Error reading Google Sheet: {e}")
        return pd.DataFrame()
    
    # Row 1 contains Week labels: "Week 15", "Week 16", etc.
    weeks = df.iloc[1].values
    
    # Data starts from row 2
    data = df.iloc[2:].copy()
    
    records = []
    for index, row in data.iterrows():
        activity = row[1]
        if pd.isna(activity):
            continue
            
        # Iterate through pairs of columns starting from index 2
        for i in range(2, len(row), 2):
            week_label = weeks[i]
            if pd.isna(week_label) and i > 0:
                week_label = weeks[i-1]
                
            if pd.isna(week_label):
                continue
                
            trainings = row[i]
            attendees = row[i+1]
            
            # Convert to numeric, handle NaNs
            try:
                trainings = float(trainings) if not pd.isna(trainings) else 0
                attendees = float(attendees) if not pd.isna(attendees) else 0
            except:
                trainings = 0
                attendees = 0
                
            records.append({
                'Activity': str(activity).strip(),
                'Week': str(week_label).strip(),
                'Trainings': trainings,
                'Attendees': attendees
            })
            
    return pd.DataFrame(records)

# --- APP START ---

st.title("🚗 Weekly Road Safety Dashboard")
st.markdown("### SINOHYDRO Road Safety Data Visualization")

# Google Sheet URL
sheet_url = 'https://docs.google.com/spreadsheets/d/143nWa-JslTihcEGuXkuCrMmzznO7ga13Rl0omYJYUuY/edit?gid=658628159#gid=658628159'

# Load Data
df = load_data(sheet_url)

if df.empty:
    st.warning("No data found or file could not be loaded.")
else:
    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # Activity Filter
    all_activities = sorted(df['Activity'].unique())
    selected_activities = st.sidebar.multiselect(
        "Select Activities",
        options=all_activities,
        default=all_activities[:0] if len(all_activities) > 5 else all_activities
    )
    
    # Week Filter
    all_weeks = sorted(df['Week'].unique(), key=lambda x: int(x.split()[-1]) if 'Week' in x else 0)
    selected_weeks = st.sidebar.select_slider(
        "Select Week Range",
        options=all_weeks,
        value=(all_weeks[0], all_weeks[-1])
    )
    
    # Filter Data
    start_week_idx = all_weeks.index(selected_weeks[0])
    end_week_idx = all_weeks.index(selected_weeks[1])
    filtered_weeks = all_weeks[start_week_idx : end_week_idx + 1]
    
    mask = (df['Activity'].isin(selected_activities)) & (df['Week'].isin(filtered_weeks))
    filtered_df = df[mask]

    # --- Metrics ---
    total_attendees = filtered_df['Attendees'].sum()
    total_trainings = filtered_df['Trainings'].sum()
    avg_attendees_per_week = total_attendees / len(filtered_weeks) if filtered_weeks else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Attendees", f"{int(total_attendees)}")
    col2.metric("Total Trainings/Campaigns", f"{int(total_trainings)}")
    col3.metric("Avg Attendees / Week", f"{avg_attendees_per_week:.1f}")

    st.divider()

    # --- Visualizations ---
    
    # 1. Attendees by Activity (Bar Chart)
    fig_activity = px.bar(
        filtered_df.groupby('Activity')['Attendees'].sum().reset_index(),
        x='Activity',
        y='Attendees',
        title="Total Attendees by Activity",
        color='Activity',
        text_auto=True
    )
    st.plotly_chart(fig_activity, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # 2. Trends over Weeks (Line Chart)
        weekly_trend = filtered_df.groupby('Week')['Attendees'].sum().reset_index()
        # Sort weekly_trend by week number
        weekly_trend['Week_Num'] = weekly_trend['Week'].apply(lambda x: int(x.split()[-1]) if 'Week' in x else 0)
        weekly_trend = weekly_trend.sort_values('Week_Num')
        
        fig_trend = px.line(
            weekly_trend,
            x='Week',
            y='Attendees',
            title="Weekly Attendee Trend",
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        # 3. Trainings by Activity (Pie Chart)
        trainings_dist = filtered_df.groupby('Activity')['Trainings'].sum().reset_index()
        trainings_dist = trainings_dist[trainings_dist['Trainings'] > 0]
        
        fig_pie = px.pie(
            trainings_dist,
            values='Trainings',
            names='Activity',
            title="Distribution of Trainings/Campaigns",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Data Table ---
    with st.expander("View Raw Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")
    st.caption("Dashboard generated from Weekly Road Safety Data.xlsx")
