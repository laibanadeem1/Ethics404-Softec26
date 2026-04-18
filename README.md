# Ethics404-Softec26

## Overview
Ethics404-Softec26 is an AI-powered Streamlit web application designed to analyze emails, extract relevant information, and manage student profiles. The system uses a modular pipeline architecture, integrating classification and extraction tasks, powered by both the Gemini and Groq APIs.

## Features
- **Interactive Interface:** Built with Streamlit for a seamless user experience.
- **Student Profile Management:** Sidebar interface for viewing and managing student profiles.
- **Email Analysis Pipeline:** Robust processing pipeline for email classification and data extraction.
- **Results Visualization:** Actionable insights displayed via structured result cards.
- **Filtering System:** Expandable section for tracking ignored or filtered emails.

## Project Structure

```text
Ethics404-Softec26/
├── app.py          # UI Entry point; interacts primarily with pipeline.py
├── pipeline.py     # Main processing logic; orchestrates classifier, extractor, and utils
├── classifier.py   # Handles email categorization and filtering
├── extractor.py    # Extracts key entities and data points from email content
├── utils.py        # Shared utility functions
├── gemini.py       # Integration with Gemini AI models
├── groq_client.py  # Integration with Groq AI models
└── .env            # Environment configuration for API keys and settings
```

## Architecture & App Flow (`app.py`)
The main application follows a structured execution flow:
1. **Imports:** Loads necessary modules and the main pipeline.
2. **Page Config:** Initializes Streamlit page settings and layout.
3. **Session State Init:** Sets up variables to maintain state across user interactions.
4. **Sidebar:** Displays the student profile interface.
5. **Main Interface:** Features the main title and a text area for email input.
6. **Analyze Button:** Triggers the evaluation process.
7. **Pipeline Call:** Executes the core logic from `pipeline.py` upon button click.
8. **Results Cards:** Displays the extracted and classified data cleanly.
9. **Ignored Emails:** Expander component to show emails that did not meet processing criteria.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Ethics404-Softec26
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   Ensure you have the required packages installed (e.g., Streamlit, python-dotenv, Groq, and Gemini SDKs).
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: If a `requirements.txt` file is not present, you may need to install packages manually: `pip install streamlit python-dotenv google-generativeai groq`)*

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your API credentials:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

To start the application, run the following command in your terminal:
```bash
streamlit run app.py
```
