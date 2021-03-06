"""
    the database model of job search planner web app
"""

from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime

"""Import SQLAlchemy object from flask_sqlalchemy library and make the 
    connection to PostgreSQL"""

db = SQLAlchemy()   #create an instance of SQLAlchemy object

class User(db.Model):
    """Users of the website"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        )
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    applications = db.relationship('Application')

    def __repr__(self):
        """Human readable data"""
        return f"<User id: {self.user_id}, \
                    username: {self.username},\
                    password: {self.password},\
                    email: {self.email}>"


class Company(db.Model):
    """Company names, etc for the jobs applied"""

    __tablename__ = 'companies'

    company_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            )
    company_name = db.Column(db.String(50), nullable=False)
    company_website = db.Column(db.String(150), nullable=True)
    
    applications = db.relationship('Application')

    def __repr__(self):
        """Human readable data"""
        return f"<Company id: {self.company_id}, \
                    name: {self.company_name},\
                    website: {self.company_website}>"


class Application(db.Model):
    """Applications to the companies"""

    __tablename__ = 'applications'

    application_id = db.Column(db.Integer,
                                primary_key=True,
                                autoincrement=True,
                                )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    company_id = db.Column(db.Integer,
                        db.ForeignKey('companies.company_id'),
                        nullable=False
                        )
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    #check this one later!!!!
    position = db.Column(db.String(50), nullable=False)
    resume = db.Column(db.String(50), nullable=True)    #the location of the file 
    cover_letter = db.Column(db.String(50), nullable=True)  #the location of the file
    summary = db.Column(db.Text, nullable=True)
    referer_id = db.Column(db.Integer,
                            db.ForeignKey('referers.referer_id'),
                            nullable=False
                            )


    user = db.relationship('User')
    company = db.relationship('Company')
    referer = db.relationship('Referer')


    def __repr__(self):
        """Human readable data"""
        return f"<Application id: {self.application_id}, \
                    company id: {self.company_id},\
                    user id: {self.user_id}, \
                    date applied: {self.date_applied},\
                    position: {self.position},\
                    resume: {self.resume},\
                    cover letter: {self.cover_letter},\
                    summary: {self.summary},\
                    referer id: {self.referer_id}>"


class Referer(db.Model):
    """Contact in company applied"""

    __tablename__ = 'referers'

    referer_id = db.Column(db.Integer, 
                            primary_key=True,
                            autoincrement=True,
                            )
    referer_name = db.Column(db.String(75), nullable=False)

    application = db.relationship('Application')

    def __repr__(self):
        """Human readable data"""
        return f"<Referer id: {self.referer_id}, \
                    referer name: {self.referer_name}>"


class Interview(db.Model):
    """Topics asked in interview"""

    __tablename__ = 'interviews'

    interview_id = db.Column(db.Integer,
                                primary_key=True,
                                autoincrement=True,
                                )
    topic_id = db.Column(db.Integer,
                        db.ForeignKey('topics.topic_id'),
                        nullable=False
                        )
    application_id = db.Column(db.Integer,
                        db.ForeignKey('applications.application_id'),
                        nullable=False
                        )
    improvement = db.Column(db.Boolean, nullable=False)


    application = db.relationship('Application')
    topic =  db.relationship('Topic')

    def __repr__(self):
        """Human readable data"""
        return f"<interview id: {self.interview_id},\
                    topic id: {self.topic_id},\
                    application id: {self.application_id},\
                    improvement: {self.improvement}>"

                    
class Topic(db.Model):
    """Interview topics that could be asked"""

    __tablename__ = 'topics'

    topic_id = db.Column(db.Integer, 
                            primary_key=True,
                            autoincrement=True,
                            )
    topic = db.Column(db.String(150), nullable=False)


    def __repr__(self):
        """Human readable data"""
        return f"<Topic id: {self.topic_id},\
                    topic: {self.topic}>"


def connect_to_db(app, db_name):
    """Connect to database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_ECHO'] = True    #For debugging purposes keep this True
    db.app = app
    db.init_app(app)


db_name = 'jobs'


if __name__ == '__main__':
    """For running this interactively"""

    from server import app

    connect_to_db(app, db_name)

    db.create_all()
    # example_data()

    print('Connected to database.')