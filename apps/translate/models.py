from apps import db

class Reviews(db.Model):

    __tablename__ = 'Reviews'

    id = db.Column(db.Integer, primary_key=True)
    sl = db.Column(db.String)
    tl = db.Column(db.String)
    text = db.Column(db.String)
    translation = db.Column(db.String)
    reviewed = db.Column(db.String)
    reviewed_at = db.Column(db.DateTime)

    def __init__(self, sl, tl, text, translation, reviewed, reviewed_at):
        self.sl = sl
        self.tl = tl
        self.text = text
        self.translation = translation
        self.reviewed = reviewed
        self.reviewed_at = reviewed_at