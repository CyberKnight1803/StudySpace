from flask import Blueprint, render_template, g
from sqlalchemy import * 

customer_bp = Blueprint(
  'customer_bp', 
  __name__,
  template_folder='templates'
)

@customer_bp.route('/')
def index():
  # Example query 
  cursor = g.conn.execute(text("""
    SELECT * 
    FROM customers;
  """)) 

  for result in cursor:
    print(result)

  return "HELLO"