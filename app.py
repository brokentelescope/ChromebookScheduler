from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.column(db.String(200))
#     completed = db.column(db.Integer)
#     date_created = db.Column(db.DateTime, default=datetime.estnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id
    
@app.route('/', methods=['GET', 'POST'])
def login_index():
    if request.method == 'POST':
        # sqlite
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        # html form 
    return render_template('login_index.html')
    



    # return render_template('home_index.html')


# @app.route('/')
# def home_index():
#     return render_template('home_index.html')

@app.route('/date_lookup')
def date_lookup():
    return render_template('date_lookup_index.html')

@app.route('/my_reservations')
def my_reservations():
    return render_template('my_reservations_index.html')

@app.route('/reservation_history')
def reservation_history():
    return render_template('reservation_history_index.html')

# @app.route('/bug_report')
# def bug_report():
#     return render_template('bug_report.html')


if __name__ == '__main__':
    app.run(debug=True)