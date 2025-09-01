# 📝 Crafted -  Write. Share. Connect.   

![Django](https://img.shields.io/badge/Django-REST_Framework-green?style=flat-square&logo=django)  
![JWT](https://img.shields.io/badge/Auth-JWT-blue?style=flat-square)  


A modern AI-powered platform where users can share blogs and showcase their projects built with **Django REST Framework (DRF)** and **JWT authentication**.  
Users can **create, explore, and even generate blogs with AI** on any topic , showcase your projects effortlesly.  

---

## ✨ Features  

- 🔑 JWT Authentication (login/register/refresh)  
- 📝 Create, update, delete blog/project posts  
- 🔍 Explore blogs from other users  
- 🔍 Search and apply filters , find trending or latest posts
- ❤️ Like & comment system  
- 🤖 **AI-powered blog generation**  
- 👤 Easy to use interactive UI/UX

---

## 🚀 Installation  

```bash
# Clone the repository
git clone https://github.com/bhavy-Official/crafted.git
cd crafted

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

## 📡 API Endpoints

### 🔐 Authentication
- **POST** `/api/auth/register/` → Register a new user  
- **POST** `/api/auth/login/` → Login with JWT and get access/refresh tokens  
- **POST** `/api/auth/refresh/` → Refresh JWT access token  
- **POST** `/api/auth/logout/` → Blacklist JWT access token  

### 📝 Posts
- **GET** `/api/posts/` → Get all posts (blogs and projects)  
- **GET** `/api/posts/{id}/` → Get single post by ID  
- **POST** `/api/posts/create/` → Create a new post *(auth required)*

### 🤖 Like and Comments 
- **POST** `/api/posts/{id}/comments/` → Write comments (auth required)
- **POST** `/api/posts/{id}/like/` → Like post (auth required)

### 🤖 AI Features
- **POST** `/api/posts/ai-generate/` → Generate blog content with AI *(auth required , pass the topic too)*  

## 🛠 Tech Stack

Backend: Django, Django REST Framework (DRF)

Auth: JWT (djangorestframework-simplejwt)

Database: SQLite (default) / PostgreSQL (production ready)

Frontend: HTML, CSS, JS (React to be extended)

AI: API based

## ©️ Copyright
© 2025 Bhavy Manchanda. Unauthorized use, copying, or distribution of this project without explicit permission is strictly prohibited.


## Made by Bhavy Manchanda
```Built with ❤️ using Django REST Framework.```
