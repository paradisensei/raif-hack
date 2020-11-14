from flask import Flask, render_template, redirect, url_for
import json
import util
from backend import metric_buttons

app = Flask(__name__, static_folder='assets')

@app.route('/')
def get_login() -> 'html':
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    # todo simple auth? search by company name
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard() -> 'html':
    avg_bill = metric_buttons.button_AverageBill()
    gender = metric_buttons.button_Gender()
    client_avg_bill = metric_buttons.button_ClientAverageBill()

    return render_template(
        'index.html',
        avg_bill=avg_bill,
        gender=util.gender_graph(gender),
        client_avg_bill=util.avg_bill_graph(client_avg_bill)
    )

if __name__ == "__main__":
    app.run(debug=True)