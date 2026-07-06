# 🚨 ResQLink

### AI-Powered Disaster Response & Evacuation Agent

ResQLink is an AI-powered disaster response and evacuation web application developed for the **Google Agents Competition** under the **Agents for Good** category.

The platform assists citizens, shelter administrators, rescue teams, and disaster management authorities during emergencies by providing intelligent disaster guidance, shelter recommendations, rescue request management, and emergency resource coordination through Google's Gemini AI.

---

## 🌟 Features

### 👤 Citizen Portal
- User Registration & Login
- AI Emergency Assistant
- Disaster Alerts
- Emergency (SOS) Reporting
- Shelter Search
- Emergency Checklist
- Family Status Tracking
- Notification Center

### 🏠 Shelter Management
- Add, Edit, Delete Shelters
- Shelter Capacity Tracking
- Shelter Availability
- Resource Availability
- Shelter Status Management

### 🚑 Rescue Management
- Submit Rescue Requests
- Rescue Request Prioritization
- Rescue Status Tracking
- Rescue Team Dashboard

### 🤖 AI Emergency Agent
Powered by **Google Gemini API**

The AI agent can:
- Answer disaster-related questions
- Provide emergency guidance
- Recommend suitable shelters
- Generate personalized emergency checklists
- Prioritize rescue requests
- Summarize disaster reports for administrators

### 📊 Admin Dashboard
- User Management
- Shelter Management
- Resource Management
- Rescue Management
- Dashboard Analytics

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite

### Artificial Intelligence
- Google Gemini API

### Deployment
- Local server

---

## 📁 Project Structure

```text
ResQLink/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
├── database/
│   ├── db.py
│   ├── schema.sql
│   └── resqlink.db
│
├── routes/
│   ├── auth.py
│   ├── citizen.py
│   ├── admin.py
│   ├── shelter.py
│   ├── rescue.py
│   └── ai_agent.py
│
├── agents/
│   └── gemini.py
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/FatemaAkter247/Capstone__GoogleXKaggale

cd ResQLink
```

### 2. Create a Virtual Environment

Windows

```bash
python -m venv venv
```

Activate it

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
SECRET_KEY=YOUR_SECRET_KEY
```

---

### 5. Run the Application

```bash
python app.py
```

or

```bash
flask run
```

Open:

```
http://127.0.0.1:5000
```

---

## 📦 Dependencies

- Flask
- python-dotenv
- google-generativeai
- gunicorn

Install manually if needed:

```bash
pip install flask python-dotenv google-generativeai gunicorn
```

---

## 🤖 AI Agent Workflow

1. User submits an emergency request.
2. The AI agent analyzes the situation.
3. It asks follow-up questions if required.
4. The system retrieves shelter information from the database.
5. The AI recommends the most suitable shelter.
6. An emergency checklist is generated.
7. Rescue requests are prioritized for administrators.

---

## 🔒 Security

- Password Hashing
- Session Authentication
- Environment Variables for API Keys
- Input Validation
- Secure Flask Configuration

---

## 🎯 Target Users

- Citizens
- Shelter Administrators
- Rescue Teams
- Disaster Management Authorities

---

## 💡 Future Enhancements

- SMS & Email Notifications
- Real-Time Weather Integration
- Firebase Authentication
- Multi-Language Support
- Offline Emergency Guide
- Voice Interaction
- Image Upload for Damage Assessment

---

## 👩‍💻 Developed By

**Fatema Akter**

Capstone Project

Google AI Vibecoding Competition 2026

---

## 📄 License

This project is developed for educational and competition purposes.

---

## 🙏 Acknowledgements

- Google AI Studio
- Flask
- Bootstrap
- SQLite
- Python Community
