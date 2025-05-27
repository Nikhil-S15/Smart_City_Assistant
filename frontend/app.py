import streamlit as st
import requests
from typing import List, Dict
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
PAGE_TITLE = "Smart City Information Assistant"
PAGE_ICON = "🏙️"

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "show_context" not in st.session_state:
    st.session_state.show_context = False

# Page setup
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
st.title(PAGE_TITLE)
st.markdown("Ask questions about city services, facilities, transportation, and policies.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.session_state.show_context = st.checkbox(
        "Show source documents", 
        value=st.session_state.show_context
    )
    
    st.markdown("---")
    st.markdown("### Categories")
    categories = ["All", "Services", "Facilities", "Transport", "Policies", "Emergency"]
    selected_category = st.selectbox("Filter by category", categories)
    
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()

# Chat interface
def display_chat():
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if st.session_state.show_context and message.get("sources"):
                with st.expander("Source Documents"):
                    for doc in message["sources"]:
                        st.markdown(f"**{doc['metadata'].get('title', 'Document')}**")
                        st.markdown(doc["text"])
                        st.markdown("---")

def add_message(role: str, content: str, sources: List[Dict] = None):
    st.session_state.conversation.append({
        "role": role,
        "content": content,
        "sources": sources,
        "timestamp": datetime.now().isoformat()
    })

# Display chat history
display_chat()

# User input
if prompt := st.chat_input("Ask about city services..."):
    add_message("user", prompt)
    st.chat_message("user").markdown(prompt)
    
    try:
        with st.spinner("Searching city knowledge base..."):
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": prompt},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                add_message("assistant", result["response"], result["source_documents"])
                st.rerun()
            else:
                add_message("assistant", f"Error: {response.text}")
                st.rerun()
    except Exception as e:
        add_message("assistant", f"Connection error: {str(e)}")
        st.rerun()