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



#Signup, Login, Logout
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
        False
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

@author_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
  if request.method == 'GET':
    incorrect_details = request.args.get('incorrect_details')
    return render_template('reset_password.html', incorrect_details=incorrect_details) 
  
  else:
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
      return redirect(author_bp.url_prefix + '/reset-password' + '?incorrect_details=True')

    try:
      cursor = g.conn.execute(text(
      """
      UPDATE Authors 
      SET password=:password
      WHERE user_id=:user_id;
      """
      ), {'user_id': session['current_user_id'], 'password': password})
    
      g.conn.commit()

    except Exception as e:
      return redirect(author_bp.url_prefix + '/reset-password' + '?incorrect_details=True')

    return redirect(author_bp.url_prefix + '/profile')



#Profile updation
@author_bp.route('/profile', methods=['GET'])
def view_profile():
  if 'current_user_id' not in session or session['user_type'] != 'author':
    return redirect(author_bp.url_prefix + '/login')
  sql_query_params = {
    'user_id': session['current_user_id']}
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
    'email': request.form.get('email')}
  try:
    cursor = g.conn.execute(text("""
      UPDATE authors
      SET mobile=:mobile, email=:email
      WHERE user_id=:user_id
    """), update_profile_details)
    g.conn.commit()
  except Exception as e:
    return redirect(author_bp.url_prefix + '/profile' + '?incorrect_details=True')
  return redirect(author_bp.url_prefix + '/profile') 



#Add a book
@author_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
  query_res = g.conn.execute(text("""
    SELECT *
    FROM Publishers
    """))
  publishers = query_res.fetchall()
  query_res = g.conn.execute(text("""
    SELECT A.user_id
    FROM Authors A
    """))
  all_authors = query_res.scalars().all()
  if request.method == 'GET':
    query_param = request.args.get('incorrect_details')
    return render_template('add_book.html', publishers= publishers, incorrect_details=query_param)
  else:
    new_book = {
      'book_name': request.form.get('book_name'), 
      'edition':  request.form.get('edition'), 
      'pages': request.form.get('pages'), 
      'publication_year': request.form.get('publication_year'),
      'description': request.form.get('description'),
      'language': request.form.get('language'),
      'google_link': request.form.get('google_link'),
      'publisher_id': request.form.get('publisher_id'),
      'authors': request.form.get('authors')
    }
    try:
      query_res = g.conn.execute(text("""
      INSERT INTO books (
        book_name, edition, pages, publication_year, description, language, google_link
      ) VALUES (
        :book_name, 
        :edition, 
        :pages, 
        :publication_year, 
        :description, 
        :language, 
        :google_link
      )
      RETURNING book_id
      """), new_book)
      new_book["book_id"] = query_res.scalar()
      query_res2 = g.conn.execute(text("""
      INSERT INTO Published_by (
        book_id,publisher_id
      ) VALUES (
        :book_id, 
        :publisher_id
      )
      """), new_book)
      authors = new_book["authors"].split(",")
      for author in authors:
        author = author.strip()   #Removing whitespaces
        print(author)
        print(all_authors)
        if author not in all_authors:
          print("The author id does not exist")
          raise Exception('The author id does not exist')
        new_book["secondary_author_id"] = author
        query_res = g.conn.execute(text("""
        INSERT INTO Written_by (
          user_id,book_id
        ) VALUES (
          :secondary_author_id,
          :book_id
        )
        """), new_book)
        g.conn.commit()
    except Exception as e:
      return redirect(author_bp.url_prefix + '/add_book' + '?incorrect_details=True')
    return redirect(author_bp.url_prefix + '/add_book' + '?incorrect_details=False') 




#View all my books
@author_bp.route('/books', methods=['GET']) 
def view_books():
  if 'current_user_id' not in session or session['user_type'] != 'author':
    return redirect(author_bp.url_prefix + '/login')
  cursor = g.conn.execute(text("""
    SELECT *
    FROM Books B
  """))
  query_res = cursor.fetchall()
  if query_res is None:
    return redirect(author_bp.url_prefix)
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
    authors_list = ""
    authors_ids = ""
    for author in query_res:
      authors_list = authors_list + author[1]+" "+author[2] + ", "
      authors_ids = authors_ids + author[0] + ", "
    print(authors_ids)
    authors_list = authors_list[:-2]
    temp_book = list(book)
    if session['current_user_id'] in authors_ids:
      books_and_authors.append(temp_book+[authors_list])
  return render_template('books.html', books=books_and_authors)