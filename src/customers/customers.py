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
    return render_template('customers/signup.html', incorrect_details=query_param)

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

  query_res = cursor.mappings().all()

  if query_res is None: 
    return redirect(customer_bp.url_prefix)

  query_params = request.args.get('incorrect_details')

  customer = dict(query_res[0])
  if customer['address'] is None:
    customer['address'] = ''

  subscription_name = ''
  if customer['subscription_status']:
    cursor = g.conn.execute(text("""
    SELECT S.subscription_name 
    FROM Customers C, Subscriptions S, Subscribe sub
    WHERE C.user_id = :user_id AND C.user_id = sub.user_id AND S.subscription_id = sub.subscription_id
    """), {'user_id': session['current_user_id']}) 

    query_res = cursor.fetchone()

    if query_res is not None:
      subscription_name = query_res[0]
  
  return render_template('customers/profile.html', customer=customer, subscription_name=subscription_name, incorrect_details=query_params)

@customer_bp.route('/profile', methods=['POST'])
def update_profile():
  update_profile_details = {
    'user_id': session['current_user_id'],
    'mobile': request.form.get('mobile'), 
    'address': None if request.form.get('address') == '' else request.form.get('address'),
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

@customer_bp.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
  try:
    cursor = g.conn.execute(text(
      """
      DELETE FROM Subscribe
      WHERE user_id=:user_id
      """
    ), {'user_id': session['current_user_id']})
    g.conn.commit()

    cursor = g.conn.execute(text(
      """
      UPDATE Customers 
      SET subscription_status=FALSE
      WHERE user_id=:user_id;
      """
    ), {'user_id': session['current_user_id']})
    g.conn.commit()

  except Exception as e:
    pass 

  return redirect(customer_bp.url_prefix + '/profile') 



@customer_bp.route('/transaction-history', methods=['GET'])
def view_transaction_history():

  cursor = g.conn.execute(text(
    """
    SELECT pt.transaction_id, s.subscription_name, pt.time_stamp, s.subscription_cost
    FROM paymenttransactions pt, payments p, subscriptions s
    WHERE p.transaction_id = pt.transaction_id AND p.subscription_id = s.subscription_id AND p.user_id = :user_id
    ORDER BY pt.time_stamp DESC;
    """
  ), {'user_id': session['current_user_id']})
  g.conn.commit()

  transactions = cursor.mappings().all()
  
  noTransactions = False 
  if transactions is None:
    noTransactions = True

  return render_template('customers/transactions.html', transactions=transactions, noTransactions=noTransactions) 

@customer_bp.route('/delete-payment-details', methods=['POST'])
def delete_payment_details():
  cursor = g.conn.execute(text(
    """
    UPDATE Customers 
    SET payment_details = NULL 
    WHERE user_id=:user_id
    """
  ), {'user_id': session['current_user_id']})
  g.conn.commit()

  return redirect(customer_bp.url_prefix + '/profile')

@customer_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
  if request.method == 'GET':
    incorrect_details = request.args.get('incorrect_details')
    return render_template('customers/reset_password.html', incorrect_details=incorrect_details) 
  
  else:
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
      return redirect(customer_bp.url_prefix + '/reset-password' + '?incorrect_details=True')

    try:
      cursor = g.conn.execute(text(
      """
      UPDATE Customers 
      SET password=:password
      WHERE user_id=:user_id;
      """
      ), {'user_id': session['current_user_id'], 'password': password})
    
      g.conn.commit()

    except Exception as e:
      return redirect(customer_bp.url_prefix + '/reset-password' + '?incorrect_details=True')

    return redirect(customer_bp.url_prefix + '/profile')