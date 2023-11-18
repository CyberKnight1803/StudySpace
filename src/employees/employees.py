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

  if query_res is None:
    return redirect(employee_bp.url_prefix)
  
  query_params = request.args.get('incorrect_details')
  return render_template('employees/profile.html', employee=query_res, incorrect_details=query_params)

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

  return redirect(employee_bp.url_prefix + '/profile') 
