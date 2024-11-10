# AI Agent for Information Retrieval

An AI-powered tool designed for flexible and efficient information retrieval. This tool allows users to upload a CSV file or connect through the Google Sheets API to gather specific data from online sources. With the ability to select specific columns and choose between predefined searches or custom prompts, this tool offers a versatile solution for retrieving, parsing, and downloading structured information.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Setup Instructions](#setup-instructions)
4. [Usage Guide](#usage-guide)
5. [Technologies Used](#technologies-used)
6. [API and Tool References](#api-and-tool-references)
7. [License](#license)

## Project Overview
This project simplifies data retrieval by leveraging AI to search the web and extract relevant information. After uploading a CSV file or connecting through the Google Sheets API, users can specify a column to retrieve information about and either choose from predefined search options or provide a custom prompt for more personalized results. The results are then parsed into a structured table format, which can be downloaded in Excel or CSV formats.

## Key Features
- **File Upload or Google Sheets Integration**: Users can upload a CSV or connect via Google Sheets API.
- **Column Selection and Search Customization**: Choose a column to search from and specify information to retrieve via preset options or a custom prompt.
- **Automated Web Search**: Utilizes SerpAPI to gather data for each row in the selected column.
- **Data Parsing with Google Gemini**: Results are parsed into a structured table for easy analysis.
- **Downloadable Output**: Data can be downloaded as an Excel or CSV file.

## Setup Instructions
Follow these steps to set up the project locally:

### Prerequisites
1. **Python**: Ensure Python 3.8+ is installed.
2. **API Keys**: Obtain your API keys for SerpAPI and Google Gemini (and Google Sheets if using the Sheets integration).
3. **Libraries**: The required Python packages are listed in `requirements.txt`.

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-agent-info-retrieval.git
   cd ai-agent-info-retrieval
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Configure API Keys:

Create a .env file in the project root directory and add your API keys:
env
Copy code
SERPAPI_KEY=your_serpapi_key
GOOGLE_GEMINI_KEY=your_google_gemini_key
GOOGLE_SHEETS_KEY=your_google_sheets_key
Usage Guide
Start the Application:

bash
Copy code
streamlit run app.py
This will launch the application locally via Streamlit.

Upload or Connect Data:

Upload a CSV file directly or connect through the Google Sheets API.
Select Column and Choose Search Option:

Use the dropdown to select a column for information retrieval.
Choose from predefined search options or enter a custom prompt for targeted results.
Retrieve and Parse Results:

Click Search Results to begin data retrieval using SerpAPI.
Click Parse with LLM to format the results into a structured table using Google Gemini.
Download the Output:

Download the parsed results as an Excel or CSV file.
Technologies Used
Python: Programming language used to build the application.
Streamlit: Framework for building the user interface.
SerpAPI: API for performing web searches and retrieving data.
Google Gemini: Tool for parsing and structuring the retrieved search results.
Google Sheets API (optional): For direct data input from Google Sheets.
API and Tool References
SerpAPI: https://serpapi.com/
Google Gemini: https://cloud.google.com/gemini
Google Sheets API: https://developers.google.com/sheets/api
