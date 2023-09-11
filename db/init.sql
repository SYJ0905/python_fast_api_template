-- 創建數據庫
CREATE DATABASE IF NOT EXISTS message_board;

-- 選擇該數據庫
USE message_board;

-- 創建表格 (在新容器中添加新表，如果它不存在)
CREATE TABLE IF NOT EXISTS user (
    user_id VARCHAR(64) NOT NULL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    age INTEGER,
    email VARCHAR(64) UNIQUE
);

CREATE TABLE IF NOT EXISTS password (
    user_id VARCHAR(64) NOT NULL PRIMARY KEY,
    password_hash VARCHAR(128),
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS message (
    message_id VARCHAR(36) NOT NULL PRIMARY KEY,
    content VARCHAR(200) NOT NULL,
    create_account VARCHAR(64),
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reply (
    reply_id VARCHAR(36) NOT NULL PRIMARY KEY,
    content VARCHAR(200) NOT NULL,
    create_account VARCHAR(64),
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    message_id VARCHAR(36),
    CONSTRAINT fk_reply_message FOREIGN KEY (message_id) REFERENCES message (message_id) ON DELETE CASCADE
);


