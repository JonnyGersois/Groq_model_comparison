import os
import streamlit as st
import requests
import re
import time
from dotenv import load_dotenv

# Load .env if available
load_dotenv()

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Available models
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "qwen/qwen3-32b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b"
]

# Get API key – from ENV or sidebar input
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.sidebar.subheader("API Key")
    api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if not api_key:
    st.error("Please provide a Groq API Key to continue.")
    st.stop()


def clean_response(text: str) -> str:
    """
    Remove <think>...</think> sections from model output if present.
    """
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def call_groq(prompt, model, temperature=0.7, max_tokens=400):
    """
    Call Groq API with parameters and measure response time.
    Ensures the model is instructed not to include <think> reasoning,
    and strips any that slip through.
    Returns tuple: (response_text, time_taken)
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Do not include hidden reasoning steps, thought processes, "
                    "or <think> tags in your response. "
                    "Only return the final answer clearly and concisely."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        start_time = time.time()
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload)
        end_time = time.time()
        time_taken = end_time - start_time

        if resp.status_code != 200:
            return f"Error: {resp.status_code} - {resp.text}", 0.0

        data = resp.json()
        response_text = data["choices"][0]["message"]["content"]

        # Clean up leftover <think>...</think> if model still emitted it
        response_text = clean_response(response_text)

        return response_text, time_taken

    except Exception as e:
        return f"Error: {e}", 0.0

# --- Streamlit UI ---
st.set_page_config(page_title="Groq Model Comparison Lab", layout="wide")
st.title("Groq Model Comparison Lab")
st.write("Select any two available Groq models and compare their responses side by side.")


# --- Sidebar with controls ---
st.sidebar.header("Configuration")

# Model selection
st.sidebar.subheader("Model Selection")
model_1 = st.sidebar.selectbox("Model 1", AVAILABLE_MODELS, index=0)
model_2 = st.sidebar.selectbox("Model 2", AVAILABLE_MODELS, index=1)

# Parameters
st.sidebar.subheader("Generation Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)

# Response Length Dropdown (simple UI for most users)
length_option = st.sidebar.selectbox(
    "Response Length",
    ["Short", "Medium", "Long"],
    index=1
)

# Map length choice → token limits
length_map = {
    "Short": 150,
    "Medium": 400,
    "Long": 800
}
max_tokens = length_map[length_option]

# Advanced options (collapsed by default)
with st.sidebar.expander("Advanced Options"):
    st.caption("Note: Options here override defaults. Use only if you know what you're doing 🙂")

    # Max Tokens override
    custom_max_tokens = st.number_input(
        "Max Tokens (override)",
        min_value=50, max_value=2000,
        value=max_tokens, step=50
    )
    if custom_max_tokens != max_tokens:
        max_tokens = custom_max_tokens  # Override

    # Other power user settings
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
    frequency_penalty = st.slider("Frequency Penalty", -2.0, 2.0, 0.0, 0.1)

# User input
user_prompt = st.text_area("Enter your prompt here:", height=100)

# Run button
if st.button("Run Prompt", type="primary"):
    if user_prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        # print(f"Max tokens set to: {max_tokens}")# Just checking
        # Create progress indicator
        with st.spinner(f"Running prompt on {model_1} and {model_2}..."):
            output_1, time_1 = call_groq(
                user_prompt,
                model_1,
                temperature=temperature,
                max_tokens=max_tokens
            )
            output_2, time_2 = call_groq(
                user_prompt,
                model_2,
                temperature=temperature,
                max_tokens=max_tokens
            )

        # Side by side layout
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{model_1}")
            st.info(f"Temperature: {temperature} | Max Tokens: {max_tokens}")
            st.write(output_1)
            if output_1 and not output_1.startswith("Error"):
                word_count = len(output_1.split())
                st.caption(f"Response time: {time_1:.2f} seconds")
                st.caption(f"Word count: {word_count} words")
                if time_1 > 0:
                    st.caption(f"Speed: {word_count/time_1:.1f} words/second")

        with col2:
            st.subheader(f"{model_2}")
            st.info(f"Temperature: {temperature} | Max Tokens: {max_tokens}")
            st.write(output_2)
            if output_2 and not output_2.startswith("Error"):
                word_count = len(output_2.split())
                st.caption(f"Response time: {time_2:.2f} seconds")
                st.caption(f"Word count: {word_count} words")
                if time_2 > 0:
                    st.caption(f"Speed: {word_count/time_2:.1f} words/second")

        # Comparison summary
        if time_1 > 0 and time_2 > 0:
            st.markdown("---")
            faster_model = model_1 if time_1 < time_2 else model_2
            speed_diff = abs(time_1 - time_2)
            speed_ratio = max(time_1, time_2) / min(time_1, time_2)
            st.success(f"{faster_model} was {speed_ratio:.1f}x faster ({speed_diff:.2f}s difference)")

# Footer with tips
st.sidebar.markdown("---")
st.sidebar.markdown("### Tips")
st.sidebar.markdown(
"""
- **Temperature**: Lower = more focused, Higher = more creative  
- **Max Tokens**: Controls response length  
- **Top P**: Probabilistic cutoff (use with Temperature)  
- **Frequency Penalty**: Discourages repetition  
"""
)
st.sidebar.markdown("Developed by [Jon Vaughan](https://github.com/JonnyGersois).")