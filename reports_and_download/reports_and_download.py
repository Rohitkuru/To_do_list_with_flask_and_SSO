from flask import render_template,send_file,Blueprint
from datetime import datetime
import csv
from flask_login import login_required,current_user
import os


reports_and_download = Blueprint("reports_and_download",__name__)

from models import *


@reports_and_download.route("/reports")
@login_required
def reports():
    pie_chart_data = {}
    bar_charts_data = {}
    multiple_bar_charts_data = {}
    for x in "InProgress","OnHold","Complete","New":
        count = Todolist.query.filter(db.and_(Todolist.user_id == current_user.id,Todolist.status == x )).all()
        pie_chart_data[x] = len(count)


    for x in "Work","Personal","Family","Shopping","Others":
        count = Todolist.query.filter(db.and_(Todolist.user_id == current_user.id,Todolist.label == x )).all()
        bar_charts_data[x] = len(count)


    for y in "Work","Personal","Family","Shopping","Others":
        incomplete_count = Todolist.query.filter(db.and_(Todolist.label==y,Todolist.status != "Complete",Todolist.user_id == current_user.id)).all()
        complete_count = Todolist.query.filter(db.and_(Todolist.label== y ,Todolist.status == "Complete",Todolist.user_id == current_user.id)).all()
        multiple_bar_charts_data[y] = { "Incomplete": len(incomplete_count),"Complete": len(complete_count) }


    return render_template("reports.html",pie_chart_data=pie_chart_data,bar_charts_data=bar_charts_data,multiple_bar_charts_data=multiple_bar_charts_data,login_information=current_user.user_name)


@reports_and_download.route("/download", methods = ['POST',"GET"])
@login_required
def download_master_file():
    name = current_user.user_name + "-" + datetime.now().strftime('%m-%d-%Y-%H-%M')  + ".csv"
    with open(name, mode='w',newline='') as master_file:
        master_writer = csv.writer(master_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        master_writer.writerow(["Task No","User ID","Task","Description","Label","Status","Start Date","Due Date","Completion Date"])

        for x in Todolist.query.filter_by(user_id=current_user.id).all():
            master_writer.writerow([x.id,x.user_id,x.task,x.description,x.label,x.status,x.start_date,x.due_date,x.complete_date])

    master_file.close()

    return send_file(filename_or_fp=name,as_attachment=True)