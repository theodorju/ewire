DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS message;

CREATE TABLE user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE message(
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    user_message TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE
);