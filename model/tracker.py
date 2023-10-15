import os, base64

from __init__ import app, db
from sqlalchemy.exc import IntegrityError # make sure sqlalchemy is installed


class Tracker(db.Model):
    """Specification for Instrument table """
    __tablename__ = 'trackers' #class name singular, table name plural
    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('id'))
    instrument = db.Column(db.String)
    date = db.Column(db.String)
    play_minutes = db.Column(db.Integer)
    
    #object oriented programming. defines init (constructor).
    def __init__(self, id, user_id, date, play_minutes):
            self.id = id
            self.user_id = user_id
            self.date = date
            self.play_minutes = play_minutes
  
    def __repr__(self):
            return "Tracker(" + str(self.id) + "," + self.instrument+ "," + str(self.date) + str(self.play_minutes) + ")"
    
    def create(self):
        try: #try and except to prevent errors
            # creates a Instrument object from Instrument (db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Instrument table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.instrument)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "user_id": self.user_id, 
            "date": self.date,
            "play_minutes": self.play_minutes,
            "instrument": self.instrument,
            "base64": str(file_encode)
        }
