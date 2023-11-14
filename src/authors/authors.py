from flask import Blueprint, render_template, g
from sqlalchemy import * 

author_bp = Blueprint(
  'author_bp', 
  __name__,
  template_folder='templates'
)

@author_bp.route('/')
def index():
  return "HELLO AUTHOR HOME PAGE"