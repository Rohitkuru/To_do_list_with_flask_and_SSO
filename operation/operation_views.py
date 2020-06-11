from flask import render_template,request,session,Blueprint
from datetime import datetime


from models import *

operation= Blueprint('operation',__name__)

from flask_login import login_required,current_user




@operation.route("/home/")
@login_required
def user_home():
    all_user_records = Todolist.query.filter_by(user_id=current_user.id).all()
    return render_template("datatables.html",all_records=all_user_records,login_information=current_user.user_name)


@operation.route("/add_new",methods = ['POST','GET'])
@login_required
def add_new():
    if request.method == "POST":
        try:
            due_date_diff = datetime.now()- datetime.strptime(request.form['duedate'],'%Y-%m-%d')
            if due_date_diff.days <= 0:
                record = Todolist(task=request.form['taskname'],description=request.form['taskdescription'],start_date=datetime.now(),label=request.form['label'],status="New",due_date = datetime.strptime(request.form['duedate'],'%Y-%m-%d'),user_id=current_user.id)
                db.session.add(record)
                db.session.commit()
            else:
                return render_template("add_new_task.html",result="duedateerror",login_information=current_user.user_name)
            return render_template("add_new_task.html", result="success",login_information=current_user.user_name)
        except Exception as e:
            print(e)
            return render_template("add_new_task.html",result="fail",login_information=current_user.user_name)
    return render_template("add_new_task.html",login_information=current_user.user_name)


@operation.route("/search_task",methods=['POST','GET'])
@login_required
def search_task():
    all_user_records = Todolist.query.filter_by(user_id=current_user.id).all()
    return render_template("edit_task.html",all_records=all_user_records,search="on",login_information=current_user.user_name)


@operation.route("/edit_task/<task>",methods=['POST','GET'])
@operation.route("/edit_task",methods = ["POST"])
@login_required
def edit_task(task=None):
    if request.method == "POST":
        try:
            record = Todolist.query.filter_by(task=session['record']).first()
            record.description = request.form['taskdescription']
            record.status = request.form['status']
            if request.form['status'] == "Complete":
                record.complete_date = datetime.now()
            db.session.commit()
            return render_template("edit_task.html",edit="on",result="success",record=record,login_information=current_user.user_name)
        except Exception as e:
            db.session.rollback()
            return render_template("edit_task.html",edit="on",result="fail",record=record,login_information=current_user.user_name)

    record = Todolist.query.filter_by(task=task).first()
    if record.user_id == current_user.id:
        if record.status == "Complete":
            return render_template("edit_task.html",status="complete",record=record,login_information=current_user.user_name)
        session['record'] = task
        return render_template("edit_task.html",edit="on",record=record,login_information=current_user.user_name)
    else:
        return "Unauthorized access "