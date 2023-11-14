import os 
from flask import Flask, request, render_template, Response, abort, g 
from sqlalchemy import * 

from src.home.home import home_bp
from src.customers.customers import customer_bp
from src.authors.authors import author_bp
from src.employees.employees import employee_bp
from src.books.books import book_bp

from config import (
  DATABASEURI, 
  DEVLOPMENT_ENV, 
  HOST, 
  THREADED
)

# template_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__, template_folder=template_directory)

app = Flask(__name__)

# Database Connection
engine = create_engine(DATABASEURI)
connection = engine.connect()

# Example - 


# Database connection on webpage request
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def home():
  print(request.args)


  # Example query 
  cursor = g.conn.execute(text("""
    SELECT * 
    FROM customers;
  """)) 

  for result in cursor:
    print(result)
  
  return "HELLO MAIN PAGE"

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(author_bp, url_prefix='/author')
app.register_blueprint(book_bp, url_prefix='/book')


if __name__=="__main__":
  app.run(debug=DEVLOPMENT_ENV) 