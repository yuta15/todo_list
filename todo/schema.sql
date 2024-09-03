DROP TABLE IF EXISTS todo;

CREATE TABLE todo(
    id INTEGER PRIMARY KEY, 
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME  NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    is_state  BOOLEAN NOT NULL DEFAULT False
    );
