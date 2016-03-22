#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    database = connect()
    cursor = database.cursor()
    cursor.execute("DELETE FROM matches;")
    cursor.execute("UPDATE players set wins = 0;")
    cursor.execute("UPDATE players set matches = 0;")
    database.commit()
    database.close()

def deletePlayers():
    """Remove all the player records from the database."""
    database = connect()
    cursor = database.cursor()
    cursor.execute("DELETE FROM players;")
    database.commit()
    database.close()

def countPlayers():
    """Returns the number of players currently registered."""
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT COUNT(*) FROM players;")
    player_count = cursor.fetchall()[0][0]
    database.close()
    return player_count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    database.commit()
    database.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM players ORDER BY wins DESC;")
    standings = cursor.fetchall()
    database.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    database = connect()
    cursor = database.cursor()
    cursor.execute("UPDATE players SET wins = wins + 1 WHERE id = %s", (winner,))
    cursor.execute("UPDATE players SET matches = matches + 1 WHERE id = %s", (winner,))
    cursor.execute("UPDATE players SET matches = matches + 1 WHERE id = %s", (loser,))
    database.commit()
    database.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    database = connect()
    database.autocommit = True
    cursor = database.cursor()
    cursor.execute("DELETE FROM matches;")
    cursor.execute("SELECT id, name, wins FROM players ORDER BY wins DESC;")
    pairings = cursor.fetchall()
    previous_player = []
    for player in pairings:
        if previous_player:
            cursor.execute("INSERT INTO matches (p1, name1, p2, name2) VALUES (%s, %s, %s, %s);",
            (previous_player[0], previous_player[1], player[0], player[1]))
            previous_player = []
        else:
            previous_player = player
    cursor.execute("SELECT * FROM matches;")
    swiss_pairings = cursor.fetchall()
    database.close()
    return swiss_pairings
	


