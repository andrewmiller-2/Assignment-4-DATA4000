import requests
import json
import pandas as pd
from datetime import datetime
import time

# --- Configuration ---
BASE_URL = "https://api.doge.gov/savings/grants"
HEADERS = {"accept": "application/json"}
PAGE_SIZE = 100 # Max per_page allowed by the API
SORT_PARAMS = "sort_by=date&sort_order=desc"
MAX_RETRIES = 5
RETRY_DELAY = 5 # seconds

def fetch_all_grants():
    """
    Extracts ALL grant data from the Doge API by iterating through pages.
    """
    print("🚀 Starting data extraction from Doge API...")
    all_grants = []
    page = 1
    total_grants = 0
    
    while True:
        url = f"{BASE_URL}?{SORT_PARAMS}&page={page}&per_page={PAGE_SIZE}"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, headers=HEADERS, timeout=30)
                
                # Check for successful response
                if response.status_code == 200:
                    data = response.json()
                    
                    # Access the grants list
                    current_grants = data.get("result", {}).get("grants", [])
                    
                    if not current_grants:
                        print(f"✅ Reached last page (Page {page}). Total grants extracted: {total_grants}")
                        return all_grants

                    all_grants.extend(current_grants)
                    total_grants += len(current_grants)
                    print(f"  -> Successfully fetched Page {page}. Total grants collected: {total_grants}")
                    
                    page += 1
                    break # Break retry loop on success
                
                # Handle API errors (e.g., rate limiting, server error)
                else:
                    print(f"⚠️ Error on Page {page}: Status {response.status_code}. Retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
            
            except requests.exceptions.RequestException as e:
                print(f"❌ Connection Error on Page {page}: {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
        
        else:
            print(f"❌ Failed to fetch page {page} after {MAX_RETRIES} attempts. Stopping extraction.")
            return all_grants
            
        # Optional: Add a small delay between requests to be polite to the API
        time.sleep(0.5)
        

def create_savings_summary(df):
    """
    Creates a summary DataFrame showing the sum of 'savings' by month and year.
    """
    
    # 1. Convert 'date' column to datetime objects
    # The 'date' column in the original data should be in a standard format (e.g., ISO 8601)
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Extract Month and Year for grouping
    df['YearMonth'] = df['date'].dt.to_period('M')
    
    # 3. Group by the YearMonth and sum the 'savings'
    summary_df = df.groupby('YearMonth')['savings'].sum().reset_index()
    
    # 4. Rename columns and reformat YearMonth for display
    summary_df.columns = ['Year_Month', 'Total_Savings']
    summary_df['Year_Month'] = summary_df['Year_Month'].astype(str)
    
    return summary_df


if __name__ == "__main__":
    # 1. Extract ALL grant data
    grants_data = fetch_all_grants()
    
    if not grants_data:
        print("\n🛑 No grant data was extracted. Exiting.")
    else:
        # 2. Convert to Pandas DataFrame
        df_grants = pd.DataFrame(grants_data)
        
        # Display the head of the full dataset
        print("\n--- Extracted Grants Data (Head) ---")
        print(df_grants.columns) # Print all column names
        print(df_grants.head()) # Print the first few rows with all data
        print(f"\nTotal records in DataFrame: {len(df_grants)}")
        
        # 3. Create the Summary DataFrame
        df_summary = create_savings_summary(df_grants)
        
        # Display the Summary
        print("\n--- Summary: Total Savings by Month/Year ---")
        print(df_summary)
        
        # 4. Optional: Save results to CSV
        df_grants.to_csv("doge_all_grants.csv", index=False)
        df_summary.to_csv("doge_savings_summary.csv", index=False)