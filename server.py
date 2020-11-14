from flask import Flask, render_template, redirect, url_for, request
import json
import util
from backend import metric_buttons

app = Flask(__name__, static_folder='assets')

@app.route('/')
def get_login() -> 'html':
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    # get merchant name and pass it to dashboard
    return redirect(url_for('dashboard', merchant=request.form['merchant']))

@app.route('/dashboard')
def dashboard() -> 'html':
    # get merchant from param
    merchant = request.args['merchant']

    # single-valued metrics
    avg_bill = round(metric_buttons.button_AverageBill())
    ltv = metric_buttons.button_LTV()

    # doughnut-graph metrics
    gender = metric_buttons.button_Gender()
    age = metric_buttons.button_Age()

    # value-graph metrics
    client_avg_bill = metric_buttons.button_ClientAverageBill()
    client_avg_tx = metric_buttons.button_AverageTransactionNumber()

    # rating-graph metrics
    income_in_segment = metric_buttons.button_IncomeInSegmentRate(merchant)[1:]
    # clients_in_segment = metric_buttons.button_ClientNumberInSegmentRate(merchant)

    return render_template(
        'index.html',
        merchant=merchant,
        avg_ltv = util.avg_ltv(ltv),
        avg_bill=avg_bill,
        gender=util.gender_graph(gender),
        age=util.age_graph(age),
        client_avg_bill=util.avg_bill_graph(client_avg_bill),
        client_avg_tx=util.avg_tx_graph(client_avg_tx),
        income_in_segment=util.income_in_segment(income_in_segment),
    )

if __name__ == "__main__":
    app.run(debug=True)