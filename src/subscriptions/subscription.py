import os 
from flask import Blueprint, render_template, g, request, redirect, session
from sqlalchemy import * 
from datetime import datetime, timedelta

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
  g.conn.commit()
  subscriptions = cursor.fetchall()

  cursor = g.conn.execute(text(
    """
    SELECT S.subscription_id 
    FROM Subscriptions S
    WHERE S.subscription_id NOT IN (
        SELECT sub.subscription_id
        FROM Subscribe sub
        WHERE sub.user_id=:user_id
      )
    """
  ), {'user_id': session['current_user_id']})
  g.conn.commit()

  subscription_ids = cursor.fetchall()
  not_subscribed_subscription_ids = []
  for subscription_id in subscription_ids:
    not_subscribed_subscription_ids.append(subscription_id[0])

  return render_template('subscriptions/index.html', subscriptions=subscriptions, not_subscribed_subscription_ids=not_subscribed_subscription_ids)

@subscription_bp.route('/purchase', methods=['POST'])
def update_subscription():
  subscription_id = request.args.get('subscription_id') 
  
  cursor = g.conn.execute(text(
    """
    SELECT C.payment_details 
    FROM Customers C 
    WHERE C.user_id=:user_id
    """
  ), {'user_id': session['current_user_id']})

  g.conn.commit()

  payment_details = cursor.fetchone()
  print(payment_details)

  if payment_details[0] is None:
    return redirect(subscription_bp.url_prefix + '/payment-details' + f'?subscription_id={subscription_id}')
  
  else:
    try:
      cursor.g.conn.execute(text(
        """
        DELETE FROM Subscribe 
        WHERE user_id=:user_id
        """
      ), {'user_id': session['current_user_id']})
      g.conn.commit()

      current_timestamp = datetime.now()
      start_date = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
      end_date = (current_timestamp + timedelta(days=366)).strftime("%Y-%m-%d %H:%M:%S")

      cursor = g.conn.execute(text(
      """
      INSERT INTO Subscribe (user_id, subscription_id, start_date, end_date)
      VALUES (:user_id, :subscription_id, :start_date, :end_date);         
      """), {'user_id': session['current_user_id'], 'subscription_id': subscription_id, 'start_date': start_date, 'end_date': end_date})
      g.conn.commit()

      # Update PaymentTransactions Table
      cursor = g.conn.execute(text(
        """
        INSERT INTO PaymentTransactions (time_stamp)
        VALUES(:date)
        RETURNING transaction_id;
        """
      ), {'date': start_date})
      g.conn.commit()
      transaction_id = cursor.scalar()

      # Update Payments Table
      cursor = g.conn.execute(text(
        """
        INSERT INTO Payments (user_id, transaction_id, subscription_id)
        VALUES (:user_id, :transaction_id, :subscription_id);
        """
      ), {'user_id': session['current_user_id'], 'transaction_id': transaction_id, 'subscription_id': subscription_id})
      g.conn.commit()
    
    except Exception as e:
      return redirect('/customer/profile')


    return redirect('/customer/profile')

@subscription_bp.route('/payment-details', methods=['GET', 'POST'])
def subscription_payment_details():
  if request.method == 'GET':
    subscription_id = request.args.get('subscription_id')
    return render_template('subscriptions/payment.html', subscription_id=subscription_id)

  else:
    payment_details = request.form.get('payment_details')
    subscription_id = request.form.get('subscription_id')
    print(payment_details, subscription_id)

    # try:
    current_timestamp = datetime.now()
    start_date = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    end_date = (current_timestamp + timedelta(days=366)).strftime("%Y-%m-%d %H:%M:%S")


    # Update Subscribe Table
    cursor = g.conn.execute(text(
    """
    INSERT INTO Subscribe (user_id, subscription_id, start_date, end_date)
    VALUES (:user_id, :subscription_id, :start_date, :end_date);         
    """), {'user_id': session['current_user_id'], 'subscription_id': subscription_id, 'start_date': start_date, 'end_date': end_date})
    g.conn.commit()

    # Update PaymentTransactions Table
    cursor = g.conn.execute(text(
      """
      INSERT INTO PaymentTransactions (time_stamp)
      VALUES(:date)
      RETURNING transaction_id;
      """
    ), {'date': start_date})
    g.conn.commit()
    transaction_id = cursor.scalar()

    # Update Payments Table
    cursor = g.conn.execute(text(
      """
      INSERT INTO Payments (user_id, transaction_id, subscription_id)
      VALUES (:user_id, :transaction_id, :subscription_id);
      """
    ), {'user_id': session['current_user_id'], 'transaction_id': transaction_id, 'subscription_id': subscription_id})
    g.conn.commit()

    # Update Customer Table
    cursor = g.conn.execute(text(
      """
      UPDATE Customers 
      SET payment_details=:payment_details, subscription_status=TRUE
      WHERE user_id=:user_id; 
      """), {'user_id': session['current_user_id'], 'payment_details': payment_details})
    g.conn.commit()
    
    # except Exception as e:
      # return redirect('/customer/profile')
    
    return redirect('/customer/profile')