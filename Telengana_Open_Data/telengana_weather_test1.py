import requests
import pandas as pd

# List of UUIDs for each month (based on the examples in your API documentation)
month_uuids = {
    "January 2023": "f498922f-5f2a-5435-95ff-1ee2ef1daf0a",
    "February 2023": "7c44d0ee-2b79-5559-a731-7335f045b518",
    "March 2023": "37915cb6-4f25-5395-ae1f-a50b7bbc2ed5",
    "April 2023": "95202e68-eae2-5b45-804b-115371f36f0a",
    "May 2023": "8d28c0b5-bde9-550a-9eba-3f44701699b7",
    "June 2023": "642539b8-e5f8-5a69-83f1-5d2307c27581",
    "July 2023": "482aea6c-8b0c-5da4-a2db-f13b13e335a3",
    "August 2023": "24bd47a3-5180-577a-bc2a-8d3fb95202be",
    "September 2023": "cf870a1b-72a3-5565-b611-52e904494bfa",
    "October 2023": "ac3e867b-d618-51d7-a52b-a82d62a30e99",
    "November 2023": "0e57ec35-cffc-5f6f-9f78-6eb9cda1a344",
    "December 2023": "e2a33576-e9f3-53e0-b67c-6754c6ae4612",
    # "January 2024": "fe0c6566-1b21-56ed-bed5-f775c9696aa7",
    # "February 2024": "a2609fa7-2e17-501d-ba2a-a06fa2b64d5a",
    # "March 2024":"a2609fa7-2e17-501d-ba2a-a06fa2b64d5a",
    # "April 2024": "6f8d6cba-a7db-5ab6-9778-4061708e087d",
    # "May 2024": "4aaea438-f0ad-5c67-bd76-2f0885fba5be",
    # "June 2024":"7b5f5a1a-d97d-589e-baa1-5750dc611741",
    # "July 2024": "f0e5305f-383d-5614-a3ae-56cb980fe6a3"
    # Add more UUIDs as needed
}

# Function to fetch data from the API
def fetch_data(query):
    url = f"https://data.telangana.gov.in/api/1/datastore/sql?query={query}&show_db_columns=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Directly returning the list of dictionaries
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

# Function to process data into a dataframe
def process_data(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y')
    df['month'] = df['date'].dt.strftime('%B')
    df['year'] = df['date'].dt.year
    return df

# Initialize an empty list to hold DataFrames for each month
all_dataframes = []

# Fetch and process data for each month
for month, uuid in month_uuids.items():
    query = f"[SELECT * FROM {uuid}]"
    data = fetch_data(query)
    df = process_data(data)
    all_dataframes.append(df)

# Concatenate all monthly dataframes into one
annual_df = pd.concat(all_dataframes, ignore_index=True)

# Save the combined data to a CSV file
annual_df.to_csv("temperature_data_entire_year.csv", index=False)

# Create month-specific dataframes and save them to CSV files
monthly_dfs = {}
for month, uuid in month_uuids.items():
    df_month = annual_df[annual_df['month'] == month.split()[0]]
    df_month.to_csv(f"temperature_data_{month}.csv", index=False)  # Save each month to a separate CSV file

# Display the combined DataFrame
print("\nData for the entire year:")
print(annual_df.head())
