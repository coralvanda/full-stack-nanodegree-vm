#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Get posts from database.
'''Get all the posts from the database, sorted with the newest first.
	
	Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
def GetAllPosts():
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    query = "SELECT time, content FROM posts ORDER BY time DESC;"
    cursor.execute(query)
    posts = [{'content': str(bleach.clean(item[1])), 'time': str(item[0])} for item in cursor.fetchall()]
    db.close()
    return posts
    

## Add a post to the database.
'''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
def AddPost(content):
    clean_content = bleach.clean(content)
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    
    cursor.execute("INSERT INTO posts (content) VALUES (%s);", (clean_content,))
    db.commit()
    db.close()