# ⚙️ Procurement Reliability Dashboard

##  1. Problem Statement

Procurement systems often rely on basic metrics like cost or supplier reputation, without systematically evaluating **delivery reliability, consistency, and risk**. This leads to:

* Poor supplier selection
* Unexpected delays in supply chain
* Increased operational costs
* Lack of data-driven decision making

The objective of this project is to build a **data-driven procurement analytics system** that evaluates suppliers based on multiple factors and provides actionable insights.

---

##  2. Objective

To design and implement a system that:

* Analyzes supplier performance using historical procurement data
* Computes a **reliability score** for each supplier
* Classifies suppliers into risk categories
* Uses machine learning to predict delays
* Provides an interactive dashboard for decision-making

---

##  3. Solution Overview

We developed a **Procurement Reliability Dashboard** that processes procurement data and transforms it into meaningful insights.

The system follows a structured pipeline:

```text
Raw Data → Processing → Feature Engineering → Scoring → ML Prediction → Visualization
```

---

##  4. System Architecture

The project follows a **modular architecture**, ensuring separation of concerns:

```text
Data Layer        → CSV files (Suppliers, Orders, Products, Order Details)
Processing Layer  → Delay & cost computation
Analytics Layer   → Scoring + Risk classification
ML Layer          → Delay prediction
Presentation Layer→ Streamlit Dashboard
```

---

##  5. Dataset Design

The project uses a **relational dataset with 4 tables**:

### 1. Suppliers

* supplier_id
* rating
* supplier_type
* primary_category

### 2. Orders

* order_id
* supplier_id
* expected_delivery
* actual_delivery

### 3. Order Details

* order_id
* product_id
* quantity
* cost_per_unit

### 4. Products

* product_id
* category

---

###  Key Design Strengths

* ✔ Multi-table relational structure
* ✔ Realistic procurement flow
* ✔ Supports scalability (100 suppliers)
* ✔ Enables advanced analytics

---

##  6. Data Processing

### Key transformations:

* **Total Cost Calculation**

  * quantity × cost_per_unit

* **Delay Calculation**

  * actual_delivery − expected_delivery

* **Important Fix (Realism)**

  * Negative delays are clipped to 0
  * Early delivery = 0 delay

* **On-time Delivery**

  * delay == 0 → on_time = 1

---

##  7. Feature Engineering

For each supplier:

* Average Delay
* On-Time Delivery Rate
* Average Cost
* Supplier Rating

---

##  8. Scoring Model

A composite score is computed using:

```text
Score =
0.4 × On-Time Rate +
0.2 × Normalized Delay +
0.2 × Normalized Cost +
0.2 × Rating
```

###  Normalization Strategy

* norm_delay = 1 / (1 + avg_delay)
* norm_cost = 1 / (1 + avg_cost)

###  Why this approach?

* Prevents division by zero
* Keeps values bounded (0–1)
* Ensures fair comparison

---

##  9. Risk Classification

Suppliers are classified as:

* 🟢 Low Risk → delay ≤ 2
* 🟡 Medium Risk → delay ≤ 5
* 🔴 High Risk → delay > 5

---

## 🤖 10. Machine Learning Component

A **Linear Regression model** is used to predict supplier delay based on:

* Average Cost
* Supplier Rating

### Purpose:

* Demonstrates predictive capability
* Adds intelligence to procurement decisions

---

##  11. Visualizations

The dashboard includes:

### 🔹 Core Visuals

* Supplier Score Comparison
* Delay Distribution

### 🔹 Advanced Visuals

* Top 10 Suppliers (ranking) 
* Risk Distribution 

---

###  Design Improvement

Instead of plotting all 100 suppliers (which caused clutter), we:

* Display only **Top 20 suppliers** in charts
* Improve readability and interpretability

---

##  12. UI Design

The dashboard uses:

* Dark theme 🌑
* Metallic styling ⚙️
* Minimal layout

### Goals:

* Reduce clutter
* Improve readability
* Focus on insights

---

##  13. Key Insights Generated

The system answers:

* Which supplier performs best?
* Which suppliers are high risk?
* How does delay affect performance?
* What is overall procurement efficiency?

---

##  14. Unique Aspects of the Project

* ✔ Multi-factor supplier evaluation (not just cost)
* ✔ Realistic delay handling (no negative delays)
* ✔ Stable normalization techniques
* ✔ Modular architecture (industry-style design)
* ✔ Integration of ML with analytics
* ✔ Clean, decision-focused dashboard

---

##  15. Relevance to Problem Statement

This project directly addresses the procurement problem by:

* Replacing intuition with data-driven scoring
* Identifying high-risk suppliers early
* Providing actionable insights for supplier selection
* Improving supply chain reliability

---

##  16. Future Improvements

###  Advanced Visualizations

* Supplier performance by product category
* Time-series delay trends
* Heatmaps (supplier vs category)
* Cost vs delay trend lines

---

###  UI Enhancements

* Color-coded rows (risk highlighting)
* Highlight best supplier
* Sidebar navigation
* Multi-filter dashboard
* Animated charts

---

###  ML Enhancements

* Classification model for risk prediction
* More features (supplier type, category)
* Model evaluation metrics
* Time-series forecasting

---

###  Data Enhancements

* Multiple products per order
* Supplier specialization mapping
* Quality/defect rate
* Larger dataset

---

## 17. How to Run

# macOS / Linux

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 -m streamlit run app.py

# Windows (PowerShell)

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python3 -m streamlit run app.py


##  18. Author

**Rachana Ramchandar - PES1UG23CS459**

**Preksha M - PES1UG23CS450**

**Pranitha G - PES1UG23CS441**

---

##  19. Conclusion

This project demonstrates how procurement data can be transformed into actionable insights using:

* Data engineering
* Analytics
* Machine learning
* Visualization

It provides a scalable and practical solution for improving supplier selection and procurement efficiency.
