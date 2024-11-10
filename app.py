import streamlit as st
import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import requests
import time
import google.generativeai as genai


load_dotenv()
st.title("AI Agent for Information Retrieval")

# Section for CSV File Upload
st.subheader("Upload a CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

main_column = None
data = None

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded data:")
    st.write(data.head())

    # Display column options for selection
    column_options = data.columns.tolist()
    main_column = st.selectbox("Select the main column for entities (e.g., company names)", column_options)
else:
    st.warning("Please upload a CSV file to proceed.")

# Section for Google Sheets Connection
st.subheader("Or, Connect to a Google Sheet")

# Google Sheets Setup
google_sheets_json = os.getenv("GOOGLE_SHEETS_JSON")

gs_main_column = None
google_sheet_data = None

if google_sheets_json:
    try:
        # Convert JSON string to dictionary
        google_sheets_info = json.loads(google_sheets_json)

        # Set up Google Sheets API Credentials
        credentials = service_account.Credentials.from_service_account_info(google_sheets_info)

        # Function to load Google Sheet data
        def load_google_sheet(spreadsheet_id, range_name):
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])
            if not values:
                st.error("No data found.")
            else:
                return pd.DataFrame(values[1:], columns=values[0])

        # Input for Google Sheet ID and range
        sheet_id = st.text_input("Enter Google Sheet ID")
        sheet_range = st.text_input("Enter the Sheet range (e.g., 'Sheet1!A1:D')")

        if sheet_id and sheet_range:
            try:
                google_sheet_data = load_google_sheet(sheet_id, sheet_range)
                st.write("Preview of the Google Sheet data:")
                st.write(google_sheet_data.head())

                # Column selection for Google Sheets data
                gs_column_options = google_sheet_data.columns.tolist()
                gs_main_column = st.selectbox("Select the main column for entities in Google Sheets", gs_column_options)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    except json.JSONDecodeError:
        st.error("Invalid Google Sheets JSON format in .env file.")
else:
    st.info("Please set up your Google Sheets API credentials in the .env file.")

# Function for SerpAPI search
def search_serpapi(query, api_key):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "gl": "us",
        "hl": "en",
        "num": 3  # Limiting to top 3 results
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("search_metadata", {}).get("status") == "Success":
                return data.get("organic_results", [])
            else:
                return []
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred during search: {str(e)}")
        return []

# Section for Custom Query Input
st.subheader("Define Your Information Retrieval Query")

# Determine which dataset is being used
current_data = None
current_main_column = None

if data is not None and main_column:
    current_data = data
    current_main_column = main_column
elif google_sheet_data is not None and gs_main_column:
    current_data = google_sheet_data
    current_main_column = gs_main_column

