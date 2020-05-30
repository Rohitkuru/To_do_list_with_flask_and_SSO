import csv
import random
from models import *
from datetime import datetime



due_date = ['2020-05-30','2020-05-31','2020-06-01','2020-06-02','2020-06-03','2020-06-04','2020-06-05','2020-06-06','2020-06-07','2020-06-08']
labels = ['Others','Shopping','Family','Personal','Work']
status = ['InProgress','Complete','OnHold','New']

for r in range(0,100):
    f = open("list_chores", "r")
    data = csv.reader(f)
    for x in data:
        record = Todolist(task=x[0],description=x[0]+ " Add some description",label=random.choice(labels),status=random.choice(status),due_date=datetime.strptime(random.choice(due_date),'%Y-%m-%d').date(),start_date=datetime.now().date(),user_id=1)
        db.session.add(record)
        db.session.commit()
        print("Record added successfully")
