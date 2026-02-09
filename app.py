import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

st.set_page_config(page_title="OpenAI Q&A", page_icon="💬")
st.title("OpenAI Q&A")
st.caption("Ask a question and get an answer from the OpenAI API.")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY is missing. Set it in .env and restart the app.")
    st.stop()

client = OpenAI()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your question")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.responses.create(
                model="gpt-5",
                input=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    *st.session_state.messages,
                ],
            )
            answer = response.output_text
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
