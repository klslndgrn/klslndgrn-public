import time
from plotting import update_plot
from getdata import fetch_data_from_api

"""
TODO:
- Update data every 10s.
- In 24h window, include current data, yesterdays data, and rolling 7 days average.
- Retrieve Data from API: Write a Python script to fetch data from the API at regular intervals. You can use libraries like requests to make HTTP requests to the API and retrieve data.
- Update Plot: Once you retrieve data from the API, update the plot accordingly. Matplotlib provides functions to update plots dynamically. You can update the data in your plot and then redraw it.
- Continuous Execution: Use a loop in your script to continuously fetch data and update the plot. You can implement this loop using a while loop with a sleep timer to control the update frequency.
- Optimization: Consider optimizing your code to avoid unnecessary API requests or excessive processing. Caching data locally or implementing data streaming techniques can help improve performance and reduce load on the API.
- Error Handling: Implement robust error handling in your script to handle network errors, API rate limits, and other potential issues gracefully.
"""


def run_monitor():
    # Fetch data from API, sleep if unsuccesful.
    while True:
        data = fetch_data_from_api()
        if data is not None:
            update_plot(data)
            time.sleep(10)
        else:
            print("Failed to fetch data. Retrying in 5 minutes...")
            time.sleep(300)  # Wait for 5 minutes before retrying


if __name__ == "__main__":
    run_monitor()
