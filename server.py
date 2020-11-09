from flask import Flask, render_template

app = Flask(__name__, static_folder='assets')

@app.route('/')
def home() -> 'html':
    #TODO calculate average check on mocked data
    avg_check = 100
    return render_template('index.html', avg_check=avg_check)

if __name__ == "__main__":
    app.run(debug=True)