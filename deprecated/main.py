from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Serve HTML pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu.html")
def menu():
    return render_template("menu.html")

@app.route("/season.html")
def season():
    return render_template("season.html")

@app.route("/dish.html")
def dish():
    return render_template("dish.html")

# Serve static files (JS, CSV, CSS, images)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
