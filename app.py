from flask import Flask, render_template, request, flash, redirect, url_for, Response, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import date
from db_conn import User, Session
import bcrypt

app = Flask(__name__)
app.secret_key = 'whatismysecretkey'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

sess = Session()


# Load a user from the database
@login_manager.user_loader
def load_user(user_id):
  return sess.query(User).get(user_id)


@app.route("/")
@app.route("/home")
def list_jobs():
  from database import load_from_db
  jobs = load_from_db()
  return render_template('home.html', jobsHome=jobs, company_name="Uthra's")


# @app.route("/")
# @app.route("/home")
# def list_jobs():
#   page = request.args.get('page', 1, type=int)
#   jobs = db.session.query(Jobs).order_by(Jobs.id.desc()).paginate(
#     page, 5, False)
#   return render_template('home.html', jobsHome=jobs)


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    user = sess.query(User).filter_by(email=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'),
                               user.password.encode('utf-8')):
      login_user(user)
      target_url = session.pop('target_url', None)
      if target_url:
        return redirect(target_url)
      else:
        return redirect(url_for('list_jobs'))
    else:
      flash("Invalid username or password", "danger")

  target_url = request.referrer
  session['target_url'] = target_url
  return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('logout'))


@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
  from database import updatePassword
  try:
    if request.method == "POST":
      email = request.form['email']
      password = request.form['password']

      if email and password:
        try:
          passwordUpdated = updatePassword(email, password)
          if passwordUpdated:
            flash("Password Updated Successfully", 'success')
          else:
            flash("Password Update Failed", 'danger')
        except Exception as e:
          flash(e, 'danger')
      else:
        flash("No such email", 'danger')
  except Exception as e:
    flash(e, 'danger')

  return render_template('forgotpassword.html')


@app.route("/register", methods=["GET", "POST"])
def signup():
  from database import registration_info
  try:
    if request.method == "POST":
      if 'chkTerms' in request.form:
        checkbox_value = request.form['chkTerms']
        if checkbox_value == 'on':
          try:
            reg_details = request.form
            registration_info(reg_details)
            flash("User created successfully", 'success')
          except Exception as err:
            if '1062' in err.args[0]:
              flash("Email ID already exists. Please select a new email ID",
                    'danger')
        else:
          flash("Please tick the terms checkbox", 'danger')
  except Exception as err:
    print(err)

  return render_template('register.html')


@app.route("/applyjob/<id>")
@login_required
def applyjob(id):
  from database import load_job_title
  job_title = load_job_title(id)
  return render_template('applyjob.html', id=id, jobtitle=job_title)


# @app.route("/job/<id>")
# def job_details(id):
#   from database import load_job_details
#   jobdetails = load_job_details(id)

#   if not jobdetails:
#     return "Page not found", 404
#   else:
#     return render_template('jobdetails.html', jobs=jobdetails, id=id)


@app.route("/home/job", methods=["GET", "POST"])
@login_required
def job_details():
  from database import load_job_details
  if request.method == "POST":
    try:
      for id in request.form:
        if id.startswith("job_"):
          job_id = id.split('_')[1]
          if job_id:
            session['job_id'] = job_id
            jobSession = session.get('job_id')
            jobdetails = load_job_details(jobSession)
            return render_template('jobdetails.html',
                                   jobs=jobdetails,
                                   id=jobSession)
          else:
            return "Page not found", 404
    except Exception as e:
      return f"{e}", 404
  elif request.method == "GET":
    jobSession = session.get('job_id')
    jobdetails = load_job_details(jobSession)
    return render_template('jobdetails.html', jobs=jobdetails, id=jobSession)
  else:
    return "Page not found", 404


@app.route("/applyjob/<id>", methods=["GET", "POST"])
def job_application(id):
  from database import load_job_title, insert_job_application, check_for_job_applied
  if request.method == "POST":
    jobs = load_job_title(id)
    if jobs == "None":
      flash("No Job Found", 'danger')
      return render_template("applyjob.html", jobtitle="No Job Found")
    else:
      appldetails = request.form
      condition = check_for_job_applied(id, jobs['title'],
                                        appldetails['email'], 1)

      x = date.today()

      if condition == 0:
        insert_job_application(appldetails, id, jobs['title'])

      return render_template("applyjob.html",
                             jobtitle=jobs,
                             dicts=appldetails['fullname'],
                             date=x.strftime("%B %d, %Y"),
                             valexists=condition)
  elif Response.status_code == 404:
    return render_template("home.html")


@app.route("/contactus", methods=["GET", "POST"])
def contact_us():
  from database import insert_contact_us
  if request.method == "POST":
    formdtls = request.form
    insert_contact_us(formdtls)
    x = date.today()

    return render_template('contactus.html',
                           name=formdtls['fullname'],
                           date=x.strftime("%B %d, %Y"))
  else:
    return render_template('contactus.html')


@app.route("/about")
def about_us():
  return render_template('about.html')


@app.route("/admin", methods=["GET", "POST"])
def admin():
  from database import insert_jobs_db
  if request.method == "POST":
    Dict = request.form
    insert_jobs_db(Dict)

    return render_template('admin.html',
                           dicts=Dict['title_text'],
                           date=date.today())
  else:
    return render_template('admin.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
