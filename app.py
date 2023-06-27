from flask import Flask, render_template, jsonify
from database import load_from_db, load_job_details

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
    return render_template('jobdetails.html', jobs=jobs)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
