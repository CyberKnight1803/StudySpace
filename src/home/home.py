from flask import Blueprint, render_template, g, session, redirect
from sqlalchemy import * 

home_bp = Blueprint(
  'home_bp', 
  __name__,
  template_folder='templates'
)

@home_bp.route('/')
def index():

  if 'current_user_id' in session:
    return redirect(f"/{session['user_type']}")

  cursor = g.conn.execute(text(
    """
    SELECT * FROM Subscriptions
    """
  ))
  g.conn.commit()
  subscription_plans = cursor.mappings().all()
  print(subscription_plans)
  return render_template('home.html', subscription_plans=subscription_plans)