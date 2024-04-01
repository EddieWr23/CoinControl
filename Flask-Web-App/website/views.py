from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Income, Expense
from . import db
from sqlalchemy.sql import func
import json
from datetime import datetime as dt, timedelta
import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        form_name = request.form.get('form-name')
        if form_name == 'add-income':
            income = request.form.get('income')#Gets the income from the HTML
            amount = round(float(request.form.get('amount')), 2)#Gets the amount from the HTML

            if income and amount: #Checks if the income and amount are not empty
                new_income = Income(name=income, value=amount, user_id=current_user.id)  #providing the schema for the note 
                db.session.add(new_income) #adding the note to the database 
                db.session.commit()
                flash('Income added!', category='success')
            else:
                flash('Invalid Income!', category='error')

        elif form_name == 'add-expense':
            expense = request.form.get('expense')
            amount = round(float(request.form.get('amount')), 2)

            if expense and amount:
                new_expense = Expense(name=expense, value=amount, user_id=current_user.id)
                db.session.add(new_expense)
                db.session.commit()
                flash('Expense added!', category='success')
            else:
                flash('Invalid Expense!', category='error')

        elif form_name == 'update-balance':
            new_balance = request.form.get('balance')
            if new_balance:
                new_balance = round(float(new_balance), 2)
                current_user.balance = new_balance
                db.session.commit()
                flash('Balance updated!', category='success')
            else:
                flash('Invalid Balance!', category='error')
        
        # After processing the form, redirect to the home page 
        return redirect(url_for('views.home'))
    


    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    total_income = db.session.query(func.sum(Income.value)).filter_by(user_id=current_user.id).scalar() or 0
    total_expense = db.session.query(func.sum(Expense.value)).filter_by(user_id=current_user.id).scalar() or 0
    difference = total_income - total_expense

    current_balance = current_user.balance
    week_count = 25
    weeks = list(range(1, week_count+1))
    balances = [current_balance]
    for week in weeks:
        balances.append(week * difference + current_balance)

    today = dt.today() # Gets the current date
    dates = [today + timedelta(weeks=i) for i in range(week_count + 1)] # Creates a list of dates
    dates = [date.strftime("%d %b") for date in dates] #Formats the date to day month

    return render_template("home.html", user=current_user, incomes=incomes, expenses=expenses, total_income=total_income, total_expense=total_expense, difference=difference, balances=balances, dates=dates)


@views.route('/delete-income', methods=['POST'])
@login_required
def delete_income():
    income_id = request.form.get('income_id')
    income = Income.query.get(income_id)
    if income:
        if income.user_id == current_user.id:
            db.session.delete(income)
            db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/delete-expense', methods=['POST'])
@login_required
def delete_expense():
    expense_id = request.form.get('expense_id')
    expense = Expense.query.get(expense_id)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()
    return redirect(url_for('views.home'))
