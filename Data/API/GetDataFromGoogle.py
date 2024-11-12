import time
from pytrends.request import TrendReq

# Initialize the pytrends object
pytrends = TrendReq()

# Set the keywords you want to track
pytrends.build_payload(["Attention", "Charlie Puth"], timeframe='now 7-d')

# Try fetching the data with a retry mechanism
retry_attempts = 5
for attempt in range(retry_attempts):
    try:
        data = pytrends.interest_over_time()
        if not data.empty:
            print(data)
            break
        else:
            print("No data available for the given keywords.")
            break
    except Exception as e:
        print(f"Error: {e}. Retrying in 60 seconds...")
        time.sleep()  # Wait for 60 seconds before retrying
