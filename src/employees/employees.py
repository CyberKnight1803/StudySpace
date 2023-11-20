import uuid
from flask import Blueprint, render_template, g, request, redirect, session
from sqlalchemy import * 

employee_bp = Blueprint(
  'employee_bp', 
  __name__,
  template_folder='templates',
  url_prefix='/employee'
)

@employee_bp.route('/')
def index():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  
  return render_template('employees/index.html')

@employee_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    query_param = request.args.get('incorrect_details')
    return render_template('employees/login.html', incorrect_details=query_param)
  
  else:
    login_data = {
      'employee_email': request.form.get('email'), 
      'employee_password': request.form.get('password')
    }

    cursor = g.conn.execute(text("""
    SELECT * 
    FROM Employees E
    WHERE E.email=:employee_email AND E.password=:employee_password
    """), login_data)

    g.conn.commit()

    query_res = cursor.fetchone()
    cursor.close()
    if query_res is None:
      return redirect(employee_bp.url_prefix + '/login' + '?incorrect_details=True')

    session['current_user_id'] = query_res[0] 
    session['user_type'] = 'employee'

    return redirect(employee_bp.url_prefix)

@employee_bp.route('/logout', methods=['POST'])
def logout():
  session.pop('current_user_id', None)
  session.pop('user_type', None)
  return redirect('/')

@employee_bp.route('/profile', methods=['GET'])
def view_profile():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  
  sql_query_params = {
    'user_id': session['current_user_id']
  } 

  cursor = g.conn.execute(text("""
    SELECT * 
    FROM Employees E 
    WHERE E.user_id=:user_id
  """), sql_query_params)

  query_res = cursor.fetchone()
  cursor.close()

  if query_res is None:
    return redirect(employee_bp.url_prefix)
  
  query_data = []
  for i in range(len(query_res)):
    if query_res[i] is None:
      query_data.append('')
    else:
      query_data.append(query_res[i])
  
  query_params = request.args.get('incorrect_details')
  return render_template('employees/profile.html', employee=query_data, incorrect_details=query_params)

@employee_bp.route('/profile', methods=['POST'])
def update_profile():
  update_profile_details = {
    'user_id': session['current_user_id'],
    'mobile': request.form.get('mobile'), 
    'address': request.form.get('address'),
  }

  try:
    cursor = g.conn.execute(text("""
      UPDATE Employees
      SET mobile=:mobile, address=:address
      WHERE user_id=:user_id
    """), update_profile_details)

    g.conn.commit()

  except Exception as e:
    return redirect(employee_bp.url_prefix + '/profile' + '?incorrect_details=True')

#add publisher, remove customer
#View customers, view authors, view publishers
#Customers



#All the views
@employee_bp.route('/customers', methods=['GET'])
def view_customers():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  cursor = g.conn.execute(text("""
    SELECT * 
    FROM Customers C
  """))
  g.conn.commit()
  query_res = cursor.fetchall()
  cursor.close()
  if query_res is None:
    return redirect(employee_bp.url_prefix)
  return render_template('employees/views/customers.html', customers=query_res)
@employee_bp.route('/publishers', methods=['GET'])
def view_publishers():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  cursor = g.conn.execute(text("""
    SELECT * 
    FROM Publishers P
  """))
  query_res = cursor
  if query_res is None:
    return redirect(employee_bp.url_prefix)
  return render_template('employees/views/publishers.html', publishers=query_res)
@employee_bp.route('/authors', methods=['GET']) 
def view_authors():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  cursor = g.conn.execute(text("""
    SELECT * 
    FROM Authors A
  """))
  query_res = cursor
  if query_res is None:
    return redirect(employee_bp.url_prefix)
  return render_template('employees/views/authors.html', authors=query_res)
