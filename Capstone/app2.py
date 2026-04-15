# =========================================
# BIM + SD + GEMINI + DASHBOARD (FINAL)
# DRP: Digital Delivery Platform for Design
# Development Phase of Healthcare Building Projects
# AIDTM | Parth Patel | 20241040
# =========================================
 
# --- Import Libraries ---
import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import plotly.express as px
import plotly.graph_objects as go
 
# --- Load API Key ---
# --- Load API Key ---
import os
import streamlit as st
from dotenv import load_dotenv

# --- Load API Key ---
load_dotenv()

def get_gemini_api_key():
    # 1) Try Streamlit Cloud secrets first
    try:
        return st.secrets["AIzaSyDeWILGO6OuNVgm1_YO_gFA9IUp0w4zAf4"]
    except Exception:
        pass

    # 2) Fallback to local .env for local development
    return os.getenv("GEMINI_API_KEY")

GEMINI_API_KEY = get_gemini_api_key()

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Add it in Streamlit Cloud Secrets or local .env file.")
    st.stop()

# --- Initialize Gemini ---
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini: {e}")
    st.stop()
 
# --- Page Config ---
st.set_page_config(
    page_title="BIM Decision Support | AIDTM",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# =========================================
# SIDEBAR
# =========================================
with st.sidebar:
    st.markdown("### 🏗️ BIM Decision Support")
    st.markdown("DD Stage · LOD 300–350")
    st.divider()
 
    page = st.radio(
        "Navigation",
        ["Dashboard", "BIM Data", "Scenarios", "Simulation", "AI Chat"],
        label_visibility="collapsed"
    )
 
    st.divider()
    st.markdown("**Project Info**")
    st.caption("AIDTM")
    st.caption("Parth Patel · 20241040")
 
# =========================================
# LOAD DATA
# =========================================
# excel_path = "project.xlsx"
# --- Correctly locate the Excel file ---
script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(script_dir, "project.xlsx")


 
try:
    xls      = pd.ExcelFile(excel_path)
    bim_df   = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    scenario_df = pd.read_excel(xls, sheet_name=xls.sheet_names[1])
    sim_df   = pd.read_excel(xls, sheet_name=xls.sheet_names[2])
except Exception as e:
    st.error(f"❌ Error loading Excel: {e}")
    st.stop()
 
# --- Detect Columns ---
def find_col(df, keyword):
    for col in df.columns:
        if keyword.lower() in col.lower():
            return col
    return None
 
status_col    = find_col(bim_df, "status")       # 'Issues Status'
desc_col      = find_col(bim_df, "description")  # 'Description'
placement_col = find_col(bim_df, "placement")    # 'Placement'
month_col     = find_col(bim_df, "month")        # 'Month'
rework_col    = find_col(sim_df, "rework")       # 'Rework'
scenario_col  = find_col(sim_df, "scenario")     # 'Scenario_ID'
open_issues_col = find_col(sim_df, "open")       # 'Open_Issues'
 
# =========================================
# BIM SUMMARY METRICS
# =========================================
total_issues  = len(bim_df)
open_issues   = len(bim_df[bim_df[status_col].astype(str).str.lower() == "open"])
closed_issues = len(bim_df[bim_df[status_col].astype(str).str.lower() == "closed"])
open_pct      = round((open_issues / total_issues) * 100, 1) if total_issues > 0 else 0
 
# =========================================
# SCENARIO LOGIC
# =========================================
if open_issues > 5:
    recommended_scenario = "S3 — BIM + LLM (High Coordination)"
    recommendation_reason = f"{open_issues} open issues detected (>5 threshold). Resolution_Rate=0.7"
elif open_issues > 2:
    recommended_scenario = "S2 — Moderate Coordination"
    recommendation_reason = f"{open_issues} open issues detected (3–5 range). Resolution_Rate=0.5"
else:
    recommended_scenario = "S1 — Low Coordination (Baseline)"
    recommendation_reason = f"Only {open_issues} open issues detected (≤2). Resolution_Rate=0.3"
 
# =========================================
# SIMULATION ANALYSIS
# =========================================
best_scenario = "Not identified"
try:
    if rework_col and scenario_col:
        best_scenario = sim_df.groupby(scenario_col)[rework_col].mean().idxmin()
except:
    pass
 
# =========================================
# GEMINI CONTEXT BUILDER
# =========================================
def build_excel_context(bim_df, scenario_df, sim_df, max_bim_rows=80):
    if len(bim_df) > max_bim_rows:
        open_mask  = bim_df[status_col].astype(str).str.lower().isin(['open', 'in progress'])
        bim_sample = bim_df[open_mask].head(max_bim_rows)
        note = f"(Showing {len(bim_sample)} open issues out of {len(bim_df)} total)"
    else:
        bim_sample = bim_df.copy()
        note = f"(All {len(bim_df)} issues shown)"
 
    if desc_col and desc_col in bim_sample.columns:
        bim_sample = bim_sample.copy()
        bim_sample[desc_col] = (
            bim_sample[desc_col]
            .astype(str)
            .str[:300]
            .apply(lambda x: x + "..." if len(x) >= 300 else x)
        )
 
    context  = f"=== SHEET 1: BIM_DATA {note} ===\n"
    context += "Project: AIDTM BDA CAPSTONE PROJECT | Disciplines: HEALTHCARE PROJECT\n\n"
    context += bim_sample.to_string(index=False) + "\n\n"
 
    context += "=== SHEET 2: SCENARIOS ===\n"
    context += (
        "S1 — Low Coordination: Baseline, fragmented BIM, high rework\n"
        "S2 — Moderate Coordination: Partial improvements\n"
        "S3 — BIM + LLM: Optimised, ISO 19650-aligned, lowest rework\n\n"
    )
    context += scenario_df.to_string(index=False) + "\n\n"
 
    context += "=== SHEET 3: SIMULATION_OUTPUT ===\n"
    context += "Open_Issues = unresolved clashes | Rework = accumulated rework volume\n\n"
    context += sim_df.to_string(index=False) + "\n\n"
 
    return context
 
def ask_gemini(question):
    excel_context = build_excel_context(bim_df, scenario_df, sim_df)
    bim_summary   = f"Total: {total_issues} | Open: {open_issues} | Closed: {closed_issues}"
 
    prompt = f"""
You are a BIM coordination decision support assistant for a real healthcare building project.
This system is part of a AIDTM capstone project titled:
"Digital Delivery Platform for Design Development Phase of Healthcare Building Projects"
by Parth Patel (20241040).
 
PROJECT DATA:
{excel_context}
 
BIM SUMMARY: {bim_summary}
Rule-based recommendation : {recommended_scenario}
Reason                    : {recommendation_reason}
Best scenario (simulation): {best_scenario}
 
Top RII challenges from DRP survey:
1. Unclear client requirements (RII = 0.875)
2. BIM used as drafting tool (RII = 0.850)
3. Rework due to unidentified design issues (RII = 0.850)
4. Poor coordination between disciplines (RII = 0.850)
5. Time pressure affecting coordination (Freq RII = 0.767)
 
QUESTION: {question}
 
Instructions:
- Answer ONLY what the user is asking.
- For specific issue questions (e.g. "describe issue #5"): use BIM_DATA only.
- For scenario/strategy questions: use Sheet 2 and/or Sheet 3.
- For simulation trends: use Sheet 3 only.
- NEVER force scenario comparison unless explicitly asked.
- Use BIM terminology: LOD, CDE, ISO 19650, MEP, DD stage, EIR, BEP, RVT.
- Be concise for simple questions. Detailed only when needed.
"""
    response = llm.invoke(prompt)
    time.sleep(2)
    return response.content.strip()
 
# =========================================
# PAGE: DASHBOARD
# =========================================
if page == "Dashboard":
 
    st.title("🏗️ BIM + SD + AI Decision Support System")
    st.caption("CEPT ICP M1 · Healthcare Project · Design Development Stage · LOD 300–350")
    st.divider()
 
    # --- Section 1: KPI Metrics ---
    st.subheader("① Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Issues", total_issues)
    col2.metric("Open Issues", open_issues, delta=f"{open_pct}% unresolved", delta_color="inverse")
    col3.metric("Closed Issues", closed_issues)
    col4.metric("Resolution Rate", f"{100 - open_pct}%")
 
    st.divider()
 
    # --- Section 2: Scenario Recommendation ---
    st.subheader("② Scenario Recommendation")
    rec_col, sim_col = st.columns(2)
    with rec_col:
        st.success(f"📊 **Rule-based:** {recommended_scenario}")
        st.caption(recommendation_reason)
    with sim_col:
        st.info(f"📉 **Best from simulation:** {best_scenario} (lowest avg rework)")
 
    st.divider()
 
    # --- Section 3: Visualizations ---
    st.subheader("③ Visualizations")
 
    chart_col1, chart_col2 = st.columns(2)
 
    # Pie chart
    with chart_col1:
        status_counts = bim_df[status_col].value_counts()
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Open vs Closed Issues",
            color=status_counts.index,
            color_discrete_map={"Open": "#BA7517", "Closed": "#3B6D11"},
            hole=0.4
        )
        fig_pie.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)
 
    # Bar chart by placement / discipline
    with chart_col2:
        if placement_col:
            placement_counts = bim_df[placement_col].astype(str).apply(
                lambda x: "ARCH" if "ARCH" in x else
                          "STR"  if "STR"  in x else
                          "MEP"  if "MEP"  in x else
                          "Coordinated" if "Coordinated" in x or "Coord" in x else "Other"
            ).value_counts().reset_index()
            placement_counts.columns = ["Discipline", "Count"]
 
            fig_bar = px.bar(
                placement_counts,
                x="Count",
                y="Discipline",
                orientation="h",
                title="Issues by Discipline",
                color="Count",
                color_continuous_scale=["#B5D4F4", "#185FA5"]
            )
            fig_bar.update_layout(
                margin=dict(t=40, b=10, l=10, r=10),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No Placement column found for discipline chart.")
 
    # Line chart: open issues over time from simulation
    if open_issues_col and scenario_col:
        time_col = find_col(sim_df, "time")
        if time_col:
            fig_line = px.line(
                sim_df,
                x=time_col,
                y=open_issues_col,
                color=scenario_col,
                title="Open Issues Over Time — Scenario Comparison",
                markers=True,
                color_discrete_map={
                    "S1": "#E24B4A",
                    "S2": "#BA7517",
                    "S3": "#3B6D11"
                }
            )
            fig_line.update_layout(margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_line, use_container_width=True)
 
    # Rework comparison bar
    if rework_col and scenario_col:
        rework_summary = sim_df.groupby(scenario_col)[rework_col].mean().reset_index()
        rework_summary.columns = ["Scenario", "Avg Rework"]
 
        fig_rework = px.bar(
            rework_summary,
            x="Scenario",
            y="Avg Rework",
            title="Average Rework by Scenario",
            color="Scenario",
            color_discrete_map={
                "S1": "#E24B4A",
                "S2": "#BA7517",
                "S3": "#3B6D11"
            },
            text="Avg Rework"
        )
        fig_rework.update_traces(textposition="outside")
        fig_rework.update_layout(
            margin=dict(t=40, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(fig_rework, use_container_width=True)
 
    st.divider()
 
    # --- Section 4: Scenario Comparison Cards ---
    st.subheader("④ Scenario Comparison")
 
    s1_col, s2_col, s3_col = st.columns(3)
 
    with s1_col:
        st.markdown("**S1 — Low Coordination**")
        s1 = scenario_df[scenario_df.iloc[:, 0] == "S1"].iloc[0] if len(scenario_df) > 0 else None
        if s1 is not None:
            st.metric("Resolution Rate", s1.get("Resolution_Rate", "—"))
            st.metric("New Issues Rate", s1.get("New_Issues_Rate", "—"))
            st.metric("Avg Rework", sim_df[sim_df[scenario_col] == "S1"][rework_col].mean() if rework_col else "—")
 
    with s2_col:
        st.markdown("**S2 — Moderate Coordination**")
        s2 = scenario_df[scenario_df.iloc[:, 0] == "S2"].iloc[0] if len(scenario_df) > 0 else None
        if s2 is not None:
            st.metric("Resolution Rate", s2.get("Resolution_Rate", "—"))
            st.metric("New Issues Rate", s2.get("New_Issues_Rate", "—"))
            st.metric("Avg Rework", sim_df[sim_df[scenario_col] == "S2"][rework_col].mean() if rework_col else "—")
 
    with s3_col:
        st.markdown("**✅ S3 — BIM + LLM (Best)**")
        s3 = scenario_df[scenario_df.iloc[:, 0] == "S3"].iloc[0] if len(scenario_df) > 0 else None
        if s3 is not None:
            st.metric("Resolution Rate", s3.get("Resolution_Rate", "—"))
            st.metric("New Issues Rate", s3.get("New_Issues_Rate", "—"))
            st.metric("Avg Rework", sim_df[sim_df[scenario_col] == "S3"][rework_col].mean() if rework_col else "—")
 
    st.divider()
 
    # --- Section 5: Data Tables ---
    st.subheader("⑤ Project Data")
 
    with st.expander("📂 BIM Data — Clash Issues"):
        st.dataframe(bim_df, use_container_width=True)
 
    with st.expander("⚙️ Scenarios"):
        st.dataframe(scenario_df, use_container_width=True)
 
    with st.expander("📈 Simulation Output"):
        st.dataframe(sim_df, use_container_width=True)
 
# =========================================
# PAGE: BIM DATA
# =========================================
elif page == "BIM Data":
 
    st.title("📂 BIM Data — Clash Issues")
    st.caption("Source: Autodesk Construction Cloud (ACC) · CEPT ICP M1")
    st.divider()
 
    # Filters
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=bim_df[status_col].unique().tolist(),
            default=bim_df[status_col].unique().tolist()
        )
    with filter_col2:
        if month_col:
            month_filter = st.multiselect(
                "Filter by Month",
                options=sorted(bim_df[month_col].dropna().unique().tolist()),
                default=sorted(bim_df[month_col].dropna().unique().tolist())
            )
        else:
            month_filter = None
 
    filtered_df = bim_df[bim_df[status_col].isin(status_filter)]
    if month_col and month_filter:
        filtered_df = filtered_df[filtered_df[month_col].isin(month_filter)]
 
    st.metric("Showing", f"{len(filtered_df)} of {total_issues} issues")
    st.dataframe(filtered_df, use_container_width=True)
 
# =========================================
# PAGE: SCENARIOS
# =========================================
elif page == "Scenarios":
 
    st.title("⚙️ Coordination Scenarios")
    st.caption("System Dynamics Scenarios from DRP SD Model — Vensim Stock & Flow")
    st.divider()
 
    st.markdown("""
    | Scenario | Name | Description |
    |---|---|---|
    | **S1** | Low Coordination | Baseline — fragmented BIM, slow error discovery, high rework |
    | **S2** | Moderate Coordination | Partial improvements, better coordination, lacks stage-gate validation |
    | **S3** | BIM + LLM | Optimised — ISO 19650-aligned CDE, LLM-assisted, lowest rework |
    """)
 
    st.divider()
    st.subheader("Scenario Parameters")
    st.dataframe(scenario_df, use_container_width=True)
 
    st.divider()
    st.subheader("SD Model Stocks")
    st.markdown("""
    The Vensim stock-and-flow model tracks four key variables:
    - **Coordination Quality** — effectiveness of multidisciplinary coordination (0–1 scale)
    - **Undiscovered Design Errors** — hidden issues not yet identified
    - **Rework Volume** — accumulated rework due to design errors
    - **Project Delay** — cumulative delay generated during DD stage
    """)
 
# =========================================
# PAGE: SIMULATION
# =========================================
elif page == "Simulation":
 
    st.title("📈 Simulation Output")
    st.caption("SD Model Results — Open Issues and Rework per Scenario over Time")
    st.divider()
 
    st.dataframe(sim_df, use_container_width=True)
    st.divider()
 
    if open_issues_col and scenario_col:
        time_col = find_col(sim_df, "time")
        if time_col:
            fig = px.line(
                sim_df,
                x=time_col,
                y=open_issues_col,
                color=scenario_col,
                title="Open Issues Over Time",
                markers=True,
                color_discrete_map={"S1": "#E24B4A", "S2": "#BA7517", "S3": "#3B6D11"}
            )
            st.plotly_chart(fig, use_container_width=True)
 
    if rework_col and scenario_col:
        time_col = find_col(sim_df, "time")
        if time_col:
            fig2 = px.line(
                sim_df,
                x=time_col,
                y=rework_col,
                color=scenario_col,
                title="Rework Volume Over Time",
                markers=True,
                color_discrete_map={"S1": "#E24B4A", "S2": "#BA7517", "S3": "#3B6D11"}
            )
            st.plotly_chart(fig2, use_container_width=True)
 
# =========================================
# PAGE: AI CHAT
# =========================================
elif page == "AI Chat":
 
    st.title("🤖 AI Decision Support")
    st.caption("Ask anything about your BIM data, scenarios, or coordination decisions")
    st.divider()
 
    # Quick question buttons
    st.markdown("**Quick questions:**")
    q_col1, q_col2, q_col3 = st.columns(3)
 
    quick_q = None
    with q_col1:
        if st.button("Which scenario has lowest rework?"):
            quick_q = "Which scenario has the lowest rework?"
        if st.button("Describe issue #14"):
            quick_q = "Describe issue #14"
    with q_col2:
        if st.button("How many open issues?"):
            quick_q = "How many open issues are there and which are they?"
        if st.button("What is S3?"):
            quick_q = "What does S3 mean in this project?"
    with q_col3:
        if st.button("Best coordination strategy?"):
            quick_q = "What coordination strategy should I follow given the current open issues?"
        if st.button("What does simulation suggest?"):
            quick_q = "What does the simulation output suggest about the current project state?"
 
    st.divider()
 
    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
 
    # Display history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
 
    # Handle quick question
    if quick_q:
        st.session_state.chat_history.append({"role": "user", "content": quick_q})
        with st.chat_message("user"):
            st.write(quick_q)
        with st.chat_message("assistant"):
            with st.spinner("Gemini is analysing your data..."):
                answer = ask_gemini(quick_q)
            st.write(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
 
    # Chat input
    user_input = st.chat_input("Ask about your BIM data, scenarios, or coordination decisions...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Gemini is analysing your data..."):
                answer = ask_gemini(user_input)
            st.write(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
 
    # Clear history button
    if st.session_state.chat_history:
        st.divider()
        if st.button("🗑️ Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()
