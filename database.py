from sqlalchemy import create_engine, text

db_connection = "mysql+pymysql://adir7s1srtejmiv4o2zf:pscale_pw_6RGydXtatyQONeocJNICmTHrbxGMfXMeTkNtVWgbeh6@aws.connect.psdb.cloud:3306/uthrasproject?"

engine = create_engine(db_connection,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

with engine.connect() as conn:
  result = conn.execute(text("select * from jobs"))
  print(result.all())
