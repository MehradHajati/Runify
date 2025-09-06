SET FOREIGN_KEY_CHECKS=0;
DROP TABLE users;
DROP TABLE playlists;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_name VARCHAR(255) NOT NULL,
    height int NOT NULL,
    sex int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

