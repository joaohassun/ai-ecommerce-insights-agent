# AI-Powered E-commerce Analytics Agent

## Overview

This project builds an end-to-end analytics system on the Brazilian Olist e-commerce dataset, designed to simulate how a data analyst translates raw data into business insights and recommendations.

Beyond traditional analysis, the project introduces an intent-driven query system that dynamically generates insights based on business questions, mimicking how an analyst would respond in a real-world setting.

---

## Objectives

- Transform raw transactional data into structured business insights  
- Identify key drivers of customer satisfaction, revenue and operational performance  
- Build a reusable insight generation engine  
- Simulate an AI-assisted business analyst through a query interface  

---

## Dataset

The project uses the publicly available **Olist Brazilian E-commerce Dataset**, which includes:

- Orders and order items  
- Customer information  
- Product categories  
- Reviews and ratings  
- Delivery timestamps  

---

## Methodology

The system is structured as a modular analytics pipeline:

### 1. Data Preparation
- Data cleaning and type handling  
- Feature engineering (delivery delays, revenue, etc.)  
- Separation of order-level vs item-level data  

### 2. Insight Engine
A rule-based system that generates structured outputs:
- Insight  
- Business implication  
- Recommended action  

Covered domains:
- Delivery performance  
- Customer satisfaction  
- Revenue concentration  
- Geographic performance  
- Freight cost  
- Review distribution  

### 3. Automated Business Reporting
Insights are compiled into a structured, executive-ready report.

### 4. Query-Based Insight System
A dynamic interface that:
- Classifies user intent  
- Routes queries to relevant analytical functions  
- Combines multiple insights into a single response  

### 5. Advanced Query Reasoning Layer
Enhances the system with:
- Multi-intent handling  
- Insight prioritization  
- Structured responses (Executive Answer, Key Takeaways, Detailed Insights)

### 6. Optional LLM Rewrite Layer
A lightweight local language model (FLAN-T5) is used to improve clarity and communication of the final output while keeping the analytical logic deterministic and transparent.

---

## Example Questions

The system can answer questions such as:

- What drives customer satisfaction and how is delivery performing?  
- Which categories generate the most revenue and what about freight costs?  
- What are the main business risks in the dataset?  

---

## Key Findings

- Delivery performance exceeds expectations, with orders arriving earlier than estimated on average  
- Customer satisfaction is strongly associated with delivery performance relative to expectations  
- Revenue is concentrated in a limited number of categories, creating both opportunities and risk  
- Freight cost varies significantly across categories and may impact conversion  

---

## Business Recommendations

- Treat delivery performance vs estimate as a core KPI  
- Optimize logistics in high-impact regions and sellers  
- Diversify category growth to reduce concentration risk  
- Investigate low-review segments for operational issues  
- Analyze high freight cost categories for margin and satisfaction impact  

---

## Tech Stack

- Python  
- Pandas  
- Jupyter Notebook  
- Hugging Face Transformers (FLAN-T5)  

---

## Limitations

- The insight engine is rule-based and does not learn from new data  
- Query understanding relies on intent classification rather than full natural language reasoning  
- The LLM layer is optional and lightweight, prioritizing interpretability over generative capability  

---

## Future Improvements

- Integrate more advanced LLMs for improved reasoning  
- Expand to additional data sources (seller, product-level features)  
- Build an interactive interface (e.g. Streamlit)  
- Introduce feedback loops for adaptive insights  

---

## How to Run

1. Open the notebook:
2. Run all cells from top to bottom
3. Outputs will be saved in: outputs/

---

## Final Note

This project focuses on bridging the gap between data analysis and business decision-making by combining structured analytics with an intent-driven insight system.

It reflects how modern data teams move beyond dashboards toward interactive, decision-support tools.
