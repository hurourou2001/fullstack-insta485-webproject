# Insta485 - Instagram Clone

This project is a simplified clone of Instagram, developed as part of the EECS 485 Web Systems course. It demonstrates a full-stack web application with core social media features, including user authentication, posting, liking, following, and more.

## 🚀 Features

- User registration and login with secure session handling
- Post creation with image uploads and captions
- Like/unlike functionality on posts
- Follow/unfollow other users
- Dynamic user profiles with follower/following counts
- RESTful API endpoints supporting asynchronous frontend behavior
- Responsive frontend built with JavaScript and AJAX

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML, CSS, JavaScript (AJAX/Fetch API)
- **Authentication**: Flask sessions and password hashing

## 📂 Project Structure
'''insta485/
├── app/
│ ├── init.py
│ ├── views.py # Flask route handlers
│ ├── api.py # REST API endpoints
│ ├── model.py # Database schema and queries
│ └── static/ # Static JS/CSS/image files
│ ├── js/
│ └── css/
├── templates/ # Jinja2 HTML templates
├── config.py # App configuration
├── requirements.txt # Python dependencies
└── run.py # App entry point'''
