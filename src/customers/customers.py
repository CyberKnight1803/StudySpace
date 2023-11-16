import uuid
from flask import Blueprint, render_template, g, request, redirect
from sqlalchemy import * 

customer_bp = Blueprint(
  'customer_bp', 
  __name__,
  template_folder='templates', 
  url_prefix='/customer'
)

@customer_bp.route('/')
def index():
  # Example query 
  cursor = g.conn.execute(text("""
    SELECT * 
    FROM customers;
  """)) 
  g.conn.commit()

  for result in cursor:
    print(result, type(result))
  
  cursor.close()

  return "HELLO"

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

  else:
    login_data = {
      'customer_email': request.form.get("email"), 
      'customer_password': request.form.get("password"),
    }

    # customer_email =  request.form.get("email")
    # customer_password = request.form.get("password")

    print(login_data)

    cursor = g.conn.execute(text("""  
    SELECT * 
    FROM Customers C
    WHERE C.email=:customer_email AND C.password=:customer_password
    """), login_data)

    g.conn.commit()

    

    return redirect(customer_bp.url_prefix) 
  

@customer_bp.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')

  else:
    new_customer = {
      'user_id': str(uuid.uuid4().hex), 
      'given_name': request.form.get('givenName'), 
      'last_name':  request.form.get('lastName'), 
      'mobile': request.form.get('mobile'), 
      'email': request.form.get('email'),
      'password': request.form.get('password')
    }

    # user_id = str(uuid.uuid4().hex)
    # given_name = request.form.get('givenName')
    # last_name = request.form.get('lastName')
    # mobile = request.form.get('mobile')
    # email = request.form.get('email')
    # password = request.form.get('password')

    query_res = g.conn.execute(text("""
    INSERT INTO customers (
      user_id, given_name, last_name, mobile, email, password 
    ) VALUES (
      :user_id, 
      :given_name, 
      :last_name, 
      :mobile, 
      :email, 
      :password
    )
    """), new_customer)

    g.conn.commit()
    return redirect(customer_bp.url_prefix + '/login') 