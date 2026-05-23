import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

from src.graph import app as agent_workflow

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #f8f9fa; }
.answer-box {
    background: #f0f7ff;
    border-left: 4px solid #1d72b8;
    padding: 1.2rem 1.5rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔍 AI Research Assistant")
st.markdown(
    "**Ask any question** — the AI researches your topic, "
    "a second AI checks the answer for accuracy, and you get a verified result."
)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")

    accuracy_target = st.slider(
        "Minimum accuracy target",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.05,
        help=(
            "The answer is flagged as meeting your standard only when accuracy reaches this level. "
            "The AI internally targets 80% regardless — this setting changes how YOUR result is labeled."
        ),
    )

    if accuracy_target < 0.5:
        badge = "🟡 Quick check"
    elif accuracy_target < 0.75:
        badge = "🟠 Standard"
    else:
        badge = "🟢 Thorough"

    st.caption(f"{badge} — you want at least **{accuracy_target:.0%}** accuracy")

    st.divider()
    st.markdown("**Supported topics**")
    st.markdown(
        "These topics have built-in research data. "
        "Other questions will get a generic answer."
    )
    st.markdown(
        "- 🤖 **Artificial Intelligence**\n"
        "- ⚛️ **Quantum Computing**\n"
        "- 🌍 **Climate Change**\n"
        "- 🏥 **Healthcare & Medicine**\n"
        "- 🚀 **Space Exploration**\n"
        "- 💰 **Crypto & Blockchain**\n"
        "- 🔐 **Cybersecurity**\n"
        "- 🦾 **Robotics & Automation**\n"
        "- ⚡ **Energy & Renewables**\n"
        "- 📚 **Education & EdTech**\n"
        "- 📈 **Economics & Global Economy**\n"
        "- 🧬 **Biotechnology**"
    )
    st.divider()
    st.markdown("**How it works**")
    st.markdown(
        "1. You type a question  \n"
        "2. An AI **researches** your topic  \n"
        "3. A second AI **checks** the answer  \n"
        "4. If accuracy isn't good enough, it tries again  \n"
        "5. You receive the final verified answer"
    )
    st.caption("Runs locally using Ollama — no internet required, but slower than cloud AI.")

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("### What would you like to research?")
with st.form("search_form", border=False):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "Your question",
            placeholder="e.g. AI breakthroughs, space exploration, cybersecurity, biotech...",
            label_visibility="collapsed",
        )
    with col_btn:
        run_clicked = st.form_submit_button("Ask", use_container_width=True, type="primary")

# ── Execution ─────────────────────────────────────────────────────────────────
if run_clicked:
    if not query.strip():
        st.warning("Please enter a question before clicking Ask.")
        st.stop()

    initial_state = {
        "messages": [HumanMessage(content=query.strip())],
        "current_agent": "",
        "verification_score": 0.0,
    }

    with st.spinner("Researching your question — this may take a moment..."):
        try:
            final_state = agent_workflow.invoke(initial_state)
        except Exception as exc:
            st.error(f"Something went wrong. Please try again. ({exc})")
            st.stop()

    messages = final_state.get("messages", [])
    score = final_state.get("verification_score", 0.0)

    # Separate researcher vs verifier messages.
    # Pattern after the initial HumanMessage: researcher, verifier, researcher, verifier…
    researcher_msgs = []
    verifier_msgs = []
    ai_index = 0
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.content:
            if ai_index % 2 == 0:
                researcher_msgs.append(msg)
            else:
                verifier_msgs.append(msg)
            ai_index += 1

    st.divider()

    # ── Result banner ──────────────────────────────────────────────────────────
    if score >= accuracy_target:
        st.success(
            f"Answer verified — accuracy **{score:.0%}**, meets your {accuracy_target:.0%} target."
        )
    else:
        st.warning(
            f"Research complete, but accuracy ({score:.0%}) is below your target ({accuracy_target:.0%}). "
            "Try lowering the accuracy target or asking a more specific question."
        )

    st.progress(min(score, 1.0), text=f"Accuracy: {score:.0%}")

    # ── Final answer ───────────────────────────────────────────────────────────
    st.markdown("### Answer")
    if researcher_msgs:
        st.markdown(
            f'<div class="answer-box">{researcher_msgs[-1].content}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No answer was produced. Please try again.")

    # ── Verification details (collapsed by default) ────────────────────────────
    rounds = len(verifier_msgs)
    if verifier_msgs:
        label = f"See how the answer was checked ({rounds} verification round{'s' if rounds > 1 else ''})"
        with st.expander(label):
            for i, v_msg in enumerate(verifier_msgs, 1):
                if rounds > 1:
                    st.markdown(f"**Round {i} — Verification check**")
                else:
                    st.markdown("**Verification check**")
                st.markdown(v_msg.content)
                if i < rounds:
                    st.divider()
