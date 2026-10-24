import os
import streamlit as st
from google import genai

# Configure page
st.set_page_config(
    page_title="AI Study Buddy MVP", page_icon="🎓", layout="centered"
)

st.title("🎓 AI Study Buddy & Quiz Generator")
st.markdown("Your personalized AI tutor powered by advanced prompt engineering.")

# Initialize Gemini Client (Make sure to set your GEMINI_API_KEY environment variable)
# Alternatively, you can use st.text_input for the user to input their key securely in the UI.
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to proceed.")
else:
    client = genai.Client(api_key=api_key)

    # Sidebar mode selection
    mode = st.sidebar.selectbox(
        "Choose Mode", ["Concept Explainer (Persona)", "Quiz Generator (Few-Shot)"]
    )

    if mode == "Concept Explainer (Persona)":
        st.subheader("💡 Learn a Tough Concept")
        topic = st.text_input(
            "What topic or concept are you trying to learn?"
        , placeholder="e.g., Quantum Computing, Backpropagation, Photosynthesis"
        )

        if st.button("Explain to Me"):
            if topic:
                with st.spinner("Professor Alex is thinking..."):
                    # --- PERSONA PATTERN ---
                    prompt = f"""
                    [Role]
                    Act as Professor Alex, an enthusiastic, supportive, and world-class tutor. Your teaching style relies on the Feynman Technique: clear language, zero unnecessary jargon, and memorable real-world analogies.

                    [Task]
                    Explain the following concept to a college student: {topic}.

                    [Tone]
                    Encouraging, clear, and engaging. Use formatting (bullet points, bold text) to make it easy to read.
                    """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash", contents=prompt
                    )
                    st.markdown("### 👨‍🏫 Professor Alex says:")
                    st.write(response.text)
            else:
                st.error("Please enter a topic.")

    elif mode == "Quiz Generator (Few-Shot)":
        st.subheader("📝 Test Your Knowledge")
        subject = st.text_area(
            "Paste your study notes or type a subject area:"
        , placeholder="Paste notes here..."
        )

        if st.button("Generate Quiz"):
            if subject:
                with st.spinner("Generating quiz questions..."):
                    # --- FEW-SHOT PATTERN ---
                    prompt = f"""
                    You are an expert quiz creator. Generate 2 multiple-choice questions based on the provided text. Follow the exact format shown in the examples below.

                    [Example 1]
                    Input Text: Photosynthesis is the process used by plants to convert light energy into chemical energy.
                    Output:
                    Q1: What is the primary purpose of photosynthesis?
                    A) To produce carbon dioxide
                    B) To convert light energy into chemical energy
                    C) To absorb water from roots
                    D) To release thermal energy
                    Correct Answer: B
                    Explanation: Photosynthesis converts solar energy into chemical energy stored in glucose.

                    [Target Input Text]
                    {subject}

                    Generate the quiz now following the format above:
                    """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash", contents=prompt
                    )
                    st.markdown("### 📋 Practice Quiz:")
                    st.write(response.text)
            else:
                st.error("Please provide study notes or a subject.")