import streamlit as st
import requests
import json

# FastAPI server URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="LangChain AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .response-box {
        color: black;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def call_api(endpoint, data):
    """Generic function to call FastAPI endpoints"""
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to the server. Make sure the FastAPI server is running on localhost:8000"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def main():
    st.title("🤖 LangChain AI Assistant")
    st.markdown("---")
    
    # Sidebar for model selection
    st.sidebar.header("Configuration")
    option = st.sidebar.selectbox(
        "Choose AI Service",
        ["OpenAI", "Ollama (Llama3)"],
        help="Select which AI service to use"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Make sure your FastAPI server is running on http://localhost:8000"
    )
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Essay Generator")
        essay_topic = st.text_input(
            "Enter topic for essay:",
            placeholder="e.g., Climate Change, Artificial Intelligence...",
            key="essay_topic"
        )
        
        if st.button("Generate Essay", key="essay_btn"):
            if essay_topic.strip():
                with st.spinner("Generating essay..."):
                    if option == "OpenAI":
                        data = {"input": {"topic": essay_topic}}
                        result = call_api("essay/invoke", data)
                    else:
                        data = {"input": {"topic": essay_topic}}
                        result = call_api("poem/invoke", data)  # Using poem endpoint for Ollama
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.markdown("### 📄 Generated Essay")
                        st.markdown(f'<div class="response-box">{result["output"]}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter a topic for the essay")
    
    with col2:
        st.subheader("🎭 Poem Generator")
        poem_topic = st.text_input(
            "Enter topic for poem:",
            placeholder="e.g., Love, Nature, Technology...",
            key="poem_topic"
        )
        
        if st.button("Generate Poem", key="poem_btn"):
            if poem_topic.strip():
                with st.spinner("Generating poem..."):
                    if option == "OpenAI":
                        # For OpenAI, we might need to use a different approach since poem is Ollama-only
                        st.info("Poem generation is optimized for Ollama. Using essay endpoint instead.")
                        data = {"input": {"topic": f"Write a poem about: {poem_topic}"}}
                        result = call_api("essay/invoke", data)
                    else:
                        data = {"input": {"topic": poem_topic}}
                        result = call_api("poem/invoke", data)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.markdown("### ✨ Generated Poem")
                        st.markdown(f'<div class="response-box">{result["output"]}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter a topic for the poem")
    
    # Raw API testing section
    st.markdown("---")
    st.subheader("🔧 API Testing")
    
    with st.expander("Test API Endpoints Directly"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Test OpenAI Endpoint"):
                with st.spinner("Testing..."):
                    try:
                        response = requests.get(f"{API_URL}/openai")
                        st.json(response.json())
                    except:
                        st.error("OpenAI endpoint not available")
        
        with col2:
            if st.button("Test Server Health"):
                try:
                    response = requests.get(f"{API_URL}/")
                    st.success(f"Server is running: {response.json()}")
                except:
                    st.error("Server is not responding")
        
        with col3:
            if st.button("View OpenAPI Docs"):
                st.markdown(f"[OpenAPI Documentation]({API_URL}/docs)")

if __name__ == "__main__":
    main()