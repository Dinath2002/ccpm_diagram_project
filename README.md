# 🧭 Critical Chain Project Management (CCPM) Diagram Generator

This repository contains a **Python script** that visualizes a **Critical Chain Project Management (CCPM) schedule** with buffers, based on the *Online Examination System Upgrade Project* scenario from the IT Project Management (ITE2612) coursework.

---

## 🎯 Project Overview

The goal of this script is to demonstrate how **Critical Chain Project Management (CCPM)** applies to real-world IT projects.  
It visually represents:
- The **Critical Chain (A → I)** sequence
- **Feeding Buffers (FB)** for dependent chains
- **Resource Buffers (RB)** as alerts for resource constraints
- **Project Buffer (PB)** protecting the final delivery

This visualization helps illustrate how CCPM manages **uncertainty, time, and resource constraints** to ensure on-time project completion.

---

## 🧩 Features

- Clean and professional **Matplotlib-based diagram**
- Shapes follow CCPM conventions from PMI slides:
  - **Rounded rectangles** → Tasks  
  - **Trapezoids** → Feeding / Project Buffers  
  - **Triangles** → Resource Buffers  
- Exported automatically as `.png`, `.pdf`, and `.svg`
- Easy to modify task names and dependencies

---

## 🧠 Scenario Summary

The **Online Examination System Upgrade** includes:
- Modern UI & mobile-friendly access  
- Enhanced exam management and grading tools  
- Real-time dashboards for faculty and admin users  
- Integration testing and final go-live before semester start  

The CCPM approach ensures the upgrade meets deadlines even under **tight schedules and limited resources**.

---

## ⚙️ Requirements

Make sure Python and Matplotlib are installed:

```bash
sudo dnf install python3-pip -y
pip install matplotlib