if current_data is not None and current_main_column:
    # Add a search type selector
    search_type = st.selectbox(
        "What type of information are you looking for?",
        ["Email Address", "Phone Number", "LinkedIn Profile", "Company Website", "Location", "Custom"]
    )
    
    # Custom prompt based on search type
    if search_type == "Custom":
        prompt_template = st.text_input(
            "Enter your custom prompt (use `{}` as a placeholder for the entity):",
            "Find information about `{}`"
        )
        llm_instruction = st.text_input(
            "Enter instruction for the LLM to extract specific information:",
            "Extract the following information:"
        )
    else:
        # Predefined prompts for different search types
        search_prompts = {
            "Email Address": ("Find contact email for `{}`", "Extract the email address:"),
            "Phone Number": ("Find contact phone number for `{}`", "Extract the phone number:"),
            "LinkedIn Profile": ("`{}` company LinkedIn profile", "Extract the LinkedIn profile URL:"),
            "Company Website": ("`{}` official website", "Extract the official website URL:"),
            "Location": ("`{}` company headquarters location", "Extract the company's location/address:")
        }
        prompt_template = search_prompts[search_type][0]
        llm_instruction = search_prompts[search_type][1]
        
        st.info(f"Using search prompt: {prompt_template}")

    if "{" in prompt_template and "}" in prompt_template:
        st.success("Prompt template set successfully!")

        # Section for Performing Web Search
        st.subheader("Perform Web Search")


        serpapi_key = st.text_input("Enter your SerpAPI Key", type="password", value=os.getenv("SERPAPI_KEY", ""))

        if serpapi_key:
            search_button = st.button("Start Search")

            if search_button:
                # Placeholder for storing search results
                search_results = []

                # Progress bar
                progress_bar = st.progress(0)
                total_entities = len(current_data[current_main_column])

                # Iterate over each entity and perform search
                for idx, entity in enumerate(current_data[current_main_column]):
                    query = prompt_template.format(entity)
                    st.write(f"Searching for: {query}")

                    # Perform search using serpapi
                    url = "https://serpapi.com/search"
                    params = {
                        "q": query,
                        "api_key": serpapi_key,
                        "gl": "us",
                        "hl": "en",
                        "num": 5  # Increased to 5 results for better coverage
                    }
                    
                    try:
                        response = requests.get(url, params=params)
                        if response.status_code == 200:
                            data = response.json()
                            results = data.get("organic_results", [])
                            
                            formatted_results = [
                                {
                                    "title": res.get("title"),
                                    "link": res.get("link"),
                                    "snippet": res.get("snippet"),
                                    "displayed_link": res.get("displayed_link", ""),
                                    "position": res.get("position", 0)
                                }
                                for res in results[:5]  # Take top 5 results
                            ]
                        else:
                            formatted_results = []
                            st.error(f"Search failed for {entity}: Status code {response.status_code}")

                    except Exception as e:
                        formatted_results = []
                        st.error(f"Error searching for {entity}: {str(e)}")

                    search_results.append({
                        "entity": entity,
                        "query": query,
                        "results": formatted_results
                    })

                    # Update progress
                    progress = (idx + 1) / total_entities
                    progress_bar.progress(progress)

                    # Respect rate limits
                    time.sleep(1)

                # Save search results to session state
                st.session_state['search_results'] = search_results
                st.success("Web search completed!")

        # Display search results section - Outside the search button condition
        if 'search_results' in st.session_state:
            st.subheader("Search Results")
            
            # Add expand/collapse all buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Expand All Results"):
                    st.session_state['expand_all'] = True
            with col2:
                if st.button("Collapse All Results"):
                    st.session_state['expand_all'] = False

            # Display results for each entity
            for result in st.session_state['search_results']:
                entity = result['entity']
                query = result['query']
                web_results = result['results']

                # Create an expander for each entity
                expand = st.session_state.get('expand_all', False)
                with st.expander(f"Results for: {entity}", expanded=expand):
                    st.write(f"**Search Query:** {query}")
                    
                    if not web_results:
                        st.warning("No results found for this entity.")
                    else:
                        # Display each search result in a card-like format
                        for idx, res in enumerate(web_results, 1):
                            st.markdown("---")
                            st.markdown(f"**Result {idx}:**")
                            
                            # Title with link
                            st.markdown(f"📌 **Title:** [{res['title']}]({res['link']})")
                            
                            # URL
                            st.markdown(f"🔗 **URL:** {res['link']}")
                            
                            # Snippet
                            if res.get('snippet'):
                                st.markdown(f"📝 **Snippet:**\n{res['snippet']}")
                            
                            # Additional metadata if available
                            if res.get('displayed_link'):
                                st.markdown(f"🌐 **Displayed Link:** {res['displayed_link']}")
                            
                            # Add a "Visit Link" button
                            st.markdown(f"[Visit Website]({res['link']})")

        # Section for LLM Parsing with Google Gemini
        if 'search_results' in st.session_state:
            st.subheader("Extract Information Using LLM")

            # Input for Gemini API Key
            gemini_api_key = st.text_input("Enter your Google Gemini API Key", type="password", value=os.getenv("API_KEY", ""))

            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                parse_button = st.button("Start Parsing with LLM")

                if parse_button:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    extracted_data = []

                    progress_bar = st.progress(0)
                    total_results = len(st.session_state['search_results'])

                    for idx, result in enumerate(st.session_state['search_results']):
                        entity = result['entity']
                        web_results = result['results']

                        if not web_results:
                            extracted_info = "No results found."
                        else:
                            # Prepare the prompt for LLM
                            llm_prompt = f"""
                            For the entity "{entity}", analyze the following search results and {llm_instruction}
                            
                            Search Results:
                            """
                            
                            for res in web_results:
                                llm_prompt += f"""
                                Title: {res['title']}
                                URL: {res['link']}
                                Snippet: {res['snippet']}
                                ---
                                """

                            try:
                                response = model.generate_content(llm_prompt)
                                extracted_info = response.text.strip()
                            except Exception as e:
                                st.error(f"Error extracting information for {entity}: {e}")
                                extracted_info = "Extraction failed."

                        extracted_data.append({
                            "Entity": entity,
                            "Extracted Information": extracted_info
                        })

                        # Update progress
                        progress = (idx + 1) / total_results
                        progress_bar.progress(progress)

                    # Save extracted data to session state
                    st.session_state['extracted_data'] = pd.DataFrame(extracted_data)
                    st.success("Information extraction completed!")

        # Display Extracted Data section - Outside the parse button condition
        if 'extracted_data' in st.session_state:
            st.subheader("Extracted Information")
            st.write(st.session_state['extracted_data'])

            # Option to download the data as CSV
            csv = st.session_state['extracted_data'].to_csv(index=False)
            st.download_button(
                label="Download Extracted Data as CSV",
                data=csv,
                file_name='extracted_data.csv',
                mime='text/csv',
            )

            # Option to write back to Google Sheets
            if google_sheet_data is not None:
                write_back = st.button("Write Extracted Data to Google Sheet")

                if write_back:
                    try:
                        # Function to write data to Google Sheets
                        def write_to_google_sheet(spreadsheet_id, range_name, dataframe):
                            service = build('sheets', 'v4', credentials=credentials)
                            sheet = service.spreadsheets()
                            data = [dataframe.columns.tolist()] + dataframe.values.tolist()
                            body = {
                                'values': data
                            }
                            result = sheet.values().update(
                                spreadsheetId=spreadsheet_id,
                                range=range_name,
                                valueInputOption="RAW",
                                body=body
                            ).execute()
                            return result

                        # Define the target sheet and range
                        target_sheet_id = sheet_id
                        target_range = st.text_input("Enter the target range to write data (e.g., 'Sheet1!F1')")

                        if target_sheet_id and target_range:
                            write_to_google_sheet(target_sheet_id, target_range, st.session_state['extracted_data'])
                            st.success("Extracted data written to Google Sheet successfully!")
                        else:
                            st.warning("Please enter the target range to write data.")
                    except Exception as e:
                        st.error(f"An error occurred while writing to Google Sheet: {e}")
else:
    st.info("Please upload a CSV or connect to a Google Sheet and select the main column to define a query.")