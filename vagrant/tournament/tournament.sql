-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (id SERIAL PRIMARY KEY, name TEXT, wins INTEGER, matches INTEGER);

CREATE TABLE matches (p1 integer references players(id), 
  p2 integer references players(id), 
  results integer references players(id));

