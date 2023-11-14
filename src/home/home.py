from flask import Blueprint, render_template, g
from sqlalchemy import * 

home_bp = Blueprint(
  'home_bp', 
  __name__,
  template_folder='templates'
)

@home_bp.route('/')
def index():
  return "HELLO MAIN HOME PAGE"