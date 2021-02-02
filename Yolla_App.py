from flask import Flask, render_template, request, jsonify, url_for
from tensorflow import keras
from sklearn import metrics
import pandas as pd
import numpy as np
import pickle
import math

import os

app = Flask(__name__)

IMG_FOLDER = os.path.join('static')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'yolla_logo.png')

@app.route('/')
@app.route('/main')
def main_page():
    return render_template("main_page.html", prediction ="" , user_image = full_filename)


@app.route('/', methods=['POST'])
def input_parameters():
    with open("demand-forecasting-model.pkl", 'rb') as file:
         prediction_model = pickle.load(file)
    item_id = request.form['itemid']
    store_id = request.form['storeid']
    model_input = transform_user_input(int(store_id), int(item_id))
    prediction = [math.floor((prediction_model.predict(model_input)[0]))]
    return render_template("main_page.html", prediction=prediction, user_image = full_filename)


def transform_user_input(store, item):
  model_input = pd.DataFrame({"store":store,"item":item}, index=[0])
  return model_input

@app.route("/anomaly-detection")
def anomaly_detection_page():
    return render_template("a_detection.html", user_image = full_filename)

@app.route('/anomaly-detection', methods=['POST'])
def a_detection_parameters():

    detection_model = keras.models.load_model("anomaly_detection_model.h5")

    product_id = int(request.form['productid'])
    city_id = int(request.form['cityid'])
    order_amount = int(request.form['orders'])

    detection_model_input = np.array([ [product_id,city_id,order_amount] ])
    detection_model_output = detection_model.predict(detection_model_input)
    anomaly_score = np.sqrt(metrics.mean_squared_error(detection_model_output, detection_model_input))

    "The score was selected during the model training process"

    if anomaly_score > 8 :
        output_to_display = "ANOMALY DETECTED"
    else:
        output_to_display = "No anomaly detected"

    return render_template("a_detection.html", prediction=output_to_display, user_image = full_filename)


if __name__ == "__main__":
     app.run(debug=True)
