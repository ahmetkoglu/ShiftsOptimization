# 🗓️ Shift Optimization & Resource Allocation Engine

An industrial-grade Decision Support System (DSS) developed at the intersection of **Computer Engineering** and **Industrial Engineering**. This engine solves complex workforce scheduling problems using **Mixed-Integer Linear Programming (MILP)** to ensure optimal resource distribution while adhering to labor regulations and operational constraints.

---

## 🚀 Project Overview

In many industries, manual shift planning is time-consuming and prone to human error. This project provides a modular Python-based solver that transforms business requirements into mathematical models. By using the **PuLP** library and the **CBC Solver**, it identifies the most efficient schedule that minimizes staffing costs while balancing workload.

[Image of Mixed-Integer Linear Programming graph and feasible region]

## ✨ Key Features

- **Mathematical Optimization:** Uses MILP to find the global optimum rather than just a "good enough" heuristic solution.
- **Dinamik Configuration:** All variables (employees, shifts, days) and constraints are managed via a `config.json` file—no code changes required for different scenarios.
- **Automated Reporting:** Generates a professional **Excel (.xlsx)** shift roster using `Pandas` for immediate operational use.
- **Smart Constraint Handling:**
    - **Staffing Requirements:** Ensures minimum personnel for every shift.
    - **Labor Laws:** Prevents double shifts within the same day (24-hour rule).
    - **Work-Life Balance:** Limits maximum weekly shifts per employee to prevent burnout.

## 🛠️ Tech Stack

| Technology | Usage |
| :--- | :--- |
| **Python 3.x** | Core logic and scripting |
| **PuLP** | Linear Programming API & Modeling |
| **Pandas** | Data Transformation & Matrix Operations |
| **OpenPyXL** | Excel Generation Engine |
| **JSON** | Configuration and Input Data Management |

## 📂 Project Structure

```text
ShiftsOptimization/
├── optimizer.py       # Core optimization logic & solver
├── config.json        # Input data (Employees, Shifts, Constraints)
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation