#!/usr/local/bin/python
from flask import Flask
from flask import render_template
from flask import request, redirect

#import googleapiclient.discovery
import json


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def predict_json(project, region, model, instances, version=None):
    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

@app.route('/predict', methods=['POST'])
def form():
    data=[]
    project="tf-blog"
    region="uscentral1"
    model="tfblog"
    instance=[[5.1, 3.5, 1.4, 0.2]]
    version="v1"
    #irisvalules = request.form['iris-values']
    prediction=predict_json(project,region,model,instance,version)
    for result in prediction:
         for k, v in result.items():
             for i in range(len(v)):
                data.append('%.08f' % (v[i]*100))
    labels=["Iris Setosa", "Iris Versicolor"," Iris Virginica"]   
    return render_template('index.html', data=data, labels=labels)

@app.route('/')
def hello():
    #instance=[[5.1, 3.5, 1.4, 0.2]]
    #preds = predict_json("tf-blog","us-east1","tf_blog",instance,"v1")
    #return str(preds)
    return render_template('index.html')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)