
---

# Groq Model Comparison Lab

This is a Streamlit prototype application that allows you to compare responses from two different large language models provided via the [Groq API](https://console.groq.com/).  
It provides side-by-side comparisons of model outputs, response times, and performance metrics.

---

## Features

- Compare outputs from two selected Groq-hosted models
- Built-in models list:
  - `llama-3.1-8b-instant`
  - `gemma2-9b-it`
  - `qwen/qwen3-32b`
  - `openai/gpt-oss-20b`
  - `openai/gpt-oss-120b`
- Adjustable generation parameters:
  - Temperature
  - Response Length (Short, Medium, Long)
- Advanced options:
  - Override `max_tokens`
  - Top P
  - Frequency Penalty
- Response metrics:
  - Token count
  - Response time
  - Speed (words per second)
- Automatic removal of `<think>...</think>` reasoning sections
- API key handling via `.env` file or runtime input in the sidebar

---

## Requirements

- Python 3.9+
- A Groq API key (sign up at [Groq Console](https://console.groq.com/))
- Dependencies listed in `requirements.txt`

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/groq-model-comparison.git
   cd groq-model-comparison
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Groq API key**

   Option A: Create a `.env` file at the project root:

   ```
   GROQ_API_KEY=your_api_key_here
   ```

   Option B: Enter your API key directly in the app sidebar when prompted.

---

## Usage

Run the Streamlit app:

```bash
streamlit run groq_playground.py
```

Then open the displayed URL in your browser (usually `http://localhost:8501`).

---

## Project Structure

```
.
├── groq_playground.py # Main Streamlit application
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
└── .env.example       # Example environment file for API keys
```

---

## Notes

- To prevent truncated outputs, the app uses a **Response Length** dropdown (`Short`, `Medium`, or `Long`).  
  This sets a suitable `max_tokens` value and includes a system instruction to guide the model to fit its response accordingly.  
- `<think>...</think>` tags are automatically removed from model outputs for clarity. This can be adjusted in the code if you want to expose them for debugging.  

---

## License

This project is provided under the MIT License. See the [LICENSE](LICENSE) file for details.

---

