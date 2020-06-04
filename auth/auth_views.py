from flask import Blueprint,redirect,url_for,session,render_template
from flask_dance.contrib.github import github
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint("auth",__name__)

from models import *



@auth.route("/")
def home():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info_json = ""
        account_info = github.get("/user")
    if account_info.ok:
        account_info_json = account_info.json()
        user =  User.query.filter_by(user_name=account_info_json['login']).first()
        if user:
            login_user(user)
        else:
            create_user = User(user_name=account_info_json['login'],is_active=True)
            db.session.add(create_user)
            db.session.commit()
            login_user(create_user)

    return redirect(url_for('operation.user_home'))

@auth.route("/admin_view")
def admin_view():
    if current_user.user_name == "Rohitkuru":
        data = {}
        for x in User.query.all():
            data[x.user_name] = []
            for y in Todolist.query.all():
                if x.id == y.user_id:
                    data[x.user_name].append((y.task,y.label,y.status))

        return render_template("admin_view.html",users_data=User.query.all(),pending = Todolist.query.filter_by("status" != "Complete").all(),
                               complete = Todolist.query.filter_by("status" == "Complete").all(),
                               login_information=current_user.user_name,tasks_data=Todolist.query.all(),data=data)
    else:
        return render_template("admin_access_denied.html",login_information=current_user.user_name)




@auth.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect("https://github.com")
