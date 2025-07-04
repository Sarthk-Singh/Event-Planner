
# 🎉 Social in the Hills — Event Planner App

> A smart, QR-powered event management system to plan, organize, and run social gatherings with ease.

![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&style=for-the-badge)
![Python](https://img.shields.io/badge/Built%20With-Python-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

---

## 📸 Overview

This app helps you manage real-world social events with digital flair:
- ✅ Track attendees, payments, and check-ins  
- ✅ Manage menu and orders with per-person ₹1000 credit  
- ✅ Auto-generate and download QR codes for each guest  
- ✅ Real-time summaries with filters and financial breakdowns  
- ✅ Hosted on **Streamlit Cloud** + GitHub Pages QR viewer

---

## 🚀 Live App

🔗 **[Open App →](https://event-planner-social-in-the-hills.streamlit.app)**

---

## 📦 Features

| Feature               | Description                                           |
|-----------------------|-------------------------------------------------------|
| 🧑‍🤝‍🧑 Attendee Manager | Add/remove guests, track payment + check-in status     |
| 📋 Menu Upload         | Upload `.csv` menu (item + price)                    |
| 🛒 Order System        | Track orders per attendee, enforce ₹1000 cap         |
| 🧾 Order Summary       | View per-person spend, live remaining credit         |
| 🎟️ Check-In Page       | Mark attendees as checked in using their ID          |
| 📎 QR Code Generator   | Generate QR for each attendee with their info        |
| 🌐 QR Web Viewer       | Scan QR and view data in browser via GitHub Pages    |
| 📊 Summary Analytics   | Live headcount, total revenue, checked-in stats      |

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/<your-username>/event-planner.git
cd event-planner
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📁 Folder Structure

```
Event Planner/
├── app.py                # Main Streamlit app
├── generate_qr.py        # QR generator utility
├── requirements.txt
├── /data/                # App data (CSV files)
│   ├── attendees.csv
│   ├── menu.csv
│   └── orders.csv
├── /qrcodes/             # Saved QR PNGs
├── /docs/                # GitHub Pages QR Viewer (HTML only)
│   └── checkin.html
```

---

## 🔐 Security & Limitations

- This app is for internal/event use — not for public/commercial deployment.
- All data is stored locally in `.csv` files.
- QR codes use plaintext — no encryption.
- No login/auth currently; security is manual.

---

## 🙌 Credits

Made with ❤️ by [Sarthak Singh](https://github.com/yourusername)  
Tech Stack: `Streamlit` + `Pandas` + `QRCode` + `GitHub Pages`

---

## 🧠 Future Upgrades

- 🔒 Login & authentication for admin access  
- ☁️ Firebase/Supabase integration  
- 💳 Payment gateway support (Razorpay, Paytm, etc.)  
- 📱 Mobile responsive redesign  
- 📊 Admin analytics dashboard  

---

## 🪪 License

This project is open for educational and personal event use.  
Feel free to remix, extend, and improve it. Just give credit 🙌
