import uuid
from flask import Blueprint, render_template, g, request, redirect, session
from sqlalchemy import * 

customer_bp = Blueprint(
  'customer_bp', 
  __name__,
  template_folder='templates', 
  url_prefix='/customer'
)

@customer_bp.route('/')
def index():
  if 'current_user_id' not in session or session['user_type'] != 'customer':
    return redirect(customer_bp.url_prefix + '/login')
  
  return render_template('customers/index.html')

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    query_param = request.args.get('incorrect_details')
    return render_template('customers/login.html', incorrect_details=query_param)

  else:
    login_data = {
      'customer_email': request.form.get("email"), 
      'customer_password': request.form.get("password"),
    }

    cursor = g.conn.execute(text("""  
    SELECT * 
    FROM Customers C
    WHERE C.email=:customer_email AND C.password=:customer_password
    """), login_data)

    g.conn.commit()

    query_res = cursor.fetchone()

    if query_res is None: 
      return redirect(customer_bp.url_prefix + '/login' + '?incorrect_details=True')


    session['current_user_id'] = query_res[0]
    session['user_type'] = 'customer'

    return redirect(customer_bp.url_prefix) 
  

@customer_bp.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    query_param = request.args.get('incorrect_details')
    return render_template('signup.html', incorrect_details=query_param)

  else:
    new_customer = {
      'user_id': str(uuid.uuid4().hex), 
      'given_name': request.form.get('givenName'), 
      'last_name':  request.form.get('lastName'), 
      'mobile': request.form.get('mobile'), 
      'address': request.form.get('address'),
      'email': request.form.get('email'),
      'password': request.form.get('password')
    }

    if new_customer['mobile'] == '':
      new_customer['mobile'] = None
    
    elif len(new_customer['mobile']) != 10:
      return redirect(customer_bp.url_prefix + '/signup' + '?incorrect_details=True')

    print(new_customer)

    try:
      query_res = g.conn.execute(text("""
      INSERT INTO customers (
        user_id, given_name, last_name, mobile, email, password, address
      ) VALUES (
        :user_id, 
        :given_name, 
        :last_name, 
        :mobile, 
        :email, 
        :password, 
        :address
      )
      """), new_customer)
      g.conn.commit()

    except Exception as e:
      return redirect(customer_bp.url_prefix + '/signup' + '?incorrect_details=True')

    return redirect(customer_bp.url_prefix + '/login') 
  
@customer_bp.route('/logout', methods=['POST'])
def logout():
  session.pop('current_user_id', None)
  session.pop('user_type', None)
  return redirect('/')

@customer_bp.route('/profile', methods=['GET'])
def view_profile():
  if 'current_user_id' not in session or session['user_type'] != 'customer':
    return redirect(customer_bp.url_prefix + '/login')
  
  sql_query_params = {
    'user_id': session['current_user_id']
  }

  cursor = g.conn.execute(text("""SELECT * FROM Customers C WHERE C.user_id=:user_id"""), sql_query_params)
  g.conn.commit()

  query_res = cursor.fetchone()

  if query_res is None: 
    return redirect(customer_bp.url_prefix)

  query_params = request.args.get('incorrect_details')
  return render_template('customers/profile.html', customer=query_res, incorrect_details=query_params)

@customer_bp.route('/profile', methods=['POST'])
def update_profile():
  update_profile_details = {
    'user_id': session['current_user_id'],
    'mobile': request.form.get('mobile'), 
    'address': request.form.get('address'),
    'email': request.form.get('email'),
  }

  try:
    cursor = g.conn.execute(text("""
      UPDATE Customers
      SET mobile=:mobile, email=:email, address=:address
      WHERE user_id=:user_id
    """), update_profile_details)

    g.conn.commit()

  except Exception as e:
    return redirect(customer_bp.url_prefix + '/profile' + '?incorrect_details=True')

  return redirect(customer_bp.url_prefix + '/profile') 
