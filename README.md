<<<<<<< HEAD
# Deep Research AI Agent

This project is a web-based AI chat application designed for deep research. It leverages the power of large language models (specifically Google's Gemini) to provide intelligent answers, summarize documents and web pages, and assist with research tasks.

The application is built with a Python Flask backend and a simple, clean frontend using vanilla JavaScript, HTML, and CSS.

## Features

*   **Interactive Chat:** A user-friendly chat interface to interact with the AI.
*   **File Upload for Context:** Upload documents (PDF, TXT, etc.) to provide context for your questions.
*   **URL Scraping:** Provide a URL to have the AI read and analyze the content of a web page.
*   **AI-Powered Responses:** Get intelligent and context-aware answers from the Gemini model.
*   **Response Summarization:** Each AI response is accompanied by a short, concise summary.
*   **Chat History:** Your conversations are automatically saved and can be revisited or deleted.
*   **Theming:** Switch between light and dark modes for comfortable viewing.

## Installation

Follow these steps to set up and run the project locally.

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)

### 1. Set Up the Environment

Clone the repository or download the project files to your local machine. It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Navigate to the project directory
cd ai_agent

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

The application requires an API key for the Google Gemini model.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your API key to the `.env` file as follows:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual API key.

## Usage

Once the installation is complete, you can run the application.

1.  Make sure your virtual environment is activated.
2.  Run the Flask server:
=======
# Open Deep Research Agent

This is a web-based research agent that can answer questions, summarize text, and perform web searches.

## Features

- **Chat Interface:** A simple, intuitive chat interface for interacting with the agent.
- **File Upload:** Upload documents (PDF, DOCX) to provide context for your questions.
- **Web Scraping:** Provide a URL and the agent will read the content of the page.
- **Web Search:** The agent can perform web searches to answer questions.
- **Summarization:** The agent can summarize long texts and research papers.
- **Chat History:** Your conversations are saved and can be revisited later.

## Running the Application

### Prerequisites

- Python 3.9 or higher
- `pip` for installing Python packages

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/open_deep_research_agent.git
    cd open_deep_research_agent
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**

    Create a `.env` file in the root of the project and add your Google Generative AI API key:

    ```
    GEMINI_API_KEY=your-api-key
    ```

### Running the Development Server
>>>>>>> 8a15bb9 (feat: Deploy on Render)

```bash
python app.py
```

<<<<<<< HEAD
3.  Open your web browser and navigate to:

```
http://127.0.0.1:5001
```

You can now start chatting with the Deep Research AI Agent!

## Project Structure

```
.
├── app.py              # Main Flask application file, handles routing and core logic.
├── document_processor.py # Handles reading and processing uploaded documents.
├── genai_client.py     # Client for interacting with the Google Gemini API.
├── memory.py           # Manages the chat history for different sessions.
├── research_summarizer.py # Logic for summarizing research topics.
├── scraper.py          # Scrapes text content from URLs.
├── search_tool.py      # Provides web search functionality.
├── summarizer.py       # General text summarization utilities.
├── requirements.txt    # Lists the Python dependencies for the project.
├── .env                # (To be created) Stores environment variables like API keys.
├── frontend/           # Contains all frontend files (HTML, CSS, JavaScript).
│   ├── index.html      # The main HTML structure of the chat interface.
│   ├── script.js       # Handles all client-side logic and interactivity.
│   └── style.css       # Styles for the web interface.
├── sessions/           # Stores chat history as JSON files.
└── uploads/            # Default directory for storing uploaded files.

```
=======
The application will be available at `http://localhost:5001`.

## Deployment on Render

This application is configured for deployment on [Render](https://render.com/).

### Prerequisites

- A Render account
- The project pushed to a GitHub repository

### Deployment Steps

1.  **Create a new Web Service on Render.**
2.  **Connect your GitHub repository.**
3.  **Use the following settings:**
    -   **Environment:** `Docker`
    -   **Start Command:** `./run_production.sh`
4.  **Add your `GEMINI_API_KEY` as an environment variable in the Render dashboard.**
5.  **Deploy the application.**

Render will automatically build the Docker image and deploy the application.
>>>>>>> 8a15bb9 (feat: Deploy on Render)
