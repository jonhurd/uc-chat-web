import streamlit as st
import openai
import time

# OpenAI Configuration (Replace with your actual key)
OPENAI_API_KEY = "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"  # Your OpenAI API Key
assistant_id = "asst_YkgNKU6zP0LuzqwI9cAlP05t"
thread_id = "thread_GB0cRlO0yillJVcYCxpL3uxj"

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Define function to send messages
def send_message(message):
    """Send user message to OpenAI Assistant and get response."""
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message)

    # Run the Assistant in the thread
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    # Poll until response is ready
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(2)  # Wait before checking again

    # Retrieve assistant response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    last_message = messages.data[0]
    return last_message.content[0].text.value


# 📌 **Initialize chat history**
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🎯 **Display Chat History**
st.title("University of the Cumberlands Chat Assistant")
st.subheader("Ask anything related to the university!")

# Show previous chat messages
for msg in st.session_state.chat_history:
    st.write(msg)

# 📌 **User Input Section**
user_input = st.text_input("Enter your question:")
if st.button("Ask"):
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(f"**You:** {user_input}")

        # Get Assistant response
        response = send_message(user_input)
        st.session_state.chat_history.append(f"**Assistant:** {response}")

        # Refresh chat display
        st.rerun()  # This forces the UI to update with new messages

# 📌 **Footer**
st.markdown("---")
st.markdown("🛠 Developed by UC Chatbot Team | Powered by OpenAI")

