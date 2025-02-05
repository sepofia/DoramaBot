CREATE TABLE tv_series
(
    id                  INTEGER PRIMARY KEY,
    name_movie          VARCHAR(100),
    kp_rating           NUMERIC,
    imdb_rating         NUMERIC,
    production_year     INTEGER,
    link                VARCHAR(100),
    description         TEXT,
    all_countries       VARCHAR(200),
    all_genres          VARCHAR(200)
);

-- DROP TABLE tv_series;

CREATE TABLE countries
(
    id              INTEGER PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES tv_series(id),
    south_korea     BOOLEAN,
    china           BOOLEAN,
    japan           BOOLEAN
);

-- DROP TABLE countries;

CREATE TABLE genres
(
    id              INTEGER PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES tv_series(id),
    biography       BOOLEAN,
    action_movie    BOOLEAN,
    military        BOOLEAN,
    detective       BOOLEAN,
    drama           BOOLEAN,
    history         BOOLEAN,
    comedy          BOOLEAN,
    criminal        BOOLEAN,
    melodrama       BOOLEAN,
    music           BOOLEAN,
    adventures      BOOLEAN,
    thriller        BOOLEAN,
    horrors         BOOLEAN,
    fantastic       BOOLEAN,
    fantasy         BOOLEAN
);

-- DROP TABLE genres;

CREATE TABLE users
(
    id              INTEGER PRIMARY KEY,
    user_login      VARCHAR(200),
    first_name      VARCHAR(200),
    language_code   VARCHAR(50),
    is_premium      BOOLEAN DEFAULT FALSE,
    is_bot          BOOLEAN DEFAULT FALSE
);

-- DROP TABLE users;

CREATE TABLE commands
(
    id              INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id         INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    command_type    VARCHAR(100),
    date_time       TIMESTAMP,
    result          BOOLEAN
);

-- DROP TABLE commands;

CREATE TABLE commands_select
(
    id          INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    command_id  INTEGER,
    FOREIGN KEY (command_id) REFERENCES commands(id),
    genre       VARCHAR(100),
    min_year    INTEGER,
    country     VARCHAR(100),
    count       INTEGER,
    answer_mode VARCHAR(100)
);

-- DROP TABLE commands_select;
