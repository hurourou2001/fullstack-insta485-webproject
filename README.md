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
```
insta485/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── views.py                 # Flask route handlers (HTML pages)
│   ├── api.py                   # REST API endpoints (JSON responses)
│   ├── model.py                 # SQL database interactions
│   └── static/                  # Static assets
│       ├── js/                  # Frontend JavaScript (AJAX, etc.)
│       └── css/                 # Styling files
├── templates/                   # Jinja2 HTML templates
├── config.py                    # App configuration settings
├── requirements.txt             # Python dependencies
└── run.py                       # Entry point to launch the Flask app
```
