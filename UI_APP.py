import streamlit as st
from graph.workflow import app
from chat_memory.chat_memory import save_summary, get_recent_summaries, trim_old_summaries
from auth.supabase_auth import login, logout, sign_up
from core.chain import summary_chain
from config.ingestion import get_docs
from config.setting import vectorstore, embeddings

st.set_page_config(page_title="AI Chat", layout="wide")

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

if "chat_done" not in st.session_state:
    st.session_state.chat_done = False

if "result" not in st.session_state:
    st.session_state.result = None

if "feedback" not in st.session_state:
    st.session_state.feedback = None

# ================= LOGIN / REGISTER =================
if st.session_state.user is None:

    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            session = login(email, password)
            if session:
                st.session_state.user = session.user.id
                # 🔥 RESET OLD CHAT STATE
                st.session_state.chat_done = False
                st.session_state.result = None
                st.session_state.feedback = None
                st.success("✅ Logged in")
                st.rerun()
            else:
                st.error("❌ Login failed")

    with tab2:
        email = st.text_input("New Email")
        password = st.text_input("New Password", type="password")

        if st.button("Register"):
            res = sign_up(email, password)
            if res:
                st.success("✅ Registered successfully")
            else:
                st.error("❌ Registration failed")

# ================= CHAT PAGE =================
else:

    st.title("🤖 AI Chat System")

    col1, col2 = st.columns([8, 2])
    #============= Logout =============================
    with col2:
        if st.button("🚪 Logout"):
            logout()
            st.session_state.user = None
            st.rerun()

    # ================= INGESTION SECTION =================
    st.markdown("## 📂 Upload Knowledge Base")

    uploaded_file = st.file_uploader("Upload PDF / DOCX / CSV")
    url_input = st.text_input("Or Paste URL")
    text_input = st.text_area("Or Paste Text")

    if st.button("📦 Process & Store in Pinecone"):

        docs = get_docs(
            uploaded_file=uploaded_file,
            url=url_input,
            raw_text=text_input
        )

        if not docs:
            st.error("❌ No input provided")
            st.stop()

        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(docs)

        vectorstore.add_documents(chunks)

        st.success(f"✅ Stored {len(chunks)} chunks in Pinecone")


       # ================= QUESTION INPUT =================            

    user_input = st.text_input("Ask something...")

    # ================= RUN GRAPH =================
    if st.button("Submit"):

        with st.spinner("🤔 Thinking..."):

            result = app.invoke({
                "question": user_input,
                "user_id": st.session_state.user
            })

            st.session_state.result = result
            st.session_state.chat_done = True
            st.session_state.feedback = None

    # ================= SHOW RESULT =================
    if st.session_state.chat_done:

        result = st.session_state.result

        st.markdown("## 🤖 Answer")
        st.write(result.get("generation", ""))

        # ================= EVALUATION =================
        eval_data = result.get("evaluation")

        if eval_data:
            st.markdown("### 📊 Evaluation")
            st.success(f"Relevant: {eval_data.relevant}")
            st.success(f"Grounded: {eval_data.grounded}")
            st.success(f"Answer Match: {eval_data.answer_question}")

        st.divider()

        # ================= HITL =================
        st.markdown("## 🧑 Human Feedback")

        col1, col2, col3 = st.columns(3)

        if col1.button("✅ Accept"):
            st.session_state.feedback = "accept"

        if col2.button("🔁 Retry"):
            st.session_state.feedback = "retry"

        if col3.button("✏️ Edit"):
            st.session_state.feedback = "edit"

        # ================= EDIT =================
        if st.session_state.feedback == "edit":
            edited = st.text_area("Edit Answer")

            if st.button("Submit Edit"):
                st.session_state.result["generation"] = edited
                st.session_state.feedback = "accept"

        # ================= RETRY =================
        if st.session_state.feedback == "retry":

            st.warning("♻️ Regenerating...")

            new_result = app.invoke({
                "question": user_input,
                "user_id": st.session_state.user
            })

            st.session_state.result = new_result
            # 🔥 FIX: Reset feedback BEFORE rerun
            st.session_state.feedback = None
            st.rerun()

        # ================= SUMMARY =================
        if st.session_state.feedback == "accept":

            st.success("✅ Approved!")

            if st.button("📝 Generate Summary"):

                summary = summary_chain.invoke({
                    "generation": st.session_state.result["generation"]
                })

                st.markdown("### 📌 Summary")
                st.write(summary)

                # SAVE TO DB
                try:
                    save_summary(st.session_state.user, summary)
                    # ✅ TRIM OLD MEMORY (KEEP LAST 5)
                    trim_old_summaries(st.session_state.user, keep_limit=5)

                    st.success("✅ Summary saved and old memory trimmed")

                    st.success("✅ Summary saved to PostgreSQL")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # ================= MEMORY =================
        if st.checkbox("📚 Show Recent Memory"):
            summaries = get_recent_summaries(st.session_state.user)

            st.markdown("### 🧠 Last 5 Memories")

            if not summaries:
                st.info("No previous chats")
            else:
                for i, s in enumerate(summaries, 1):
                    st.write(f"{i}. {s}")