# Retail Profitability & Discount Strategy Analysis

> **Live Dashboard:** [datascience-fhijvcwq9jts4des8vjcsv.streamlit.app](https://datascience-fhijvcwq9jts4des8vjcsv.streamlit.app/)

An executive analytics dashboard examining four years of retail transaction
data to answer one question: **why does $2.3M in revenue only deliver
~12% to the bottom line?**

Built with Streamlit + Plotly. Dark mode, sidebar filters, gauge-style KPIs —
designed as a product analytics tool rather than a static report.

---

## What This Dashboard Shows

- **Executive KPI Overview** — profit margin, loss rate, discount exposure shown as gauges against healthy-range thresholds
- **Revenue & Margin Trend** — year-over-year growth vs. profitability
- **Regional & Category Performance** — where margin is structurally weak, broken down by region × category
- **Discount Impact Analysis** — the precise 20% discount threshold beyond which transactions consistently lose money
- **Key Business Insights** — five data-backed findings, ranked by severity
- **Strategic Recommendations** — six prioritized actions with estimated financial impact, effort, and timeline

All charts respond live to the sidebar filters (Region, Category, Segment, Year).

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | App framework & deployment |
| Plotly | Interactive charts & gauges |
| Pandas | Data processing |
| Python | Core logic |

---

## Run Locally

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
streamlit run app.py
```

The app expects `SampleSuperstore.csv` to be in the same folder as `app.py`.

---

## Deploy Your Own Copy (Streamlit Community Cloud — Free)

1. Push this folder to a GitHub repo — include `app.py`, `requirements.txt`, and `Sample_-_Superstore.csv`
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and select `app.py` as the main file
4. Deploy — you'll get a public URL to share

---

## Files

| File | Description |
|---|---|
| `app.py` | Main dashboard application |
| `Sample_-_Superstore.csv` | Dataset — must stay in the same folder as `app.py` |
| `requirements.txt` | Python dependencies |

---

## Dataset

[Sample Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (Kaggle) —
9,994 retail transactions, January 2014 to December 2017, across 4 US regions,
3 product categories, and 3 customer segments.

---

## Author

Built as part of a data analytics portfolio focused on business profitability
and discount strategy analysis. Feedback and forks welcome.