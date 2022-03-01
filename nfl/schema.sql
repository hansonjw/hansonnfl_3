DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS pick;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS game;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    pwhash TEXT NOT NULL,
    displayname TEXT NOT NULL
);

CREATE TABLE pick (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (game_id) REFERENCES game (id),
    FOREIGN KEY (team_id) REFERENCES team (id)
);

CREATE TABLE team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamname TEXT,
    division TEXT
);

CREATE TABLE game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_desc TEXT,
    teamhome TEXT,
    teamvisitor TEXT,
    winner TEXT
);
