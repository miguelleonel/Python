# Credit goes to ChatGPT for this. Only had to prompt it with basic 3 minute interval, 48 hour logger for this website, feeding it a snippet of relevant HTML code from inspecting website. 
# Logs data into "occupancy.log" in format of 10-23-2024, 05:53PM: 1023
# Planning to better visualize and log the rec center occupancy, better than what Google reflects from the "Popular times" feature. Personal use. 
output_file = 'occupancy.log'

import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime, timedelta

def log_occupancy():
    url = 'https://portal.campusrec.utsa.edu/facilityoccupancy'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        occupancy_element = soup.find('canvas', {'data-occupancy': True})
        
        if occupancy_element:
            occupancy_value = occupancy_element['data-occupancy']
            timestamp = datetime.now().strftime("%m-%d-%Y, %I:%M%p")
            with open(output_file, 'a') as file:
                file.write(f"{timestamp}: {occupancy_value}\n")
            print(f"Logged occupancy: {timestamp}: {occupancy_value}")
        else:
            print("Occupancy element not found.")
    else:
        print(f"Failed to retrieve data: {response.status_code}")

print("Occupancy logger started. Logging every 3 minutes for 48 hours...")

# Set duration for logging (48 hours)
end_time = datetime.now() + timedelta(hours=48)

# Log immediately when the program is started. 
log_occupancy()

# Schedule the logging every 3 minutes
schedule.every(3).minutes.do(log_occupancy)

while datetime.now() < end_time:
    schedule.run_pending()
    time.sleep(1)

# The following would make more sense at first glance, but not as flexible. Schedule allows for running tasks at specific times and handle errors without stopping program. 
# Would not make use of the schedule module/functions. 
'''
# Loop for 48 hours 
while datetime.now() < end_time:
    time.sleep(180)  # Wait for 3 minutes
    log_occupancy()
'''

print("48 hours of logging completed.")

