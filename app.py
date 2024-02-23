from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home_index.html')

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