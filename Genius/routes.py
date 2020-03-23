from flask import render_template, url_for, flash, redirect, request
from Genius import app, db
from Genius.form import UpdateAccount,Register, Login, TestZone,Add_Question
from Genius.model import *
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
import random



@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    details = Candidates(cname=form.Cname.data, ename=form.Ename.data, school_id=form.School.data, student_id = form.Student_id.data)
    if form.validate_on_submit():
        if Candidates.query.filter_by(school_id=form.School.data,student_id = form.Student_id.data).first():
            flash('已有此账号','danger')
        else:
            flash('账号名为{}开创成功！'.format(form.Cname.data),'success')
            db.session.add(details)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
            candidate =Candidates.query.filter_by(school_id=form.School.data,student_id = form.Student_id.data).first()
            if candidate:
                login_user(candidate,remember=form.remember.data)
                flash(f'{candidate.cname}登入成功 ','success')
                return redirect(url_for('home'))
            else:
                flash('请检查学号与学校','danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/info')
@login_required
def info():
    return render_template('info.html')


@app.route('/update',methods=['GET','POST'])
@login_required
def update():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.cname = form.Cname.data
        current_user.ename = form.Ename.data
        current_user.school_id = form.School.data
        current_user.student_id = form.Student_id.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return render_template('info.html')
    return render_template('update.html',form=form)


@app.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    return render_template('admin.html')

@app.route('/add_question',methods=['GET','POST'])
@login_required
def add_question():
    form = Add_Question()
    if form.validate_on_submit():
        Q = Questions(question=form.question.data, answer=form.answer.data, wrong_answer1=form.wrong_answer1.data, wrong_answer2=form.wrong_answer2.data, wrong_answer3=form.wrong_answer3.data)
        db.session.add(Q)
        db.session.commit()
        flash('题目成功加入题库了','success')
        return render_template('admin.html')
    return render_template('add_question.html',form=form)

@app.route('/see_candidate',methods=['GET','POST'])
@login_required
def see_candidate():
    c = Candidates.query.all()
    return render_template('see_candidate.html',c=c)

@app.route('/see_question',methods=['GET','POST'])
@login_required
def see_question():
    q = Questions.query.all()
    return render_template('see_question.html',q=q)

@app.route('/update_question',methods=['GET','POST'])
@login_required
def update_question():
    form = Add_Question()
    if form.validate_on_submit():
        q = Questions.query.get(form.id.data)
        q.question = form.question.data
        q.answer = form.answer.data
        q.wrong_answer1 = form.wrong_answer1.data
        q.wrong_answer2 = form.wrong_answer2.data
        q.wrong_answer3 = form.wrong_answer3.data
        db.session.commit()
        flash('更新成功','success')
        return redirect(url_for('see_question'))
    return render_template('update_question.html',form=form)

@app.route('/Code_Zone',methods=['GET','POST'])
@login_required
def Code_Zone():
    form = TestZone()
    if form.validate_on_submit():
        code = form.code.data
        if code == '大家是小天才':
            return redirect(url_for('admin'))
        else:
            flash('代码错误','danger')
    return render_template('Code_Zone.html',form=form)

@app.route('/Test_Zone',methods=['GET','POST'])
@login_required
def Test_Zone():
    form = TestZone()
    if form.validate_on_submit():
        code = form.code.data
        if code == 'ABCDEF':
            return redirect(url_for('test'))
        else:
            flash('代码错误','danger')
    return render_template('Test_Zone.html',form=form)


@app.route('/test',methods=['GET','POST'])
@login_required
def test():
    if CorrectNum.query.filter_by(candidate_id=current_user.id).first():
        flash('不可重复做','danger')
        return redirect(url_for('home'))
    totalNumber = Questions.query.count()
    question_list =[]
    for i in range(1,totalNumber+1):
        q1 = Questions.query.get(i)
        list_1 = [0,q1.question,q1.answer,[q1.answer,q1.wrong_answer1,q1.wrong_answer2,q1.wrong_answer3]]
        list_1[3]= random.sample(list_1[3],4)
        question_list.append(list_1)
    question_list = random.sample(question_list,2)
    for i in range(1,totalNumber+1):
        question_list[i-1][0]=i
    if request.method == 'POST':
        number_correct = 0;
        for i in question_list:
            answer = request.form.get('q'+str(i[0]))
            if answer == i[2]:
                number_correct += 1
        num = CorrectNum(number=number_correct,candidate_id=current_user.id)
        db.session.add(num)
        db.session.commit()
        logout_user()
        return redirect(url_for('login'))
    return render_template('test.html',q=question_list)





if __name__ == '__main__':
    app.run(debug=True)
