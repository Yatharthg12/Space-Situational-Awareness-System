# Space Situational Awareness (SSA) – Conjunction Risk Monitoring System

## Overview
This project implements a short-horizon **Space Situational Awareness (SSA)** system that monitors satellite and orbital debris motion to detect potential close-approach (conjunction) risks using publicly available orbital data.

The system is designed to prioritize **deterministic physics-based modeling**, interpretability, and reproducibility over long-horizon prediction.

---

## Key Capabilities
- Ingests public Two-Line Element (TLE) data
- Propagates satellite and debris orbits using the SGP4 model
- Detects close approaches between objects
- Computes time of closest approach (TCA)
- Classifies conjunction risk using deterministic thresholds
- Generates persistent event logs
- Visualizes orbital motion in 3D

---

## System Architecture
TLE Data (Celestrak)
↓
Object Selection (CSV)
↓
Orbit Propagation (SGP4)
↓
Pairwise Distance Analysis
↓
Conjunction Risk Classification
↓
Results (CSV + 3D Visualization)

---

## Data Sources
- **Celestrak** (NORAD General Perturbations data)
  - Active Satellites
  - Space Stations
  - COSMOS-2251 Debris

All data is treated as a static snapshot to ensure reproducibility.

---

## Methodology

### Orbit Propagation
- Model: SGP4
- Reference frame: Earth-Centered Inertial (ECI)
- Time horizon: 48 hours
- Time step: 5 minutes

### Conjunction Detection
- Distance metric: Euclidean separation in ECI frame
- Time alignment: Shared propagation grid
- Risk thresholds:
  - **High risk:** < 2 km
  - **Medium risk:** 2–10 km

---

## Visualization
A 3D interactive orbital visualization is generated showing:
- Earth (reference sphere)
- Stations (red)
- Operational satellites (green)
- Debris fragments (orange)

Interactive visualization: `outputs/orbits.html`  
Downloadable report: `outputs/SSA_Report.pdf`

---

## Validation Strategy
To validate the detection pipeline, conjunction thresholds were temporarily relaxed to confirm correct event detection behavior. Normal operational thresholds were restored after validation.

---

## Operational Interpretation

A monitoring window with zero detected conjunction events is considered a nominal and valid operational outcome.

Most real-world SSA monitoring periods do not result in actionable alerts.  
The system is designed to confirm spatial separation as reliably as it detects close approaches.

---

## Limitations
- TLE accuracy degrades over time
- No collision probability modeling
- No maneuver or avoidance logic
- Short-horizon monitoring only

---

## Technologies Used
- Python 3.11
- SGP4
- NumPy
- Plotly

---

## Getting Started (Local Execution)

### Prerequisites
- Python 3.11
- pip
- Virtual environment (recommended)

### Setup
git clone https://github.com/Yatharthg12/Space-Situational-Awareness-System.git
cd Space-Situational-Awareness-System
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

### Run SSA Pipeline
python main.py

### Launch Dashboard
python app/dashboard.py
and open the local host live server

---

## Author
**Yatharth Garg**    
Space Systems & Defense-Oriented Software


**Note that this project is for academic and research purposes only. It uses publicly available orbital data and does not model real-world maneuvering or weapon systems.**

--- 

## License
**Use of this code is not permitted without prior authorization. Please contact the author to request permission.**
