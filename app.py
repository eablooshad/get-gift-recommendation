from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # We’ll create this template next

if __name__ == '__main__':
    app.run(debug=True)
