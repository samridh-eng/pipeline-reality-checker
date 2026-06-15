import streamlit as st

# Set up page configuration
st.set_page_config(
    page_title="Pipeline Reality Checker",
    page_icon="🔍",
    layout="wide"
)

# Application Title & Subtitle
st.title("🔍 Pipeline Reality Checker")
st.caption("Identify at-risk sales deals using structural logic and contextual AI.")

# Initialize tab navigation
tab1, tab2 = st.tabs(["📊 Deal Analysis Engine", "🛡️ Admin Dashboard"])

with tab1:
    st.subheader("Analyze a Deal")
    st.write("Enter the deal details below to evaluate true conversion risks.")
    
    # Create the structured input form
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

    # Processing Layer
    if submit_button:
        if not deal_name.strip():
            st.error("⚠️ Validation Error: Deal Name cannot be empty.")
        elif not sales_notes.strip() or len(sales_notes.strip()) < 15:
            st.error("⚠️ Validation Error: Please provide detailed sales notes (at least 15 characters) for the AI contextual layer to analyze.")
        else:
            st.success(f"✅ Input Validated Successfully for '{deal_name}'!")
            
            # --- COMMIT 3: PRE-AI DETERMINISTIC LOGIC LAYER ---
            st.markdown("---")
            st.subheader("⚙️ Layer 1: Deterministic Data Processing (Pre-AI)")
            
            # Define hard operational thresholds
            ACTIVITY_THRESHOLD = 14  # Max allowed days of silence
            STAGNATION_THRESHOLD = 30 # Max allowed days without stage progression
            
            logic_flags = []
            is_stale_activity = days_since_activity > ACTIVITY_THRESHOLD
            is_stagnant_stage = days_in_stage > STAGNATION_THRESHOLD
            
            # Evaluate rules
            if is_stale_activity:
                logic_flags.append(f"🚨 LOW ACTIVITY: No updates in {days_since_activity} days (Threshold: {ACTIVITY_THRESHOLD} days).")
            if is_stagnant_stage:
                logic_flags.append(f"🚨 STAGE STAGNATION: Stuck in '{deal_stage}' for {days_in_stage} days (Threshold: {STAGNATION_THRESHOLD} days).")
                
            # Render Logic Layer Findings
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.metric(label="Days Since Activity Status", value=f"{days_since_activity} Days", delta=f"{days_since_activity - ACTIVITY_THRESHOLD} Over limit" if is_stale_activity else "Safe", delta_color="inverse")
            with col_l2:
                st.metric(label="Stage Stagnation Status", value=f"{days_in_stage} Days", delta=f"{days_in_stage - STAGNATION_THRESHOLD} Over limit" if is_stagnant_stage else "Safe", delta_color="inverse")
                
            if logic_flags:
                st.warning("⚠️ **Deterministic Risk Flags Triggered:**")
                for flag in logic_flags:
                    st.write(flag)
            else:
                st.info("💚 **Deterministic Check:** Metrics are within normal operating bounds. Proceeding to contextual verification...")
            
            # Temporary placeholder for Commit 4
            st.info("⏭️ Logic calculations completed. Ready for Layer 2: Contextual AI Prompt Construction.")

with tab2:
    st.subheader("🛡️ System Administration & History")
    st.info("The Admin Dashboard will display saved historical data once database persistence is active.")