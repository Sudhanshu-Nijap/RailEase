# RailEase

## 🚆 Overview
This is a Flask-based web application that provides real-time Indian Railways train information and schedules using the **Indian Rail API**. Users can search for train details and view their schedules.

## 🔧 Features
- Retrieve train details including name, source, and destination.
- Fetch train schedules with all station stops.
- Simple and user-friendly web interface.

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **API:** [IndianRail API](https://indianrailapi.com/)

## 🚀 Installation
### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/train-info-app.git
cd train-info-app
```
### 2. Create and Activate Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
### 3. Install Dependencies
```sh
pip install -r requirements.txt
```
### 4. Run the Application
```sh
python app.py
```
Visit **http://127.0.0.1:5000/** in your browser.

## 🔑 API Key Setup
1. Sign up at [IndianRail API](https://indianrailapi.com/).
2. Replace `API_KEY` in `app.py` with your actual API key.

## 📁 Project Structure
```
flask app/
│── templates/
│   ├── index.html
│   ├── train_info.html
│   ├── train_schedule.html
│   ├── error.html
│── train_app.py
│── requirements.txt
│── README.md
```

## 📜 License
This project is open-source under the MIT License.

## 🌟 Contributing
Feel free to fork this repository and submit pull requests for improvements.

---
Made with ❤️ by Sudhanshu