@employee_bp.route('/books', methods=['GET']) 
def view_books():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  cursor = g.conn.execute(text("""
    SELECT *
    FROM Books B
  """))
  query_res = cursor.fetchall()
  cursor.close()
  if query_res is None:
    return redirect(employee_bp.url_prefix)
  books = query_res
  books_and_authors = []
  for book in books:
    cursor = g.conn.execute(text("""
    SELECT A.user_id, A.given_name, A.last_name
    FROM Written_by W, Authors A
    WHERE W.book_id =:book_id AND W.user_id = A.user_id
    """), {"book_id":book[0]})
    g.conn.commit()
    query_res = cursor.fetchall()
    cursor.close()
    authors_list = ""
    for author in query_res:
      authors_list = authors_list + author[1]+" "+author[2] + ", "
    authors_list = authors_list[:-2]
    temp_book = list(book)
    books_and_authors.append(temp_book+[authors_list])
  return render_template('employees/views/books.html', books=books_and_authors)
@employee_bp.route('/payments', methods=['GET']) 
def view_payments():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  cursor = g.conn.execute(text("""
    SELECT P.transaction_id, P.user_id, T.time_stamp, S.subscription_name, S.subscription_cost
    FROM Payments P, PaymentTransactions T, Subscriptions S
    WHERE P.transaction_id = T.transaction_id AND P.subscription_id = S.subscription_id
  """))
  g.conn.commit()
  query_res = cursor.fetchall()
  cursor.close()
  if query_res is None:
    return redirect(employee_bp.url_prefix)
  return render_template('employees/views/payments.html', payments=query_res)





#All the edits
@employee_bp.route('/add_publisher', methods=['GET'])
def add_publisher_form():
  return render_template('employees/edits/add_publisher.html')
@employee_bp.route('/add_publisher', methods=['POST'])
def add_publisher_update():
  publisher_details = {
    'publisher_name': request.form.get('publisher_name'),
  }
  cursor = g.conn.execute(text("""
    INSERT INTO Publishers (publisher_name)
    VALUES (:publisher_name);
  """), publisher_details)
  g.conn.commit()
  return redirect(employee_bp.url_prefix + '/') 
@employee_bp.route('/remove/customer', methods=['GET'])
def get_customer():
  return render_template('employees/edits/get_customer.html')
@employee_bp.route('/remove/customer', methods=['POST'])
def remove_customer():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  incorrect_message = "False"
  sql_query_params = {
    'user_id': request.form.get('customer_id')
  } 
  try:
    cursor = g.conn.execute(text("""
      DELETE FROM Customers C 
      WHERE C.user_id=:user_id
    """), sql_query_params)
    g.conn.commit()
    affected_rows = cursor.rowcount
    if affected_rows == 0:
      incorrect_message = "True"
    else:
      incorrect_message = "False"
    cursor.close()
  except Exception as e:
    print("The deletion error is still there")
    pass
  return render_template('employees/edits/get_customer.html', incorrect_details=incorrect_message)
@employee_bp.route('/remove/book', methods=['GET'])
def get_book():
  return render_template('employees/edits/get_book.html')
@employee_bp.route('/remove/book', methods=['POST'])
def remove_book():
  if 'current_user_id' not in session or session['user_type'] != 'employee':
    return redirect(employee_bp.url_prefix + '/login')
  incorrect_message = "False"
  sql_query_params = {
    'book_id': request.form.get('book_id')
  } 
  try:
    cursor = g.conn.execute(text("""
      DELETE FROM Books B 
      WHERE B.book_id=:book_id
    """), sql_query_params)
    g.conn.commit()
    affected_rows = cursor.rowcount
    if affected_rows == 0:
      incorrect_message = "True"
    else:
      incorrect_message = "False"
    cursor.close()
  except Exception as e:
    print("The deletion error is still there")
    pass
  return render_template('employees/edits/get_book.html', incorrect_details=incorrect_message)

@employee_bp.route('/verify/author', methods=['GET'])
def get_profile():
  return render_template('employees/edits/get_author.html')
@employee_bp.route('/verify/author', methods=['POST'])
def verify_profile():
  update_profile_details = {
    'is_verified': True,
    'user_id': request.form.get('author_id')
  }
  cursor = g.conn.execute(text("""
    UPDATE Authors
    SET is_verified=:is_verified
    WHERE user_id=:user_id
  """), update_profile_details)
  g.conn.commit()
  affected_rows = cursor.rowcount
  if affected_rows == 0:
    incorrect_message = "True"
  else:
    incorrect_message = "False"
  cursor.close()
  return render_template('employees/edits/get_author.html', incorrect_details=incorrect_message)