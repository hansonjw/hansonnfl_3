DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS league;
DROP TABLE IF EXISTS pick;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    pwhash TEXT NOT NULL,
    displayname TEXT NOT NULL
);

CREATE TABLE team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamname TEXT,
    league_id INTEGER,
    FOREIGN KEY (league_id) REFERENCES league (id)
);

CREATE TABLE league (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_desc TEXT,
    game_conf INTEGER,
    game_round TEXT,
    teamhome INTEGER,
    teamvisitor INTEGER,
    winner INTEGER,
    FOREIGN KEY (teamhome) REFERENCES team (id),
    FOREIGN KEY (teamvisitor) REFERENCES team (id),
    FOREIGN KEY (winner) REFERENCES team (id),
    FOREIGN KEY (game_conf) REFERENCES league (id)
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