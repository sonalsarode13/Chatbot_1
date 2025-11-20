import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"

st.set_page_config(page_title="Chatbot", layout="centered")
st.title("Chatbot")

@st.cache_resource
def load_model():
    model = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        task="conversational",
        max_new_tokens=256
    )
    return ChatHuggingFace(llm=model)

llm = load_model()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful AI Assistant")]
    st.session_state.messages_display = []

for msg in st.session_state.messages_display:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.messages_display.append({"role":"user","content":user_input})
    st.chat_message("user").write(user_input)

    result = llm.invoke(st.session_state.chat_history) 
    ai_reply = result.content if hasattr(result, "content") else result

    st.session_state.chat_history.append(AIMessage(content=ai_reply))
    st.session_state.messages_display.append({"role":"assistant","content":ai_reply})
    st.chat_message("assistant").write(ai_reply)
