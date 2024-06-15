import re
import pandas as pd

def preprocess(data):
    # Corrected message pattern to match the timestamps, user names, and messages accurately
    message_pattern = r'(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s)([^:]+):\s(.*)'
    
    try:
        matches = re.findall(message_pattern, data, re.IGNORECASE)
        if not matches:
            raise ValueError("No matches found. Check the date format in the input data.")

        timestamps = [match[0] for match in matches]
        users = [match[1] for match in matches]
        messages = [match[2] for match in matches]

        data = {
            'Timestamp': timestamps,
            'User': users,
            'Message': messages
        }

        df = pd.DataFrame(data)

        # Correcting the date format
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%y, %I:%M %p - ', errors='coerce')

        # Dropping rows where Timestamp parsing failed
        df.dropna(subset=['Timestamp'], inplace=True)

        df['Year'] = df['Timestamp'].dt.year
        df['Day'] = df['Timestamp'].dt.day
        df['month_num'] = df['Timestamp'].dt.month
        df['Month'] = df['Timestamp'].dt.month_name()
        df['Hour'] = df['Timestamp'].dt.hour
        df['Minute'] = df['Timestamp'].dt.minute
        df['day_name'] = df['Timestamp'].dt.day_name()
        df['month'] = df['Timestamp'].dt.month_name().str.lower()
        
        # Add period column for heatmap
        def get_period(hour):
            if hour == 23:
                return f"{hour}-00"
            elif hour == 0:
                return "00-01"
            else:
                return f"{hour:02d}-{hour+1:02d}"
        
        df['period'] = df['Hour'].apply(get_period)

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
