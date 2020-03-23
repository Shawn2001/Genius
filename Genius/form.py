from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,NumberRange
from flask_login import current_user



class Register(FlaskForm):

    Cname = StringField('中文姓名 Chinese Name',
                        validators=[DataRequired(),Length(min=2)])
    Ename = StringField('英文姓名 English Name',
                        validators=[DataRequired(),Length(min=5)])
    School = SelectField(u'学校 School',
                        choices=[('1','FY1'),('2','FY2'),('3','FY3'),('4','FY4'),('5','FY5')])
    Student_id = IntegerField('学号 Student ID',
                        validators=[DataRequired(),NumberRange(min=999)])
    submit = SubmitField('注册')


class Login(FlaskForm):
    Student_id = IntegerField('学号 Student ID',
                        validators=[DataRequired(),NumberRange(min=999)])
    School = SelectField(u'学校 School',
                        choices=[('1','FY1'),('2','FY2'),('3','FY3'),('4','FY4'),('5','FY5')])
    remember = BooleanField('记得我哦')
    submit = SubmitField('登录')



class UpdateAccount(FlaskForm):
    Cname = StringField('中文姓名 Chinese Name',
                        validators=[DataRequired(),Length(min=2)])
    Ename = StringField('英文姓名 English Name',
                        validators=[DataRequired(),Length(min=5)])
    School = SelectField(u'学校 School',
                        choices=[('1','FY1'),('2','FY2'),('3','FY3'),('4','FY4'),('5','FY5')])
    Student_id = IntegerField('学号 Student ID',
                        validators=[DataRequired(),NumberRange(min=999)])
    submit = SubmitField('更新')


class TestZone(FlaskForm):
    code = StringField('请输入代码',
                        validators=[DataRequired(),Length(min=6,max=6)])
    submit = SubmitField('进入')

class Add_Question(FlaskForm):
    id = IntegerField('Question_ID',
                        validators=[DataRequired()])
    question = TextAreaField('题目',
                            validators=[DataRequired()])
    answer = TextAreaField('答案',
                            validators=[DataRequired()])
    wrong_answer1 = TextAreaField('错误答案1',
                            validators=[DataRequired()])
    wrong_answer2 = TextAreaField('错误答案2',
                            validators=[DataRequired()])
    wrong_answer3 = TextAreaField('错误答案3',
                            validators=[DataRequired()])
    submit = SubmitField('增添')
