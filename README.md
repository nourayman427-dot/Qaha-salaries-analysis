# Qaha-salaries-analysis
An interactive HR Analytics Dashboard built using Streamlit &amp; Python . It analyzes employee salaries, deductions, incentives and KPI tracking with Plotly visualizations.

# 📊 HR & Salaries Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b)
![Plotly](https://img.shields.io/badge/Plotly-Express-success)

An interactive **Human Resources Dashboard** built using **Python** and **Streamlit**. 
This project transforms raw HR Excel data into actionable insights, helping management analyze salaries, deductions, incentives, and departmental costs.

The dashboard is designed to handle **Arabic datasets (RTL)** seamlessly while presenting the user interface and Key Performance Indicators (KPIs) in **English**.

## 🌟 Key Features

### 1. 🎛️ Dynamic Filtering (Slicer)
*   A sidebar dropdown menu allows users to filter data by a specific **Department** or view analytics for **All Departments**.
*   The dashboard updates instantly based on the selection.

### 2. 📈 KPIs & Metrics
Key metrics are displayed in centered, easy-to-read cards:
*   **Total Employees:** Count of active workforce.
*   **Total Departments:** Number of active departments.
*   **Deduction Ratio:** Percentage of total deductions vs. total due.
*   **Incentive Ratio:** Percentage of incentives vs. total due.

### 3. 📊 Interactive Visualizations
Powered by **Plotly Express** for rich interactivity:
*   **Bar Chart:** Distribution of employees across departments.
*   **Pie Chart:** Salary categorization (High / Medium / Low).
*   **Cost Analysis:** Top 5 departments by total Net Salary.
*   **Stacked Bar:** Breakdown of salary categories within each department.
*   **Boxplot:** Statistical detection of salary outliers.

### 4. 🧹 Smart Data Cleaning
The application automatically cleans the raw Excel file:
*   **Auto-Path Detection:** Locates `salaries2.xlsx` automatically in the directory.
*   **Noise Removal:** Filters out administrative rows (e.g.,NAN,"أسم العامل", "اجمالي").
*   **Format Handling:** Trims whitespace and handles mixed data types.
*   **Handling missing** columns and raws by removing them.
*   **Assuring correct** data type for all data columns.

---

## 🛠️ Tech Stack

*   **Python:** Core programming language.
*   **Streamlit:** For building the web application interface.
*   **Pandas:** For data manipulation and cleaning.
*   **Plotly Express:** For interactive charts and graphs.
*   **OpenPyXL:** Engine to read Excel files.

---

## 📂 Project Structure

```text
├── salaries_streamlit.py       # The main application script
├── salaries2.xlsx       # The HR dataset (Excel file)
└── README.md            # Project documentation


