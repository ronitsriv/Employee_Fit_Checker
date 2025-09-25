import streamlit as st
import pandas as pd
import spacy

# ---- Load spaCy model ----
seer = spacy.load("en_core_web_sm")

st.title("🎯 Lead Scoring with spaCy")
st.write("Upload a leads CSV and score them using **Rule-based** and **spaCy-based entity matching**.")

# ---- Offer Input ----
st.subheader("📌 Offer Details")
offer_name = st.text_input("Offer Name")
value_props = st.text_area("Value Props (comma separated)")
ideal_use_cases = st.text_area("Ideal Use Cases (comma separated)")

offer = {
    "name": offer_name.strip(),
    "value_props": [v.strip() for v in value_props.split(",") if v.strip()],
    "ideal_use_cases": [u.strip() for u in ideal_use_cases.split(",") if u.strip()],
}

# ---- Sample Leads CSV ----
st.subheader("⬇️ Sample Leads CSV")
sample_data = [
    {"name": "Ava Patel", "role": "Head of Growth", "company": "FlowMetrics", "industry": "B2B SaaS", "location": "NY", "linkedin_bio": "Scaling GTM"},
    {"name": "John Doe", "role": "Marketing Manager", "company": "MarketIQ", "industry": "B2B SaaS", "location": "SF", "linkedin_bio": "Digital marketing lead"},
    {"name": "Priya Singh", "role": "Director of Sales", "company": "CloudTech", "industry": "Cloud SaaS", "location": "TX", "linkedin_bio": "Enterprise sales"},
    {"name": "Rahul Kumar", "role": "Analyst", "company": "DataWave", "industry": "FinTech", "location": "CA", "linkedin_bio": "Data analytics"},
    {"name": "Sara Lee", "role": "VP Operations", "company": "OpsPlus", "industry": "B2B SaaS", "location": "NY", "linkedin_bio": "Operations management"},
]
sample_df = pd.DataFrame(sample_data)
csv_bytes = sample_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Sample Leads CSV", csv_bytes, "sample_leads.csv", "text/csv")

# ---- Upload Leads ----
st.subheader("📤 Upload Leads CSV")
uploaded_file = st.file_uploader("Choose your leads CSV", type=["csv"])

# ---- Rule-based scoring ----
def rule_score(lead):
    score = 0
    role = str(lead.get("role", "")).lower()
    if "head" in role or "director" in role:
        score += 20
    elif "manager" in role:
        score += 10
    for icp in offer["ideal_use_cases"]:
        if icp.lower() in str(lead.get("industry", "")).lower():
            score += 20
            break
    if all(str(v).strip() for v in lead.values()):
        score += 10
    return score

# ---- spaCy-based scoring ----
def spacy_score(lead):
    text = f"{lead.get('name','')} {lead.get('role','')} {lead.get('company','')} {lead.get('industry','')} {lead.get('linkedin_bio','')}"
    doc = seer(text)
    ents = [ent.text for ent in doc.ents]

    # Simple intent classification using entities
    if any(ent for ent in ents if ent.lower() in ["ceo", "cto", "head", "director"]):
        return 50, "High", f"Identified senior role entities: {ents}"
    elif any(ent for ent in ents if ent.lower() in ["manager", "lead"]):
        return 30, "Medium", f"Identified mid-level role entities: {ents}"
    else:
        return 10, "Low", f"No strong senior role entities found. Entities: {ents}"

# ---- Run Scoring ----
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {"name", "role", "company", "industry", "location", "linkedin_bio"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV missing columns: {required_cols - set(df.columns)}")
    else:
        st.subheader("⚙️ Processing Leads...")
        results = []
        progress_bar = st.progress(0)

        for i, (_, row) in enumerate(df.iterrows(), 1):
            lead = row.to_dict()
            rs = rule_score(lead)
            sp_pts, intent, reasoning = spacy_score(lead)
            results.append({**lead, "rule_score": rs, "spacy_points": sp_pts, "intent": intent, "reasoning": reasoning})
            progress_bar.progress(i / len(df))
        progress_bar.empty()

        results_df = pd.DataFrame(results)

        # JSON view
        st.subheader("🧾 Scored Leads (JSON)")
        st.json(results)

        # Table view
        st.subheader("📊 Table View")
        st.dataframe(results_df)

        # Save results
        results_df.to_csv("scored_leads.csv", index=False)
        st.success("Results saved to scored_leads.csv ✅")

        # Download button
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Scored Leads CSV", csv, "scored_leads.csv", "text/csv")
