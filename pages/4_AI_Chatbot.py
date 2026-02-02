# -*- coding: utf-8 -*-
import streamlit as st
from llm.client import llm_client


def main():
    st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0;'>🤖 Project Chatbot</h1>
            <p style='color: white; margin: 10px 0 0 0; font-size: 16px;'>Answers only marketing & trading topics from this project</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("## 💬 Ask a Project Question")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    col1, col2 = st.columns([2, 1])
    with col1:
        domain = st.selectbox(
            "Topic",
            options=["Marketing", "Trading"],
            index=0,
            help="Choose the topic for your question.",
        )
    with col2:
        response_style = st.selectbox(
            "Response Style",
            options=["Concise", "Detailed"],
            index=0,
            help="Choose how much detail you want in the response.",
        )

    user_question = st.text_area(
        "Your question",
        placeholder="E.g., How can I improve CTR on a Google Ads campaign? (Marketing/Trading only)",
        height=120,
    )

    if st.button("🚀 Ask", type="primary", use_container_width=True):
        if not user_question.strip():
            st.warning("Please enter a question to continue.")
        else:
            project_scope = (
                "This assistant ONLY answers questions about this project’s marketing and trading analytics. "
                "Reject unrelated topics such as coding help, general trivia, personal advice, or other domains."
            )
            system_prompt = (
                "You are a helpful assistant specialized in marketing and trading analytics for this project. "
                "Provide educational, practical guidance using simple language. Avoid financial advice. "
                "If a question is out of scope, politely refuse and ask for a marketing/trading analytics question. "
                "End with a short disclaimer. "
                + project_scope
            )
            if response_style == "Concise":
                system_prompt += " Keep answers brief and actionable."
            else:
                system_prompt += " Provide structured, detailed explanations with bullet points."

            allowed_keywords = [
                "marketing",
                "campaign",
                "roi",
                "ctr",
                "cpa",
                "conversion",
                "ad",
                "budget",
                "trading",
                "stock",
                "ticker",
                "price",
                "rsi",
                "macd",
                "moving average",
                "volatility",
                "analysis",
                "kpi",
            ]
            lower_question = user_question.lower()
            is_in_scope = any(keyword in lower_question for keyword in allowed_keywords)

            if not is_in_scope:
                response = (
                    "I can only help with marketing and trading analytics topics for this project. "
                    "Please ask a marketing or trading question (e.g., ROI, CTR, RSI, MACD, campaign performance)."
                )
            else:
                with st.spinner("Thinking..."):
                    response = llm_client.generate_response(
                        user_question,
                        system_prompt=system_prompt,
                        context=f"Topic: {domain}",
                    )

            st.session_state.chat_history.append(
                {"question": user_question.strip(), "response": response, "topic": domain}
            )

    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("## 📜 Conversation")
        for item in reversed(st.session_state.chat_history[-6:]):
            st.markdown(
                f"""
                <div style='padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 12px;'>
                    <p style='margin: 0; color: #666; font-size: 12px;'>Topic: {item['topic']}</p>
                    <p style='margin: 8px 0 6px 0; font-weight: 600;'>Q: {item['question']}</p>
                    <p style='margin: 0; color: #444; line-height: 1.6;'>A: {item['response']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 15px; background-color: #fff3cd; border-radius: 10px; border-left: 4px solid #ffc107; margin-top: 10px;'>
            <h4 style='color: #856404; margin-bottom: 10px;'>Educational Disclaimer</h4>
            <p style='color: #856404; margin: 0; font-size: 14px;'>Responses are educational and not financial advice.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
