import streamlit as st
import json
import sqlite3
from datetime import datetime
from openai import OpenAI

# Set up page configuration
st.set_page_config(
    page_title="Pipeline Reality Checker",
    page_icon="🔍",
    layout="wide"
)

# --- COMMIT 5: DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect("pipeline_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deal_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            deal_name TEXT,
            stage TEXT,
            size REAL,
            days_activity INTEGER,
            days_stagnant INTEGER,
            ai_status TEXT,
            ai_confidence INTEGER,
            ai_diagnosis TEXT,
            ai_action TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database layout
init_db()

# Application Title
st.title("🔍 Pipeline Reality Checker")
st.caption("Identify at-risk sales deals using structural logic and contextual AI.")

# Sidebar for API Key configuration
st.sidebar.header("🔑 API Configuration")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
st.sidebar.markdown("[Get an API Key here](https://platform.openai.com/api-keys)")

# Initialize tab navigation
tab1, tab2 = st.tabs(["📊 Deal Analysis Engine", "🛡️ Admin Dashboard"])

with tab1:
    st.subheader("Analyze a Deal")
    st.write("Enter the deal details below to evaluate true conversion risks.")
    
    with st.form(key="deal_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            deal_name = st.text_input("Deal Name", placeholder="e.g., Acme Corp Enterprise Expansion")
            deal_stage = st.selectbox(
                "Pipeline Stage",
                ["Discovery", "Qualification", "Proposal/Quote", "Negotiation", "Contracting"]
            )
            deal_size = st.number_input("Deal Size ($)", min_value=0, step=1000, value=25000)
            
        with col2:
            days_since_activity = st.number_input("Days Since Last Activity", min_value=0, step=1, value=5)
            days_in_stage = st.number_input("Days Stagnant in Current Stage", min_value=0, step=1, value=10)
            
        sales_notes = st.text_area(
            "Sales Rep Notes & Activity Log", 
            placeholder="Paste the latest updates, email summaries, or notes from your 1-on-1 conversations here...",
            height=150
        )
        
        submit_button = st.form_submit_button(label="Run Reality Check")

    if submit_button:
        if not deal_name.strip():
            st.error("⚠️ Validation Error: Deal Name cannot be empty.")
        elif not sales_notes.strip() or len(sales_notes.strip()) < 15:
            st.error("⚠️ Validation Error: Please provide detailed sales notes (at least 15 characters).")
        else:
            st.success(f"✅ Input Validated Successfully for '{deal_name}'!")
            
            # Layer 1: Logic Check
            st.markdown("---")
            st.subheader("⚙️ Layer 1: Deterministic Data Processing (Pre-AI)")
            
            ACTIVITY_THRESHOLD = 14
            STAGNATION_THRESHOLD = 30
            
            logic_flags = []
            is_stale_activity = days_since_activity > ACTIVITY_THRESHOLD
            is_stagnant_stage = days_in_stage > STAGNATION_THRESHOLD
            
            if is_stale_activity:
                logic_flags.append(f"LOW ACTIVITY: No updates in {days_since_activity} days.")
            if is_stagnant_stage:
                logic_flags.append(f"STAGE STAGNATION: Stuck in '{deal_stage}' for {days_in_stage} days.")
                
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.metric(label="Days Since Activity Status", value=f"{days_since_activity} Days", delta=f"{days_since_activity - ACTIVITY_THRESHOLD} Over" if is_stale_activity else "Safe", delta_color="inverse")
            with col_l2:
                st.metric(label="Stage Stagnation Status", value=f"{days_in_stage} Days", delta=f"{days_in_stage - STAGNATION_THRESHOLD} Over" if is_stagnant_stage else "Safe", delta_color="inverse")
            
            logic_summary = ", ".join(logic_flags) if logic_flags else "No hard thresholds breached."
            
            # Layer 2: AI Check
            st.markdown("---")
            st.subheader("🤖 Layer 2: Contextual AI Analysis")
            
            if not openai_api_key:
                st.warning("🔒 AI Analysis Paused: Please enter an OpenAI API Key in the sidebar.")
            else:
                with st.spinner("AI is analyzing deal context..."):
                    try:
                        client = OpenAI(api_key=openai_api_key)
                        
                        system_prompt = (
                            "You are an expert B2B Sales Operations Auditor. Your job is to analyze sales deals for hidden risks.\n"
                            "You must return your response as a strict JSON object with exactly these keys:\n"
                            "{\n"
                            "  \"deal_status\": \"Healthy\" or \"At Risk\" or \"Slipped\",\n"
                            "  \"risk_reason\": \"A concise, data-backed summary sentence explaining the core structural or conversational risk factor.\",\n"
                            "  \"next_action\": \"One explicit, tactical, highly prescriptive micro-action for the sales manager to execute immediately.\",\n"
                            "  \"confidence_score\": <an integer between 0 and 100>\n"
                            "}\n"
                        )
                        
                        user_content = f"Deal Name: {deal_name}\nStage: {deal_stage}\nSize: ${deal_size}\nDays Activity: {days_since_activity}\nDays Stagnant: {days_in_stage}\nLogic Flags: {logic_summary}\nNotes: {sales_notes}"
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_content}
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.2
                        )
                        
                        ai_result = json.loads(response.choices[0].message.content)
                        status = ai_result.get("deal_status", "At Risk")
                        confidence = ai_result.get("confidence_score", 80)
                        diagnosis = ai_result.get("risk_reason", "")
                        action = ai_result.get("next_action", "")
                        
                        # Render Results
                        col_out1, col_out2 = st.columns(2)
                        with col_out1:
                            if status == "Healthy": st.success(f"🟢 **AI Risk Rating:** {status}")
                            elif status == "At Risk": st.warning(f"🟡 **AI Risk Rating:** {status}")
                            else: st.error(f"🔴 **AI Risk Rating:** {status}")
                        with col_out2:
                            st.metric(label="AI Confidence Score", value=f"{confidence}%")
                            
                        st.info(f"**Risk Diagnosis:** {diagnosis}")
                        st.success(f"🎯 **Suggested Next Action:** {action}")
                        
                        # --- COMMIT 5: SAVE EXECUTION TO DATABASE ---
                        conn = sqlite3.connect("pipeline_data.db")
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO deal_history (timestamp, deal_name, stage, size, days_activity, days_stagnant, ai_status, ai_confidence, ai_diagnosis, ai_action)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), deal_name, deal_stage, float(deal_size), int(days_since_activity), int(days_in_stage), status, int(confidence), diagnosis, action))
                        conn.commit()
                        conn.close()
                        st.caption("💾 Analysis successfully saved to system historical logs.")
                        
                    except Exception as e:
                        st.error(f"❌ Error during API Call: {str(e)}")

# --- COMMIT 5: ADMIN DASHBOARD DISPLAY ---
with tab2:
    st.subheader("🛡️ System Administration & History Log")
    st.write("Review all historically audited sales deals stored inside the local database storage layers.")
    
    try:
        conn = sqlite3.connect("pipeline_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, deal_name, stage, size, ai_status, ai_confidence, ai_action FROM deal_history ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            for row in rows:
                with st.expander(f"🕒 {row[0]} | {row[1]} (${row[3]:,})"):
                    st.write(f"**Pipeline Stage:** {row[2]}")
                    st.write(f"**AI Evaluation Status:** {row[4]} (Confidence: {row[5]}%)")
                    st.write(f"**Prescribed Action:** {row[6]}")
        else:
            st.info("No historical audits saved yet. Run an analysis on a deal to populate the system database logs.")
    except Exception as e:
        st.error(f"Failed to load database logs: {e}")