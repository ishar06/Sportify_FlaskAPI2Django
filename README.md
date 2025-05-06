# 🛒 Sportify - E-Commerce Website

Sportify is a full-featured e-commerce platform built using two popular Python web frameworks: **Flask** and **Django**. This project demonstrates the implementation of core e-commerce functionalities such as product listing, cart management, checkout, user authentication, and more.

---

## 📁 Repository Structure

```bash
Sportify/
│
├── Sportify_Flask/        # Flask-based implementation of Sportify
└── Sportify_Django/       # Django-based implementation of Sportify
```

---

## ⚙️ Setup Instructions

### 🐍 1. Clone the Repository

```bash
git clone https://github.com/ishar06/Sportify_FlaskAPI2Django.git
cd Sportify_FlaskAPI2Django
```

---

## 🚀 Running the Flask Project (Sportify_Flask)

### ✅ Step-by-step Setup:

1. Navigate to the Flask project directory:

   ```bash
   cd Sportify_Flask
   ```

2. Create and activate a virtual environment:

   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:

   ```bash
   python app.py
   ```

5. Open your browser and go to:

   ```
   http://127.0.0.1:5000
   ```

---

## 🧩 Running the Django Project (Sportify_Django)

### ✅ Step-by-step Setup:

1. Open a **new terminal** and navigate to the Django project directory:

   ```bash
   cd Sportify_Django
   ```

2. Create and activate a virtual environment:

   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional but recommended):

   ```bash
   python manage.py createsuperuser
   ```

6. Run the Django development server:

   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to:

   ```
   http://127.0.0.1:8000
   ```

---

## 🧪 Features Implemented

✅ User authentication (Sign up, Login, Logout)  
✅ Product catalog with categories  
✅ Add to cart and checkout system  
✅ Admin dashboard for product and user management  
✅ Pagination, filters, and search  
✅ Responsive UI using Bootstrap  
✅ SQLite as the database backend  
✅ Additional UX elements like modals, animations, etc.

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Make your changes and commit (`git commit -m 'Add some feature'`)  
4. Push to the branch (`git push origin feature-name`)  
5. Open a Pull Request

---

## 🙋‍♂️ Team

**Team Leader:** Ishar  
**Contributors:** Aryan, Damanjeet, Madhav

---
