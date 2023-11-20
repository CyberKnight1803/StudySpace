import uuid
from flask import Blueprint, render_template, g, request, redirect, session
from sqlalchemy import * 

book_bp = Blueprint(
  'book_bp', 
  __name__,
  template_folder='templates', 
  url_prefix='/books'
)

@book_bp.route('/')
def index():
  return "HELLO BOOK BP"

# ?bookid=<id>&section_id=<id>&publisher_id=<id>&author_id=<id>
@book_bp.route('/book')
def show_book():
  is_accessible = False
  if 'current_user_id' not in session:
    return redirect(book_bp.url_prefix + '/login')
  our_user_id = session["current_user_id"]
  cursor = g.conn.execute(text("""
    SELECT B.book_name, B.edition, B.pages, B.publication_year, B.description, B.language, B.google_link, A.given_name, A.last_name, P.publisher_name, S.section_name
    FROM Books B
    JOIN Written_by W on W.book_id=B.book_id
    JOIN Authors A on A.user_id=W.user_id
    JOIN Published_by Pb on Pb.book_id=W.book_id
    JOIN Publishers P on P.publisher_id=Pb.publisher_id
    JOIN Classified_by Cb on Cb.book_id=B.book_id
    JOIN Sections S on S.section_id=Cb.section_id
    WHERE B.book_id =:book_id
  """), {"book_id":request.args.get('book_id')})
  query_res = cursor.fetchall()
  cursor.close()
  our_book = query_res
  print(f"This is our book {our_book}")
  our_result = {"book_name": our_book[0][0],"edition": our_book[0][1],"pages": our_book[0][2],"publication_year": our_book[0][3],"description": our_book[0][4],"language": our_book[0][5],"google_link": our_book[0][6],"publisher_name": our_book[0][9]}
  authors = []
  sections = []
  for book in query_res:
    authors.append(book[8] + " "+book[7])
    sections.append(book[10])
  our_result["sections"] = ",".join(list(set(sections)))
  our_result["authors"] = ",".join(list(set(authors)))
  cursor = g.conn.execute(text("""
    SELECT *
    FROM Books B
    JOIN Accessed_by Ab on Ab.book_id=B.book_id
    JOIN Subscribe S on S.subscription_id=Ab.subscription_id
    WHERE B.book_id=:book_id AND S.user_id=:user_id
  """), {"book_id":request.args.get('book_id'), "user_id":our_user_id})
  query_res = cursor.fetchall()
  cursor.close()
  if len(query_res)>=1:
    access_indicator = True
  else:
    access_indicator = False
  return render_template('books/book.html', book=our_result, access_indicator = access_indicator)