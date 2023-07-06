from flask import Flask, render_template, request, jsonify
from database import load_from_db, load_job_details, insert_jobs_db
from datetime import date

app = Flask(__name__)


@app.route("/")
def list_jobs():
  jobs = load_from_db()
  return render_template('home.html', jobs=jobs, company_name="Uthra's")


@app.route("/job/<id>")
def job_details(id):
  jobs = load_job_details(id)

  if not jobs:
    return "Page not found", 404
  else:
    return render_template('jobdetails.html', jobs=jobs, id=id)


@app.route("/contactus")
def contact_us():
  return render_template('contactus.html')


@app.route("/admin", methods=["GET", "POST"])
def admin():
  if request.method == "POST":
    Dict = request.form
    insert_jobs_db(Dict)

    return render_template('admin.html',
                           dicts=Dict['title_text'],
                           date=date.today())
  else:
    return render_template('admin.html')


@app.route("/job/<id>", methods=["GET", "POST"])
def job_application(id):
  if request.method == "POST":
    jobs = load_job_details(id)
    appldetails = request.form

    return render_template("jobdetails.html", jobs=jobs)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
