# 🧮 Equity Valuation Toolkit

A collection of Python-based tools for the valuation of equities using fundamental finance methodologies. This repository includes modular scripts and notebooks for Discounted Cash Flow (DCF) models, WACC calculation, and other financial metrics — built for analysts, investors, and financial engineers.

---

## 📦 Features

- ✅ **DCF Models** – Flexible and customizable Discounted Cash Flow valuation models.
- 📊 **WACC Calculator** – Weighted Average Cost of Capital estimation with cost of debt and equity modules.
- 🔍 **Financial Ratios** – Computation of key valuation ratios from financial statements.
- 📈 **Scenario Analysis** – Tools to model different economic and strategic scenarios.
- 🧠 **Automation** – Load financial statements and compute outputs with minimal input.

---

## 🧰 Tools Included

| Tool                      | Description                                        |
|--------------------------|----------------------------------------------------|
| `dcf_model.py`           | Core logic for a DCF valuation                     |
| `wacc_calculator.py`     | Computes WACC based on capital structure inputs    |
| `valuation_utils.py`     | Helper functions for working capital, tax, etc.    |
| `example_notebook.ipynb` | Walkthrough with sample data (e.g., Apple, Tesla)  |

---

## 📂 Folder Structure

'''bash
equity-valuation-toolkit/
│
├── data/                   # Raw or cleaned financial data (optional)
├── models/                 # DCF and WACC Python modules
├── notebooks/              # Interactive Jupyter Notebooks
├── outputs/                # Results, charts, and model exports
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── setup.py                # (Optional) Setup for pip installation
'''

## 🚀 Getting Started
1. Clone the repo

git clone https://github.com/yourusername/equity-valuation-toolkit.git
cd equity-valuation-toolkit

2. Set up environment

'''pip install -r requirements.txt'''

3. Run example notebook

jupyter notebook notebooks/example_notebook.ipynb

## 🧾 Requirements

    Python 3.8+

    pandas, numpy, matplotlib, scipy

    Optional: yfinance, openpyxl, seaborn, plotly

You can install all dependencies with:

pip install -r requirements.txt

## 🧠 Inspiration

This project was born out of the need for a clean, reusable, and transparent Python-based framework for valuing companies. Whether you're a student, analyst, or investor — this toolkit aims to accelerate your equity research. Big thanks to Prof. Damodaran for all his free material on equities valuation. He has been the true inspiration for me

## 📬 Contributions

Contributions are welcome! Feel free to submit pull requests, suggest features, or open issues for discussion.

## 📝 License

MIT License. See LICENSE file for details.

## 🙋‍♂️ Author

Javi – LinkedIn | Website
