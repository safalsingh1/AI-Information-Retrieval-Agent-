# AI Information Retrieval Agent

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.24+-red.svg)

## Overview

The AI Information Retrieval Agent is a powerful tool that combines data processing, web scraping, and AI capabilities to extract and analyze information from structured data sources. Built with Streamlit, it offers an intuitive interface for users to process data from CSV files or Google Sheets.

---

## ✨ Key Features

* 📂 **Data Source Integration**
  * CSV file upload support
  * Google Sheets API integration
  * Dynamic column selection

* 🔍 **Search Capabilities**
  * Direct search functionality
  * Custom query support
  * Web scraping via SerpAPI

* 🤖 **AI Processing**
  * Data parsing with Google Gemini
  * Automated table generation
  * Export to CSV/Excel

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-information-retrieval.git
   cd ai-information-retrieval
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

---

## 📁 Project Structure

```
ai-information-retrieval/
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Usage Guide

### Starting the Application

```bash
streamlit run app.py
```

### Basic Workflow

1. **Data Upload**
   * Select data source (CSV/Google Sheets)
   * Choose target column

2. **Search Configuration**
   * Select search type
   * Enter custom query (if needed)

3. **Processing**
   * Click "Search" for web results
   * Use "Parse with LLM" for structured data
   * Download results

## ⚙️ Configuration

### Required API Keys

```env
SERPAPI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials.json
```

### Google Sheets Setup

1. Create GCP project
2. Enable Sheets API
3. Create service account
4. Download credentials

### SerpAPI Setup

1. Register at serpapi.com
2. Get API key
3. Add to .env file

---

## 📚 Dependencies

* `streamlit>=1.24.0`
* `pandas>=1.5.0`
* `google-api-python-client>=2.0.0`
* `serpapi-python>=1.0.0`
* `google-generativeai>=0.1.0`

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
   ```bash
   git checkout -b feature/NewFeature
   ```
3. Commit changes
   ```bash
   git commit -m 'Add NewFeature'
   ```
4. Push to branch
   ```bash
   git push origin feature/NewFeature
   ```
5. Open Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

Your Name - safalsingh@gmail.com](mailto:your.email@example.com)


---

## 🙏 Acknowledgments

* [Streamlit](https://streamlit.io/)
* [SerpAPI](https://serpapi.com)
* [Google Cloud Platform](https://cloud.google.com)
* [Google Gemini](https://ai.google.dev/)
