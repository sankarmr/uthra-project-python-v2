from sqlalchemy import create_engine, text
import os
from datetime import date

db_connection = os.environ['DB_CONNECT']

engine = create_engine(db_connection,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_from_db():
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "select id, title, location, format(salary,0) as salary, currency from jobs"
      ))
    jobs = []
    for row in result.all():
      jobs.append(row._mapping)
    return jobs


def load_job_details(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "select id, title, location, format(salary,0) as salary, currency, responsibilities, requirements from jobs where id = :id1"
      ), {'id1': id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0]._mapping)


def insert_jobs_db(Dict):
  with engine.connect() as conn:
    
    querytext = text("insert into jobs (title, location, salary, currency, responsibilities, requirements, status, regdate) values (:title, :location, :salary, :currency, :responsibilities, :requirements, :status, :regdate)")
  
    conn.execute(querytext, 
                 {'title': Dict['title_text'], 
                 'location': Dict['location_text'],
                 'salary': Dict['salary_text'],
                 'currency': Dict['currency_text'],
                 'responsibilities': Dict['responsibilities_text'],
                 'requirements': Dict['requirements_text'],
                 'status': 1,
                 'regdate': date.today()}
                )

def insert_job_application(appldtls):
  with engine.connect() as conn:
    querytxt = text("insert into jobs_applied (jobid, title, fullname, email, linkedurl, work_experience, education, resumeurl, status, regdate) values (:jobid, :title, :fullname, :email, :linkedurl, :work_experience, :education, :resumeurl, :status, :regdate)")