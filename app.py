
import streamlit as st
from huggingface_hub import InferenceClient

st.title("🩺 Health Assistant AI")
st.caption("A helpful medical information chatbot")

HF_TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient(api_key=HF_TOKEN)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful medical assistant. Always include a disclaimer."}]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=st.session_state.messages,
            max_tokens=500
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
