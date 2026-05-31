# Fake News Detector & Fact-Checker

An AI-powered web application that fact-checks headlines, articles, claims, or URLs in real-time. By leveraging automated DuckDuckGo searches and advanced Groq-hosted LLMs, the system queries the web for current context, synthesizes the search findings, and provides a clear verdict (True, False, or Uncertain) alongside an explanation and fact-check correction.

---

## 🌟 Features

- **Dual-Mode Input**: Paste any news headline, custom claim, or direct website link/URL.
- **Automated Web Search**: Automatically scrapes the web using DuckDuckGo to extract the top source articles.
- **AI-Powered Analysis**: Feeds real-time web context into a Groq-hosted LLM to determine the veracity of the claim.
- **Detailed Fact-Check Report**: Returns a clear badge verdict, a detailed summary explanation, and the "real truth" correction.
- **Search History Database**: Stores previous searches in a local SQLite database using SQLAlchemy, allowing users to revisit past analyses or clear history.
- **Interactive Premium UI**: Designed with glassmorphism, responsive elements, and clean animations (using Inter typography, FontAwesome icons, and custom styling).

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-CORS
- **Database**: SQLite, Flask-SQLAlchemy (for search history persistence)
- **APIs & Scrapers**: 
  - `duckduckgo_search` (retrieving real-time web context)
  - `BeautifulSoup4` & `requests` (scraping article snippets)
  - `groq` (fast AI text generation/reasoning)
- **Frontend**: HTML5, Vanilla CSS3 (custom styling & gradients), JavaScript (DOM manipulation & async fetch)

---

## 📂 Directory Structure

```
├── code/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Custom styles, animations, and responsive layout
│   │   └── js/
│   │       └── script.js       # Front-end API calls, history loading, UI rendering
│   ├── templates/
│   │   └── index.html          # Main HTML structure
│   ├── .env                    # Environment keys (ignored in Git)
│   ├── app.py                  # Flask entrypoint & API endpoints
│   ├── models.py               # Database schemas (SearchHistory)
│   ├── researcher.py           # Core search, scraping, and LLM analysis logic
│   ├── debug_api.py            # Diagnostic script for API & connection testing
│   └── requirements.txt        # Python package dependencies
├── persantation/
│   ├── Synopsis fake news detectore.docx
│   ├── ppt fake news detectore.pptx
│   └── images.jpg
├── .gitignore                  # Git ignore patterns
└── README.md                   # Project documentation
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8 or higher installed.
- A **Groq API Key** (get one at [console.groq.com](https://console.groq.com/)).

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mcjk892/Fake-News-Detector.git
   cd Fake-News-Detector
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv code/.venv
   ```

3. **Activate the Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     code/.venv/Scripts/Activate.ps1
     ```
   - **Windows (CMD)**:
     ```cmd
     code/.venv\Scripts\activate.bat
     ```
   - **Linux/macOS**:
     ```bash
     source code/.venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r code/requirements.txt
   ```

5. **Configure API Keys**:
   Create a `.env` file inside the `code` directory (if it doesn't exist) and add your Groq API key:
   ```env
   GROK_API_KEY="your_groq_api_key_here"
   ```

6. **Run the Application**:
   ```bash
   python code/app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000` to start using the detector.

---

## 🧪 Testing

To test connection to search endpoints and the Groq LLM API, run the included debugger:
```bash
python code/debug_api.py
```
This script will test if your API keys are configured correctly and perform a mock search and fact-check.
