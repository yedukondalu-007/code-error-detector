import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyB13AbJbRv7aTgtMtlHQnwdHLBzxOx-EYY")
llm = genai.GenerativeModel("models/gemini-1.5-flash")
code_review_bot = llm.start_chat(history=[])

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🧑‍💻",
    layout="centered",
)

# Define custom CSS for a modern dark-themed styling
st.markdown(
    """
    <style>
    body {
        background-color: #1f1f2e;
    }
    .main-title {
        font-size: 2.5rem;
        color: #42f5dd;
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #a5a5a5;
        text-align: center;
        margin-bottom: 30px;
    }
    .sidebar-content {
        font-size: 0.95rem;
        color: #d3d3d3;
        line-height: 1.6;
        background-color: #2e2e3d;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #8e8e8e;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #333;
        background-color: #1e1e2c;
    }
    .chat-container {
        background-color: #3b3b4e;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .chat-human {
        color: #d1a36c;
        background-color: #4b4b61;
        border-radius: 8px;
        padding: 10px;
    }
    .chat-ai {
        color: #72f5a5;
        background-color: #283642;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page header
st.markdown(
    """
    <div>
        <h1 class="main-title">🧑‍💻 AI Code Review Assistant</h1>
        <p class="sub-title">Let AI optimize your code, detect bugs, and suggest improvements</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
with st.sidebar:
    st.header("Welcome to the Assistant 👋")
    st.markdown(
        """
        <div class="sidebar-content">
        - 🐞 Detect and fix bugs in your code.<br>
        - 🚀 Optimize your code structure.<br>
        - 💡 Improve your coding skills with AI recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("#### 💻 Supported Languages")
    st.write("- Python\n- Java\n- C\n- C++")
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Code-icon.svg/120px-Code-icon.svg.png",
        width=120,
    )

st.markdown("---")

# Language selection dropdown
language = st.selectbox(
    "🌐 Select Programming Language:",
    ["Python", "Java", "C", "C++"],
    help="Select the language of your code.",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "text": "Welcome! I can help review your code for issues and suggest optimizations. Paste your code below to get started.",
        }
    ]

# Display previous chat messages
for message in st.session_state.messages:
    if message["role"] == "ai":
        st.markdown(f'<div class="chat-container chat-ai">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container chat-human">{message["text"]}</div>', unsafe_allow_html=True)

# Code input section
st.markdown(f"### ✏️ Paste Your {language} Code:")
code = st.text_area("Write or paste your code here:", height=200, placeholder=f"Enter your {language} code...")

# Submit button
if st.button("🚀 Submit for Review"):
    if not code.strip():
        st.error("⚠️ Please provide your code before submitting.")
    else:
        # Display user's code in chat
        st.session_state.messages.append({"role": "human", "text": code})
        st.markdown(f'<div class="chat-container chat-human">{code}</div>', unsafe_allow_html=True)

        with st.spinner("🤖 Analyzing your code..."):
            try:
                # Generate AI response
                prompt = f"Review the following {language} code and suggest improvements:\n\n{code}"
                response = code_review_bot.send_message(prompt)

                # Display AI's response
                st.session_state.messages.append({"role": "ai", "text": response.text})
                st.markdown(f'<div class="chat-container chat-ai">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Developed by Yaswanth Kumar 🧑‍💻</p>
    </div>
    """,
    unsafe_allow_html=True,
)
