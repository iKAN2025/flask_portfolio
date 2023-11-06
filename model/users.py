""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# # Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
# class Post(db.Model):
#     __tablename__ = 'posts'

#     # Define the Notes schema
#     id = db.Column(db.Integer, primary_key=True)
#     note = db.Column(db.Text, unique=False, nullable=False)
# #     image = db.Column(db.String, unique=False)
# #     # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
# #     userID = db.Column(db.Integer, db.ForeignKey('users.id'))

# #     # Constructor of a Notes object, initializes of instance variables within object
# #     def __init__(self, id, note, image):
# #         self.userID = id
# #         self.note = note
# #         self.image = image

# #     # Returns a string representation of the Notes object, similar to java toString()
# #     # returns string
# #     def __repr__(self):
# #         return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

# #     # CRUD create, adds a new record to the Notes table
# #     # returns the object added or None in case of an error
# #     def create(self):
# #         try:
# #             # creates a Notes object from Notes(db.Model) class, passes initializers
# #             db.session.add(self)  # add prepares to persist person object to Notes table
# #             db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
# #             return self
# #         except IntegrityError:
# #             db.session.remove()
# #             return None

# #     # CRUD read, returns dictionary representation of Notes object
# #     # returns dictionary
# #     def read(self):
# #         # encode image
# #         path = app.config['UPLOAD_FOLDER']
# #         file = os.path.join(path, self.image)
# #         file_text = open(file, 'rb')
# #         file_read = file_text.read()
# #         file_encode = base64.encodebytes(file_read)
        
# #         return {
# #             "id": self.id,
# #             "userID": self.userID,
# #             "note": self.note,
# #             "image": self.image,
# #             "base64": str(file_encode)
# #         }


# # Define the User class to manage actions in the 'users' table
# # -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# # -- a.) db.Model is like an inner layer of the onion in ORM
# # -- b.) User represents data we want to store, something that is built on db.Model
# # -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

# class Tracker(db.Model):
#     """Specification for Instrument table """
#     __tablename__ = 'trackers' #class name singular, table name plural
#     # Define the Notes schema
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String, db.ForeignKey('users.id'))
#     instrument = db.Column(db.String)
#     date = db.Column(db.String)
#     play_minutes = db.Column(db.Integer)
    
#     #object oriented programming. defines init (constructor).
#     def __init__(self, id, user_id, date, play_minutes):
#             self.id = id
#             self.user_id = user_id
#             self.date = date
#             self.play_minutes = play_minutes
  
#     def __repr__(self):
#             return "Tracker(" + str(self.id) + "," + self.instrument+ "," + str(self.date) + str(self.play_minutes) + ")"
    
#     def create(self):
#         try: #try and except to prevent errors
#             # creates a Instrument object from Instrument (db.Model) class, passes initializers
#             db.session.add(self)  # add prepares to persist person object to Instrument table
#             db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
#             return self
#         except IntegrityError:
#             db.session.remove()
#             return None

#     def read(self):
#         path = app.config['UPLOAD_FOLDER']
#         file = os.path.join(path, self.instrument)
#         file_text = open(file, 'rb')
#         file_read = file_text.read()
#         file_encode = base64.encodebytes(file_read)
        
#         return {
#             "id": self.id,
#             "user_id": self.user_id, 
#             "date": self.date,
#             "play_minutes": self.play_minutes,
#             "instrument": self.instrument,
#             "base64": str(file_encode)
#         }












class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _tracking = db.Column(db.JSON)

#If When I change the schema (aka add a field)….  I delete the .db file as it will generate when it does not exist.
#Do not have a underscore in a website name 
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
   # trackers = db.relationship("Tracker", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, tracking, password="123qwerty", dob=date.today() ):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self.tracking = tracking
        self.set_password(password)
        self._dob = dob
        self._tracking = tracking
        

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def tracking(self):
        return self._tracking
    
    @tracking.setter
    def tracking(self, tracking):
        self._tracking = tracking
        
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            "age": self.age,
            "tracking": self.tracking
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="", tracking=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(tracking) > 0:
            self.tracking = tracking #
        db.session.commit()
        return self
    

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=date(1847, 2, 11), tracking='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }' )
        u2 = User(name='Nicholas Tesla', uid='niko', password='123niko', dob=date(1856, 7, 10), tracking='{"userName":"Nicholas Tesla","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }')
        u3 = User(name='Alexander Graham Bell', uid='lex', dob=date(1856, 7, 10), tracking='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }')
        u4 = User(name='Grace Hopper', uid='hop', password='123hop', dob=date(1906, 12, 9), tracking='{"userName":"Thomas Edison","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }')
        u5 = User(name='Eun Lim', uid='lim', password='123lim', dob=date(2007, 12, 9), tracking='{"userName":"Eun Lim","instrumentName": "Piano", "practiceDate": "21-Oct-2023", "practiceTime": "30" }') #testing create method
        users = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                    #user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            