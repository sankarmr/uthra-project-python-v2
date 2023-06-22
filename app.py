from flask import Flask, render_template

app = Flask(__name__)

JOBS = [{
  'id': 1,
  'title': 'Data Analyst',
  'location': 'Dubai',
  'salary': 'Dhs 100,000'
}, {
  'id': 2,
  'title': 'Data Scientist',
  'location': 'Trivandrum',
  'salary': 'Rs. 150,000'
}, {
  'id': 3,
  'title': 'Soft Engineer',
  'location': 'Bengaluru, India',
  'salary': 'Rs. 110,000'
}, {
  'id': 4,
  'title': 'Graphics Designer',
  'location': 'New York, United States',
  'salary': '$90,000'
}]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name="Uthra's")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
