import uuid
from flask import Blueprint, render_template, g, request, redirect, session
from sqlalchemy import * 

author_bp = Blueprint(
  'author_bp', 
  __name__,
  template_folder='templates', 
  url_prefix='/author'
)








@author_bp.route('/')
def index():
  if 'current_user_id' not in session or session['user_type'] != 'author':
    return redirect(author_bp.url_prefix + '/login')
  
  return render_template('index.html')

@author_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    query_param = request.args.get('incorrect_details')
    return render_template('login.html', incorrect_details=query_param)

  else:
    login_data = {
      'author_email': request.form.get("email"), 
      'author_password': request.form.get("password"),
    }

    cursor = g.conn.execute(text("""  
    SELECT * 
    FROM authors A
    WHERE A.email=:author_email AND A.password=:author_password
    """), login_data)

    g.conn.commit()

    query_res = cursor.fetchone()

    if query_res is None: 
      return redirect(author_bp.url_prefix + '/login' + '?incorrect_details=True')


    session['current_user_id'] = query_res[0]
    session['user_type'] = 'author'

    return redirect(author_bp.url_prefix) 
  

@author_bp.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    query_param = request.args.get('incorrect_details')
    return render_template('signup.html', incorrect_details=query_param)

  else:
    new_author = {
      'user_id': str(uuid.uuid4().hex), 
      'given_name': request.form.get('givenName'), 
      'last_name':  request.form.get('lastName'), 
      'mobile': request.form.get('mobile'), 
      'is_verified': request.form.get('is_verified'),
      'email': request.form.get('email'),
      'password': request.form.get('password')
    }

    if new_author['mobile'] == '':
      new_author['mobile'] = None
    
    elif len(new_author['mobile']) != 10:
      return redirect(author_bp.url_prefix + '/signup' + '?incorrect_details=True')

    try:
      query_res = g.conn.execute(text("""
      INSERT INTO authors (
        user_id, given_name, last_name, mobile, email, password, is_verified
      ) VALUES (
        :user_id, 
        :given_name, 
        :last_name, 
        :mobile, 
        :email, 
        :password, 
        :is_verified
      )
      """), new_author)
      g.conn.commit()

    except Exception as e:
      return redirect(author_bp.url_prefix + '/signup' + '?incorrect_details=True')

    return redirect(author_bp.url_prefix + '/login') 
  
@author_bp.route('/logout', methods=['POST'])
def logout():
  session.pop('current_user_id', None)
  session.pop('user_type', None)
  return redirect('/')

@author_bp.route('/profile', methods=['GET'])
def view_profile():
  if 'current_user_id' not in session or session['user_type'] != 'author':
    return redirect(author_bp.url_prefix + '/login')
  
  sql_query_params = {
    'user_id': session['current_user_id']
  }

  cursor = g.conn.execute(text("""SELECT * FROM authors C WHERE C.user_id=:user_id"""), sql_query_params)
  g.conn.commit()

  query_res = cursor.fetchone()

  if query_res is None: 
    return redirect(author_bp.url_prefix)

  query_params = request.args.get('incorrect_details')

  query_data = []
  for i in range(len(query_res)):
    if query_res[i] is None:
      query_data.append('')
    else:
      query_data.append(query_res[i])
    
  return render_template('profile.html', author=query_data, incorrect_details=query_params)

@author_bp.route('/profile', methods=['POST'])
def update_profile():
  update_profile_details = {
    'user_id': session['current_user_id'],
    'mobile': request.form.get('mobile'), 
    'is_verified': None if request.form.get('is_verified') is 'None' else request.form.get('is_verified'),
    'email': request.form.get('email'),
  }

  try:
    cursor = g.conn.execute(text("""
      UPDATE authors
      SET mobile=:mobile, email=:email, is_verified=:is_verified
      WHERE user_id=:user_id
    """), update_profile_details)

    g.conn.commit()

  except Exception as e:
    return redirect(author_bp.url_prefix + '/profile' + '?incorrect_details=True')

  return redirect(author_bp.url_prefix + '/profile') 
