from flask import Flask, render_template, redirect, url_for, request
from GARCH_Stock_Modeling import garch_model

app = Flask(__name__)

@app.route('/')
def index():
    garch_model()
    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    # return render_template("request.html")
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        user = request.args.get('nm')

    return render_template("login.html")

# @app.route('/<comp>')
# def company(comp):
#     return f"<h1> {comp} </h1"

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, threaded = False) - Alternative way of running app
    