from Genius import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Candidates.query.get(int(user_id))

class Candidates(db.Model,UserMixin):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer,primary_key = True)
    cname = db.Column(db.String(5),nullable = False)
    ename = db.Column(db.String(100),nullable = False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    student_id = db.Column(db.Integer, nullable = False)
    correctnum = db.relationship('CorrectNum',backref='correctnumber', lazy = True)

    def __repr__(self):
        return 'User({},{},{},{})'.format(self.Cname,self.Ename,self.School_id,self.Student_id)

class Schools(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String,nullable=False)
    school_name = db.relationship('Candidates',backref='school_name',lazy = True)

    def __repr__(self):
        return '{}'.format(self.school)

class CorrectNum(db.Model):
    __tablename__ = 'correctnum'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    def __repr__(self):
        return '{}'.format(self.number)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.Text,nullable=False)
    answer = db.Column(db.Text,nullable=False)
    wrong_answer1 = db.Column(db.Text,nullable=False)
    wrong_answer2 = db.Column(db.Text,nullable=False)
    wrong_answer3 = db.Column(db.Text,nullable=False)
