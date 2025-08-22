# import streamlit as st
# from retriever import LegalChatbot
# import time
# from typing import Dict, Any

# # Custom CSS for professional appearance
# PROFESSIONAL_CSS = """
# <style>
#     :root {
#         --primary-color: #2e5984;
#         --secondary-color: #f0f7ff;
#     }
    
#     .stApp {
#         max-width: 900px;
#         margin: 0 auto;
#         padding-top: 2rem;
#     }
    
#     .header {
#         color: var(--primary-color);
#         border-bottom: 1px solid #eee;
#         padding-bottom: 1rem;
#         margin-bottom: 1.5rem;
#     }
    
#     .stChatMessage {
#         padding: 1rem 1.25rem;
#         border-radius: 0.75rem;
#         margin: 0.75rem 0;
#         line-height: 1.6;
#         font-size: 0.95rem;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.1);
#     }
    
#     .stChatMessage.user {
#         background-color: #f8f9fa;
#         margin-left: 15%;
#         border-left: 4px solid var(--primary-color);
#     }
    
#     .stChatMessage.assistant {
#         background-color: var(--secondary-color);
#         margin-right: 15%;
#         border-left: 4px solid var(--primary-color);
#     }
    
#     .stChatInputContainer {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         padding: 1rem;
#         background: white;
#         box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
#     }
    
#     .disclaimer {
#         font-size: 0.8rem;
#         color: #666;
#         text-align: center;
#         margin-top: 2rem;
#         padding-top: 1rem;
#         border-top: 1px solid #eee;
#     }
    
#     .spinner-container {
#         display: flex;
#         justify-content: center;
#         padding: 1rem 0;
#     }
# </style>
# """

# def display_typing_effect(message, placeholder):
#     """Simulate typing effect for professional presentation"""
#     full_response = ""
    
#     # Split by sentences for more natural typing
#     sentences = message.split('. ')
#     for sentence in sentences:
#         if not sentence.endswith('.'):
#             sentence += '. '
#         for word in sentence.split():
#             full_response += word + " "
#             time.sleep(0.03)  # Adjust typing speed
#             placeholder.markdown(full_response + "▌")
    
#     placeholder.markdown(full_response)

# def main():
#     st.set_page_config(
#         page_title="Legal AI Assistant",
#         page_icon="⚖️",
#         layout="centered",
#         initial_sidebar_state="collapsed"
#     )
    
#     st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)
    
#     # App header
#     st.markdown("""
#     <div class="header">
#         <h1 style='margin-bottom: 0.5rem;'>⚖️ Legal AI Assistant</h1>
#         <p style='color: #666; margin-top: 0;'>Professional legal guidance powered by AI</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Initialize chatbot
#     if 'legal_assistant' not in st.session_state:
#         with st.spinner("Initializing legal knowledge base..."):
#             try:
#                 st.session_state.legal_assistant = LegalChatbot()
#             except Exception as e:
#                 st.error(f"Failed to initialize assistant: {str(e)}")
#                 st.stop()
    
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {
#                 "role": "assistant", 
#                 "content": "Hello! I'm your legal AI assistant. How can I help you with your legal inquiry today?"
#             }
#         ]
    
#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
    
#     # Chat input
#     if prompt := st.chat_input("Type your legal question here..."):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         # Display user message
#         with st.chat_message("user"):
#             st.markdown(prompt)
        
#         # Display assistant response
#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
            
#             with st.spinner("Researching legal information..."):
#                 try:
#                     response = st.session_state.legal_assistant.generate_response(prompt)
#                     answer = response["answer"]
                    
#                     # Display with typing effect
#                     display_typing_effect(answer, message_placeholder)
                    
#                     # Add to chat history
#                     st.session_state.messages.append({"role": "assistant", "content": answer})
                
#                 except Exception as e:
#                     error_msg = "Apologies, I encountered a technical difficulty. Please try again shortly."
#                     st.error(error_msg)
#                     st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
#     # Footer disclaimer
#     st.markdown("""
#     <div class="disclaimer">
#         Note: This AI assistant provides general legal information, not professional legal advice. 
#         Consult a qualified attorney for specific legal matters.
#     </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()


import streamlit as st
from retriever import LegalChatbot
import time
import base64

# Custom CSS with full background image (no white box)
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    background_css = f"""
    <style>
        .stApp {{
            background: url(data:image/jpg;base64,{encoded_string}) no-repeat center center fixed;
            background-size: cover;
            color: #e0e0e0; /* Light text for dark background */
        }}
        
        /* Remove white box around main content */
        .main .block-container {{
            background-color: transparent !important;
            box-shadow: none !important;
            padding: 2rem;
        }}
        
        /* Chat message styling */
        .stChatMessage {{
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            margin: 0.75rem 0;
            line-height: 1.6;
            font-size: 0.95rem;
            color: #e0e0e0;
            background: rgba(0, 0, 0, 0.4); /* semi-transparent bg */
        }}
        
        .stChatMessage.user {{
            background: rgba(0, 0, 0, 0.6);
            border-left: 4px solid #4fc3f7;
        }}
        
        .stChatMessage.assistant {{
            background: rgba(0, 0, 0, 0.5);
            border-left: 4px solid #81d4fa;
        }}
        
        /* Chat input */
        .stChatInputContainer {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.7);
            box-shadow: 0 -2px 5px rgba(0,0,0,0.2);
        }}
        
        .header {{
            color: #90caf9;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0px 0px 10px rgba(0,0,0,0.6);
        }}
        
        .disclaimer {{
            font-size: 0.8rem;
            color: #bdbdbd;
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
        }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)


def display_typing_effect(message, placeholder):
    """Simulate typing effect"""
    full_response = ""
    sentences = message.split('. ')
    for sentence in sentences:
        if not sentence.endswith('.'):
            sentence += '. '
        for word in sentence.split():
            full_response += word + " "
            time.sleep(0.03)
            placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)


def main():
    st.set_page_config(
        page_title="Legal AI Assistant",
        page_icon="⚖️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Set background
    set_background_image("legal.jpg")
    
    # Header (no white box)
    st.markdown("""
    <div class="header">
        <h1>⚖️ Legal AI Assistant</h1>
        <p>Professional legal guidance powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'legal_assistant' not in st.session_state:
        with st.spinner("Initializing legal knowledge base..."):
            st.session_state.legal_assistant = LegalChatbot()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your legal AI assistant. How can I help you today?"}
        ]
    
    # Display chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your legal question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Researching legal information..."):
                response = st.session_state.legal_assistant.generate_response(prompt)
                answer = response["answer"]
                display_typing_effect(answer, message_placeholder)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ Note: This AI assistant provides general legal information, not professional legal advice. 
        Consult a qualified attorney for specific legal matters.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
