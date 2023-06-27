from sqlalchemy import create_engine, text
import os

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
