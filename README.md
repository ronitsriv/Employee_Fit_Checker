only:

# Lead Scoring AI App (Streamlit)

A simple Streamlit app to score leads using Rule-based logic combined with Gemini AI.

This app allows you to:

- Upload a CSV of leads.
- Input your offer details (name, value propositions, ideal use cases).
- Score leads automatically based on role, industry, and AI-assessed intent.
- View results as JSON or table.
- Download the scored leads as a CSV.

## Features

### Rule-based scoring
Scores leads based on:
- Role relevance (Head, Director, Manager etc.)
- Industry match with your ideal use cases.
- Completeness of lead data.

### Gemini AI scoring
- Uses Google Gemini API (gemini-2.5-flash) to classify buying intent: High, Medium, Low.
- Provides a short explanation for the intent.

### Easy CSV handling
- Download sample CSV to see format.
- Upload your own leads CSV.
- Download scored leads CSV with combined rule + AI score.

## Requirements

- Python 3.10+
- Streamlit
- Pandas
- Google Gemini AI SDK (`google-generativeai`)

Install dependencies:

```bash
pip install streamlit pandas google-generativeai

Usage

Clone or download this repository.

Run the app:

streamlit run final_app.py


Enter your offer details:

Offer Name

Value Propositions (comma separated)

Ideal Use Cases (comma separated)

Upload your leads CSV:

Required columns: name, role, company, industry, location, linkedin_bio

Run scoring:

View results in JSON or table format.

Download the scored leads CSV.

Sample CSV Format
name	role	company	industry	location	linkedin_bio
Ava Patel	Head of Growth	FlowMetrics	B2B SaaS	NY	Scaling GTM
John Doe	Marketing Manager	MarketIQ	B2B SaaS	SF	Digital marketing lead
Output

rule_score: Points from rule-based logic.

ai_points: Points assigned by Gemini AI.

score: Combined score.

intent: AI classified intent (High, Medium, Low).

reasoning: AI explanation for intent.

Notes

Make sure your Gemini API key is valid (currently hardcoded in the script as API_KEY).

The scoring uses both manual rules and AI insights to give a better lead prioritization.
