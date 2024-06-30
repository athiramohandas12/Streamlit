import time
import os
import joblib
import streamlit as st

# Create a data/ folder if it doesn't already exist
if not os.path.exists('data/'):
    os.mkdir('data/')

# Load past chats (if available)
try:
    past_chats = joblib.load('data/past_chats_list')
except:
    past_chats = {}

new_chat_id = f'{time.time()}'

# Sidebar allows a list of past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = new_chat_id
    
    # Display past chats as scrollable list
    for chat_id in past_chats.keys():
        if st.button(f'ChatSession-{chat_id}'):
            st.session_state.chat_id = chat_id
    
    if st.button('New Chat'):
        st.session_state.chat_id = new_chat_id
        past_chats[st.session_state.chat_id] = f'ChatSession-{st.session_state.chat_id}'
        joblib.dump(past_chats, 'data/past_chats_list')

st.write('# Chat Interface')

# Chat history (allows to ask multiple questions)
try:
    messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
except:
    messages = []

# Display chat messages from history on app rerun
for message in messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Your message here...'):
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    messages.append(
        dict(
            role='user',
            content=prompt,
        )
    )
    # Save chat history
    joblib.dump(messages, f'data/{st.session_state.chat_id}-st_messages')

    # Placeholder for AI response
    with st.chat_message('ai'):
        response_placeholder = st.empty()
        full_response = "This is a placeholder for AI response."  # Replace with actual AI response if needed
        response_placeholder.markdown(full_response)

    # Add assistant response to chat history
    messages.append(
        dict(
            role='ai',
            content=full_response,
            avatar='✨',
        )
    )
    # Save chat history
    joblib.dump(messages, f'data/{st.session_state.chat_id}-st_messages')
