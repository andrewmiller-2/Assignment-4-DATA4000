import requests
import pandas as pd
import json

# --- Configuration ---
BASE_URL = "https://api.doge.gov/savings/grants"
# Set per_page to a reasonable max (e.g., 100) to minimize the number of API calls
PER_PAGE = 100
# Base parameters for the API call
BASE_PARAMS = {
    "sort_by": "date",
    "sort_order": "desc",
    "per_page": PER_PAGE
}
HEADERS = {"accept": "application/json"}

def get_grants_page(page_number: int) -> list:
    """
    Retrieves a single page of grant data from the Doge API endpoint.

    Args:
        page_number (int): The page number to retrieve.

    Returns:
        list: A list of grant dictionaries for that page, or an empty list if the request fails.
    """
    print(f"Fetching page {page_number}...")
    
    # 1. Prepare parameters, overriding the default page number
    params = BASE_PARAMS.copy()
    params["page"] = page_number

    try:
        # 2. Make the GET request
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        
        response.raise_for_status() 
        
        data = response.json()
        
        # 3. Extract the list of grants (the desired data)
        grants = data.get("result", {}).get("grants", [])
        
        print(f"Successfully retrieved {len(grants)} grants from page {page_number}.")
        return grants
        
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving page {page_number}: {e}")
        return []

if __name__ == "__main__":
        # Prompt user for page number
    try:
        page_num_input = input("Enter the page number to retrieve (e.g., 1): ")
        page_number = int(page_num_input)
        if page_number < 1:
            print("Page number must be 1 or greater.")
            exit()
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        exit()

    page_data = get_grants_page(page_number=page_number)
    
    if page_data:
        # Convert to DataFrame for easy viewing
        df_page = pd.DataFrame(page_data)
        
        # --- DEBUG: Available DataFrame Columns (Kept for reference) ---
        print(f"\n--- DEBUG: Available DataFrame Columns for Page {page_number} ---")
        available_columns = df_page.columns.tolist()
        print("The following columns are available in the data:")
        print(available_columns)
        print("-------------------------------------------------")
        # Display first few rows of selected columns
        try:
            display_columns = ['id', 'amount_awarded', 'recipient_name']
            print("\n--- Grants Data (First 5 Rows - Selected Columns) ---")
            print(df_page[display_columns].head())
        except KeyError:
            print("\n--- Grants Data (First 5 Rows - All Columns Displayed Due to Missing Keys) ---")
            print("To select specific columns, please update the 'display_columns' list in the script")
            print(df_page.head())
