DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS opening;
DROP TABLE IF EXISTS game;

CREATE TABLE player (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL
);

CREATE TABLE opening(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  short_name TEXT,

  UNIQUE(id, name, short_name)
);

CREATE TABLE game (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lichess_id TEXT UNIQUE NOT NULL,
  is_lose INT,
  is_draw INT,
  player_id INTEGER NOT NULL,
  opening_id INTEGER NOT NULL,

  FOREIGN KEY (player_id) REFERENCES player (id),
  FOREIGN KEY (opening_id) REFERENCES opening (id)
);
