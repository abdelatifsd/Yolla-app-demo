from flask import Flask, render_template
import os

app = Flask(__name__)

IMG_FOLDER = os.path.join('static')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route('/')
@app.route('/main')
def main_page():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'yolla_logo.png')
    return render_template("main_page.html", user_image = full_filename)


if __name__ == "__main__": app.run(debug=True)
