CREATE TABLE sessions (
    session_id CHAR(64)    NOT NULL,
    user       VARCHAR(50) NOT NULL,
    PRIMARY KEY (user)
)