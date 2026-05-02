import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    # Read the Excel file, skipping the first row which is just a title
    df = pd.read_excel(file_path, header=None, skiprows=1)
    
    # Row 0 contains column descriptions: "Numbers of weekly trainings / Campaigns" and "Number of
    # Attendees"
    # Row 1 contains Week labels: "Week 15", "Week 16", etc.
    
    col_desc = df.iloc[0].values
    weeks = df.iloc[1].values
    
  # Data starts from row 2
    data = df.iloc[2:].copy()
    
    # Columns 0 and 1 are Sr. No. and Activity
    # Columns 2 and 3 are Week 15 (Trainings, Attendees)
    # Columns 4 and 5 are Week 16 (Trainings, Attendees)
    # and so on...
    
    records = []
    for index, row in data.iterrows():
        sr_no = row[0]
        activity = row[1]
        
        if pd.isna(activity):
            continue
        
        # Iterate through pairs of columns starting from index 2
        for i in range(2, len(row), 2):
            week_label = weeks[i]
            if pd.isna(week_label):
                # Try to find the week label if it's merged (might be in previous column)
                week_label = weeks[i-1] if i > 0 else None
            
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
                'Activity': activity,
                'Week': str(week_label),
                'Trainings': trainings,
                'Attendees': attendees
            })
    return pd.DataFrame(records)
    
if __name__ == "__main__":
    file_path = 'Weekly Road Safety Data.xlsx'
    clean_df = load_and_clean_data(file_path)
    print(clean_df.head(20))
    print(clean_df['Activity'].unique())
    print(clean_df['Week'].unique())