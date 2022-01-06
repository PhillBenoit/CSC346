CREATE TABLE servers (
    id          INT         AUTO_INCREMENT,
    owner       VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    ec2id       VARCHAR(30) NOT NULL,
    ready       INT         DEFAULT 0,
    user1pw     CHAR(4)     NOT NULL,
    user2pw     CHAR(4)     NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT ready_bool CHECK (ready BETWEEN 0 AND 1)
)