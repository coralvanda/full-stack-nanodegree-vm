-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS players;

CREATE TABLE players (id SERIAL PRIMARY KEY, name TEXT, 
 wins INTEGER DEFAULT 0, matches INTEGER DEFAULT 0);

DROP TABLE IF EXISTS matches;
 
CREATE TABLE matches (p1 integer references players(id),
  name1 text, 
  p2 integer references players(id), 
  name2 text);

