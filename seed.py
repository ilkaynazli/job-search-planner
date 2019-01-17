"""
    seed file for the database
"""

from sqlalchemy import func
from model import Topic
from model import connect_to_db, db, db_name
from server import app

def interview_topics():
    """Load interview topics from topics.txt into database."""

    print("Loading topics")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate questions
    Topic.query.delete()

    # Read the file and insert data one by one
    for row in open("data/topics.txt"):
        row = row.rstrip()
        topic = Topic(topic=row)   
        db.session.add(topic)

    db.session.commit()

if __name__=='__main__':
    connect_to_db(app, db_name)

    # In case tables haven't been created, create them
    db.create_all()

    interview_topics()