CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);


INSERT INTO users (username, password) VALUES ('whale120', '0e47b305279eb4d43aa909dea68b5a92');