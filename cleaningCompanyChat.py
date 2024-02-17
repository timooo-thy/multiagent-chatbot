import streamlit as st
import json
import requests
from dotenv import load_dotenv
import os

def save_conversations(conversations, email):
    """Function for saving conversations to JSON file"""

    if not os.path.exists(f'conversations/{email}'):
        os.makedirs(f'conversations/{email}')

    conversations_file = f'conversations/{email}/conversations_history.json'

    with open(conversations_file, 'w') as f:
        json.dump(conversations, f, indent=4)


def load_conversations(email):
    """Function for loading conversations from JSON file"""
    conversations_file = f'conversations/{email}/conversations_history.json'
    if os.path.exists(conversations_file):
        with open(conversations_file, 'r') as f:
            return json.load(f)
    return {"Conversation 1": [
            {"role": "AI", "content": "Hello, I am Robin from Cleaner.io. How may I help you today?"}]}


def change_user():
    st.session_state.messages = load_conversations(st.session_state.email)
    st.session_state.current_conversation = next(
        iter(st.session_state.messages))
    st.session_state.conversation_count = len(
        st.session_state.messages)


def main():

    # Load environment variables
    load_dotenv()

    # App title
    st.set_page_config(
        page_title="Cleaner.io Chatbot by Timothy", page_icon=":robot_face:")

    # Sidebar for Hugging Face credentials, chat history download and buffer memory adjustment
    with st.sidebar:
        st.title('Rescale Lab AI Chatbot')

        email = st.text_input(
            'Enter E-mail:', type='default', on_change=change_user)
        password = st.text_input(
            'Enter password:', type='password')
        if not (email and password):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success(
                'Proceed to entering your prompt message!', icon='👉')

        # Initialise session state for storing current conversation
        if 'email' not in st.session_state:
            st.session_state.email = ""

        if "messages" not in st.session_state or st.session_state.email != email:
            st.session_state.email = email
            st.session_state.messages = load_conversations(email)

        # Initialise session state for storing current conversation
        if 'current_conversation' not in st.session_state:
            st.session_state.current_conversation = next(
                iter(st.session_state.messages))

        # Initialise session state for storing conversation count
        if 'conversation_count' not in st.session_state:
            st.session_state.conversation_count = len(
                st.session_state.messages)

        # Determine if the chat input should be enabled based on the availability of credentials
        is_input_enabled = email and password

        # Sidebar for creating a new conversation
        if st.sidebar.button("Create a new conversation", disabled=not is_input_enabled):
            st.session_state.messages[f"Conversation {st.session_state.conversation_count + 1}"] = [
                {"role": "AI", "content": "Hello, I am Robin from Cleaner.io. How may I help you today?"}]
            st.session_state.conversation_count += 1
            st.session_state.current_conversation = f"""Conversation {
                st.session_state.conversation_count}"""

        # Download chat history button
        chat_history_json = json.dumps(st.session_state.messages, indent=4)
        if st.download_button(
            label="Download current chat history",
            data=chat_history_json,
            file_name=f"{st.session_state.current_conversation}_history.json",
            mime="application/json",
            disabled=not is_input_enabled
        ):
            st.toast("Chat history downloaded!", icon="📥")

        if st.button("Delete chat history", disabled=not is_input_enabled):
            st.toast("Chat history deleted!", icon="🗑️")

            # Delete current conversation
            del st.session_state.messages[st.session_state.current_conversation]

            if len(st.session_state.messages) == 0:
                st.session_state.messages = {"Conversation 1": [
                    {"role": "AI", "content": "Hello, I am Robin from Cleaner.io. How may I help you today?"}]}
                st.session_state.current_conversation = "Conversation 1"
                st.session_state.conversation_count = 1

            else:
                # Update to another existing conversation
                st.session_state.current_conversation = next(
                    iter(st.session_state.messages))

        # Sidebar for selecting conversation
        st.session_state.current_conversation = st.sidebar.selectbox(
            "Select a conversation", list(st.session_state.messages.keys()), index=list(st.session_state.messages.keys()).index(st.session_state.current_conversation))


    # Display existing chat messages
    for message in st.session_state.messages[st.session_state.current_conversation]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input for user prompts
    prompt = st.chat_input(disabled=not is_input_enabled)

    if prompt:
        st.session_state.messages[st.session_state.current_conversation].append(
            {"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from AI
    if st.session_state.messages[st.session_state.current_conversation][-1]["role"] != "AI":
        with st.chat_message("AI"):
            with st.spinner("Generating response..."):
                response = requests.post("http://127.0.0.1:8000/enquire", json={"content": prompt})
                if response.status_code != 200:
                    response = {"response": "Sorry, I am unable to process your request at the moment. Please try again later."}
                else:
                    response = response.json()
        message = {"role": "AI", "content": response['response']}
        st.session_state.messages[st.session_state.current_conversation].append(
            message)
        st.rerun()

        save_conversations(st.session_state.messages, email
                           )


if __name__ == "__main__":
    main()
