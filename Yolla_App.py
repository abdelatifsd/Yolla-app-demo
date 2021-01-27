from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

import os

app = Flask(__name__)

IMG_FOLDER = os.path.join('static')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route('/')
@app.route('/main')
def main_page():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'yolla_logo.png')
    return render_template("main_page.html", prediction ="" , user_image = full_filename)


@app.route('/', methods=['POST'])
def input_parameters():
    with open("demand-forecasting-model.pkl", 'rb') as file:
         prediction_model = pickle.load(file)  
    item_id = request.form['itemid']
    store_id = request.form['storeid']
    model_input = transform_user_input(int(store_id), int(item_id))
    prediction = [(prediction_model.predict(model_input)[0])]
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'yolla_logo.png')
    return render_template("main_page.html", prediction=prediction, user_image = full_filename)

def transform_user_input(store, item):
  model_input = pd.DataFrame({"store":store,"item":item}, index=[0])
  return model_input


if __name__ == "__main__":
     with open("demand-forecasting-model.pkl", 'rb') as file:
         prediction_model = pickle.load(file)
     app.run(debug=True)
