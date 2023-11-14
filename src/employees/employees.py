from flask import Blueprint, render_template, g
from sqlalchemy import * 

employee_bp = Blueprint(
  'employee_bp', 
  __name__,
  template_folder='templates'
)

@employee_bp.route('/')
def index():
  return "HELLO EMPLOYEE HOME PAGE"