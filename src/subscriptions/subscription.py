import os 
from flask import Blueprint, render_template, g, request, redirect, session
from sqlalchemy import * 

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

subscription_bp = Blueprint(
  'subscription_bp', 
  __name__,
  template_folder=template_dir, 
  url_prefix='/subscription'
)

@subscription_bp.route('/')
def index():
  cursor = g.conn.execute(text(
    """
    SELECT * FROM Subscriptions
    """
  ))

  query_res = cursor.fetchall()

  return render_template('subscriptions/index.html', subscriptions=query_res)

@subscription_bp.route('/purchase', methods=['POST'])
def update_subscription():
  pass 
