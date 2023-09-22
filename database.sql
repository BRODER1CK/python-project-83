DROP TABLE IF EXISTS url_checks CASCADE;
DROP TABLE IF EXISTS urls CASCADE;

CREATE TABLE urls
(
    id         SERIAL,
    name      TEXT UNIQUE,
    created_at DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE url_checks
(
    id          SERIAL,
    url_id      INTEGER,
    status_code INTEGER,
    h1          TEXT,
    title       TEXT,
    description TEXT,
    created_at  DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (url_id) REFERENCES urls (id) ON DELETE CASCADE ON UPDATE CASCADE
);