import streamlit as st
from transformers import pipeline

# Caching the model to avoid reloading every run
@st.cache_resource
def load_model():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

classifier = load_model()

# Labels to classify
labels = ["faq", "sentiment", "escalation"]

# Page config
st.set_page_config(
    page_title="AI/ML Intent Classifier",
    page_icon="🤖",
    layout="centered",
)

# Sidebar
st.sidebar.title("⚙️ Model Information")
st.sidebar.markdown("""
**Model:** facebook/bart-large-mnli  
**Technique:** Zero-shot learning  
**Library:** 🤗 Transformers  
**Purpose:** Classify customer support queries  
""")
st.sidebar.markdown("---")
st.sidebar.markdown("""
Built with ❤️ using open-source AI.
""")

# Main Title
st.title("🤖 AI/ML Intent Classifier")

# Intro text
st.markdown("""
This app demonstrates a **zero-shot classification model** that predicts customer query intent:

- **faq:** Information requests
- **sentiment:** Positive or negative feedback
- **escalation:** Urgent complaints

Paste or type any text below and click **Classify**.
""")

# Text input
query = st.text_area(
    "✍️ Enter a customer query:",
    placeholder="E.g., I am still waiting for my refund!"
)

# Classify button
if st.button("🚀 Classify Intent"):
    if not query.strip():
        st.warning("⚠️ Please enter a query before running classification.")
    else:
        with st.spinner("Running classification..."):
            result = classifier(query, labels)

        top_label = result["labels"][0]
        scores_md = "\n".join(
            [f"- **{label.capitalize()}**: {round(score * 100, 2)}%" for label, score in zip(result["labels"], result["scores"])]
        )

        # Display output
        st.success(f"**Predicted Intent:** {top_label.capitalize()}")
        st.markdown("### 📊 Detailed Scores")
        st.markdown(scores_md)

        # Workflow explanation
        st.markdown("""
---
### 🛠️ How It Works
1️⃣ The model encodes your text  
2️⃣ Compares it to candidate labels  
3️⃣ Calculates similarity scores  
4️⃣ Outputs the most likely intent
""")

        # Mermaid diagram
        st.markdown("""
---
### 🧩 Orchestrator Workflow Diagram

```mermaid
flowchart TD
    Start([Start])

    Orchestrator[Orchestrator Agent]

    ConvAnalysis[Conversational Analysis Agent<br/>(Sentiment, Intent, Topic)]
    Retrieval[Retrieval Agent]
    VectorDB[(Vector DB)]
    Recommendation[Real-Time Recommendation Agent]
    Human[Human Agent]
    Validation[Performance Validation Agent]
    General[General Query Agent]
    Billing[Billing and Refund Agent]
    Escalation[Escalation Handle Agent]
    Feedback[Feedback Loop Agent]

    Start --> Orchestrator

    Orchestrator --> ConvAnalysis
    Orchestrator --> Retrieval
    Orchestrator --> Recommendation
    Orchestrator --> Validation
    Orchestrator --> General
    Orchestrator --> Billing
    Orchestrator --> Escalation
    Orchestrator --> Feedback

    Retrieval --> VectorDB
    Recommendation --> Human
    Feedback --> ConvAnalysis
""")