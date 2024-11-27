import streamlit as st
import random
import time
from typing import Any
from dataclasses import dataclass

GEN_DELAY = 0.1
DEBUG = False

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file" not in st.session_state:
    st.session_state.file = None


st.title("Simple chat")
history_container = st.container()
user_input_container = st.container()
if DEBUG:
    debug_container = st.expander("Debug")


@dataclass
class ChatMessage:
    author: str
    content: Any


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(GEN_DELAY)


def log_message(author, content):
    message = ChatMessage(author, content)
    st.session_state.messages.append(message)


def foo(text):
    st.write(text)


def active_buttons(options):
    cols = st.columns(len(options))
    for col, option in zip(cols, options):
        if col.button(option, on_click=foo, args=(option,)):
            return option


def log_audio():
    log_message("user", file)


# Display chat messages from history on app rerun
with history_container:
    for message in st.session_state.messages:
        with st.chat_message(message.author):
            if isinstance(message.content, str):
                st.markdown(message.content)
            else:
                st.audio(message.content)
            # elif isinstance(message.content, bytes):
            #     st.audio(message.content, format="audio/wav")

# Accept user input
with user_input_container:
    prompt = st.chat_input("What is up?")
    with st.expander("Upload file"):
        file = st.file_uploader("Upload file", type=["wav"], on_change=log_audio)


if prompt or file:
    if prompt:
        # Display user message in chat message container
        with history_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        # Add user message to chat history
        log_message("user", prompt)

        with history_container:
            with st.chat_message("ai"):
                response = st.write_stream(response_generator())

        # Add assistant response to chat history
        log_message("ai", response)

if DEBUG:
    with debug_container:
        "### Chat history"
        for message in st.session_state.messages:
            st.write(message)
