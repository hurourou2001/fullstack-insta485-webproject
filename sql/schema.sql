PRAGMA foreign_keys = ON;

CREATE TABLE users (
    username VARCHAR(20) NOT NULL,
    fullname VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    filename VARCHAR(64),
    password VARCHAR(256) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username)
);

-- Create posts table
CREATE TABLE posts (
    postid INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(64) NOT NULL,
    owner VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE
);

-- Create following table
CREATE TABLE following (
    username1 VARCHAR(20) NOT NULL,
    username2 VARCHAR(20) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username1, username2),
    FOREIGN KEY(username1) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY(username2) REFERENCES users(username) ON DELETE CASCADE
);

-- Create comments table
CREATE TABLE comments (
    commentid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL,
    postid INTEGER NOT NULL,
    text VARCHAR(1024) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY(postid) REFERENCES posts(postid) ON DELETE CASCADE
);

-- Create likes table
CREATE TABLE likes (
    likeid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL,
    postid INTEGER NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY(postid) REFERENCES posts(postid) ON DELETE CASCADE
);