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

# Initialize tab navigation (Analysis Form & Admin Dashboard)
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
            
        # Unstructured sales notes for the AI to parse
        sales_notes = st.text_area(
            "Sales Rep Notes & Activity Log", 
            placeholder="Paste the latest updates, email summaries, or notes from your 1-on-1 conversations here...",
            height=150
        )
        
        submit_button = st.form_submit_button(label="Run Reality Check")

    # Front-end Input Validation Layer
    if submit_button:
        if not deal_name.strip():
            st.error("⚠️ Validation Error: Deal Name cannot be empty.")
        elif not sales_notes.strip() or len(sales_notes.strip()) < 15:
            st.error("⚠️ Validation Error: Please provide detailed sales notes (at least 15 characters) for the AI contextual layer to analyze.")
        else:
            st.success(f"✅ Input Validated Successfully for '{deal_name}'! Ready for the Logic Layer.")

with tab2:
    st.subheader("🛡️ System Administration & History")
    st.info("The Admin Dashboard will display saved historical data once database persistence is active.")