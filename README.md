# 🚗 Jafurah Weekly Road Safety Dashboard

A dynamic, interactive web dashboard built with **Streamlit** to visualize weekly road safety data for SINOHYDRO. 

This application connects directly to a live Google Spreadsheet to fetch up-to-date data on safety campaigns, trainings, and attendees, presenting the information through clean, responsive charts and metrics.

## Features

- **Live Data Integration:** Pulls data directly from a public Google Sheet using `st-gsheets-connection`, ensuring the dashboard is always up to date.
- **Interactive Filtering:** Use the sidebar to filter the data by specific activities or select a range of weeks to analyze.
- **Key Metrics Overview:** Instantly view Total Attendees, Total Trainings/Campaigns, and Average Attendees per Week.
- **Dynamic Visualizations:**
  - **Bar Chart:** Compare total attendees across different safety activities.
  - **Line Chart:** Track the trend of attendees week over week.
  - **Pie Chart:** View the distribution of training sessions among various activities.
- **Raw Data Access:** Expandable section to view the raw, filtered dataset in a tabular format.
- **Custom Styling:** Features custom CSS injection to style specific UI components (like multiselect tags) and global Streamlit theme configurations via `.streamlit/config.toml`.

## Technologies Used

- **Python**
- **[Streamlit](https://streamlit.io/):** For the web application framework and UI.
- **[Pandas](https://pandas.pydata.org/):** For robust data cleaning and manipulation.
- **[Plotly Express](https://plotly.com/python/plotly-express/):** For rendering interactive, high-quality charts.
- **Streamlit GSheets Connection:** To connect the app to the Google Sheets backend.

## Local Setup & Installation

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jedizhi/road-safety.git
   cd road-safety
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run road_safety_dashboard.py
   ```

5. **View the App:** Open your web browser and navigate to `http://localhost:8501`.

## Deployment

This application is designed to be easily deployed on **Streamlit Community Cloud**.
1. Push your code to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Create a new app, link your GitHub repository, and select `road_safety_dashboard.py` as the main file path.

## Repository Structure
- `road_safety_dashboard.py`: The main Streamlit application file.
- `preprocess.py` / `road_safety_app.py`: Standalone scripts used initially for testing the data cleaning logic.
- `requirements.txt`: Python package dependencies.
- `.streamlit/config.toml`: Global theme settings for the dashboard.
- `.gitignore`: Specifies intentionally untracked files to ignore for Git version control.
