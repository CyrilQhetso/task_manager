# 📝 Flask Task Manager

A full-featured task management web app built with **Flask**, allowing users to register, log in, and manage their tasks with priorities, deadlines, and filtering options.


## 🚀 Features

- 🔐 User authentication (register, login, logout)
- ✅ Create, update, complete, and delete tasks
- 📅 Add deadlines and priorities to tasks
- 🔍 Filter tasks by completion status or priority
- 🧠 Flash messages for better UX
- 🎨 Responsive UI with Bootstrap

## 🛠 Technologies Used

- **Python 3.10+**
- **Flask** & **Flask-WTF**
- **Flask-Login** & **Flask-SQLAlchemy**
- **Bootstrap 5**
- **SQLite** for development (can be swapped with PostgreSQL)
- **Jinja2** templating

## 📁 Project Structure
task_manager/
├── app/
│ ├── init.py
│ ├── models.py
│ ├── forms.py
│ ├── routes.py
│ ├── templates/
│ └── static/
├── config.py
├── run.py
├── requirements.txt
└── README.md


## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/CyrilQhetso/task_manager.git
   cd task_manager

2. **Create a virtual environment**
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
4. **Install dependencies**
   pip install -r requirements.txt
   
6. **Set the environment variable**
   export SECRET_KEY='your-secret-key'  # On Windows use `set`

7. **Run the application**
   python run.py
