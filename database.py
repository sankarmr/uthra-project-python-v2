from datetime import date
import bcrypt
from db_conn import engine, text, Session, User
from app import request

# db_connection = os.environ['DB_CONNECT']

# engine = create_engine(db_connection,
#                        connect_args={"ssl": {
#                          "ssl_ca": "/etc/ssl/cert.pem"
#                        }})
# class User(db.Model):
#   __tablename__ = 'users'
#   user_id = db.Column(db.Integer, primary_key=True)
#   email = db.Column(db.String(100), unique=True, nullable=False)
#   first_name = db.Column(db.String(40), nullable=False)
#   last_name = db.Column(db.String(40), nullable=False)
#   phone = db.Column(db.BigInteger, nullable=True)
#   password = db.Column(db.String(100), nullable=False)

session = Session()


def loadAllUsers():
  users = session.query(User).filter_by(email='sankar@sankar.com').first()
  session.close()
  return users


def updatePassword(email, password):
  user = session.query(User).filter_by(email=email).first()

  try:
    if user:
      user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      session.commit()
      session.close()
      return True
    else:
      return False
  except Exception as e:
    session.rollback()
    session.close()
    return e


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


def load_job_title(id):
  with engine.connect() as conn:
    result = conn.execute(
      text("select title, location from jobs where id = :id"), {'id': id})
    if jobdetails := result.first():
      return jobdetails._mapping
    else:
      return "None"


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

    querytext = text(
      "insert into jobs (title, location, salary, currency, responsibilities, requirements, status, regdate) values (:title, :location, :salary, :currency, :responsibilities, :requirements, :status, :regdate)"
    )

    conn.execute(
      querytext, {
        'title': Dict['title_text'],
        'location': Dict['location_text'],
        'salary': Dict['salary_text'],
        'currency': Dict['currency_text'],
        'responsibilities': Dict['responsibilities_text'],
        'requirements': Dict['requirements_text'],
        'status': 1,
        'regdate': date.today()
      })


def check_for_job_applied(jobid, title, email, status):
  with engine.connect() as conn:
    querytext = text(
      'select exists (select jobid, title, email, status from jobs_applied where jobid = :jobid and title = :title and email = :email and status = :status)'
    )

    result = conn.execute(querytext, {
      'jobid': jobid,
      'title': title,
      'email': email,
      'status': status
    }).scalar()

  return result


def insert_job_application(appldtls, jobid, jobs):
  with engine.connect() as conn:
    querytxt = text(
      "insert into jobs_applied (jobid, title, fullname, email, linkedurl, work_experience, education, resumeurl, status, regdate) values (:jobid, :title, :fullname, :email, :linkedurl, :work_experience, :education, :resumeurl, :status, :regdate)"
    )

    conn.execute(
      querytxt, {
        'jobid': jobid,
        'title': jobs,
        'fullname': appldtls['fullname'],
        'email': appldtls['email'],
        'linkedurl': appldtls['linkedin_url'],
        'work_experience': appldtls['experience'],
        'education': appldtls['education'],
        'resumeurl': appldtls['resume_url'],
        'status': 1,
        'regdate': date.today()
      })


def insert_contact_us(contdtls):
  with engine.connect() as conn:
    querytext = text(
      "insert into contact_us (fullname, email, contact_number, queries, status, regdate) values (:fullname, :email, :contact_number, :queries, :status, :regdate)"
    )

    conn.execute(
      querytext, {
        'fullname': contdtls['fullname'],
        'email': contdtls['email'],
        'contact_number': contdtls['contact_number'],
        'queries': contdtls['queries'],
        'status': 1,
        'regdate': date.today()
      })


def registration_info(regInfo):
  with engine.connect() as conn:
    querytext = text(
      "insert into users (email, first_name, last_name, phone, password) values (:email, :first_name, :last_name, :phone, :password)"
    )
    passwordToHash = regInfo['password'].encode('utf-8')
    passwordHashed = bcrypt.hashpw(passwordToHash, bcrypt.gensalt())

    conn.execute(
      querytext, {
        'email': regInfo['emailID'],
        'first_name': regInfo['firstName'],
        'last_name': regInfo['lastName'],
        'phone': regInfo['phoneNo'],
        'password': passwordHashed
      })
