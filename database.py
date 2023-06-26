from sqlalchemy import create_engine, text
import os

print(type(os.environ['DB_CONNECT']))

db_connection = os.environ['DB_CONNECT']

engine = create_engine(db_connection,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(row._mapping)
    return jobs

  #result_all = result.all()
  #print(type(result))
  #print("type of result_all: ", type(result_all))
  #print(result_all[0])
  #first_result = result_all[0]._mapping
  #print("type of frist result: ", type(first_result))
  #print(first_result)
