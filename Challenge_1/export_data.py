import pandas as pd
from datetime import datetime, timedelta

# Define start and end times
start_time = datetime.strptime("14:45:00", "%H:%M:%S")
end_time = datetime.strptime("15:50:40", "%H:%M:%S")

# Create a time range with a frequency of 4 seconds
time_range = pd.date_range(start=start_time, end=end_time, freq='4S')

# Extract the time part from the datetime objects
time_values = [time.strftime('%H:%M:%S') for time in time_range.time]

# Create a DataFrame with the time column
df = pd.DataFrame({'Time': time_values})

# Export the DataFrame to an Excel file
excel_filename = 'time_data.xlsx'
df.to_excel(excel_filename, index=False)

# Print a message indicating successful export
print(f"DataFrame exported to {excel_filename}")
