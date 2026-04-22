# 🛡️ PhishGuard AI: Real-Time Phishing Detection

**PhishGuard AI** is a state-of-the-art, full-stack cybersecurity platform designed to evaluate URLs in real-time. By leveraging a high-performance Machine Learning pipeline and advanced threat intelligence, it detects phishing vectors with precision and explains its reasoning through SHAP (SHapley Additive exPlanations).

![PhishGuard Banner](https://img.shields.io/badge/Security-PhishGuard%20AI-00D1FF?style=for-the-badge&logo=shield&logoColor=white)
![Build Status](https://img.shields.io/badge/Status-Working-brightgreen?style=for-the-badge)

---

## ✨ Features

- ⚡ **Real-Time Analysis**: Instant URL evaluation using a Random Forest Classifier.
- 🔍 **SHAP Explainability**: Deep transparency into *why* a URL was flagged, showing the specific features that influenced the model.
- 📡 **Threat Intelligence**: Integrated Geolocation tracking and WHOIS domain age lookup for comprehensive context.
- 🎨 **Premium UI**: A stunning, modern dark-mode interface built with **React**, **Vite**, **Tailwind CSS**, and **Framer Motion**.
- 🛠️ **Modular Backend**: A clean, asynchronously capable **FastAPI** server designed for scalability.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS, Lucide Icons, Framer Motion |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Machine Learning** | Scikit-Learn (Random Forest), SHAP, Joblib |
| **Intelligence** | WHOIS API, IP-API Geolocation |

---

## 🏗️ Architecture

### 1. Frontend (Client)
The frontend provides a "cyber-glassmorphism" aesthetic. It manages state for URL inputs and renders a complex results dashboard including prediction confidence, geolocation maps (placeholder), and explanation lists.

### 2. Backend (API)
The backend is organized into high-cohesion service modules:
- `feature_extractor.py`: Parses 6 critical URL features (Length, Dots, Symbols, etc.).
- `model_service.py`: Handles model persistence and auto-trains a synthetic model if no `model.pkl` is detected.
- `explain_service.py`: Generates human-readable explanations using TreeExplainer.
- `domain_utils.py`: Performs asynchronous lookups for domain metadata.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the server:
   ```bash
   python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 10000
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Access the application at `http://localhost:5173`.

---

## 🔧 Features Analyzed
The ML model evaluates URLs based on the following weighted features:
1. **URL Length**: Detection of long, obfuscated paths.
2. **Number of Dots**: Identifying excessive subdomains or tunneling.
3. **Presence of '@'**: Detection of user-info masking.
4. **Presence of '-'**: Identifying hyphenated spoofed brands.
5. **HTTPS Usage**: Validating secure communication protocols.
6. **Subdomain Count**: Measuring structural complexity of the domain.

---

## ✅ Recent Improvements
- **SHAP Integration Fix**: Resolved a compatibility error where SHAP expected a NumPy array instead of a list, ensuring the "ML Explanation" segment renders flawlessly (Fixed in `/backend/services/explain_service.py`).
- **Synchronized Workspace**: Consolidated the frontend and backend into a single unified repository for easier deployment.

---

## 📄 License
This project is for educational and cybersecurity research purposes. 
🛡️ **Stay Safe Online.**
