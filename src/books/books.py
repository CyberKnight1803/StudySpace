from flask import Blueprint, render_template, g
from sqlalchemy import * 

book_bp = Blueprint(
  'book_bp', 
  __name__,
  template_folder='templates', 
  url_prefix='/book'
)

@book_bp.route('/')
def index():
  return "HELLO BOOK BP"