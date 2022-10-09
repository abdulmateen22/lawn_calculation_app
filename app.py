from flask import Flask, render_template, request
import cv2, json
import numpy as np
from inference import detect
import glob



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        # image = request.files.get('image')
        image = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        url = request.host_url
        flag = detect(image)

        if flag == True:
            print('*** SUCCESS ***')
            response = app.response_class(
                response=json.dumps(f'Results Successfully Generated at: {url}'),
                status=200,
                mimetype='application/json'
            )
        else:
            print('*** FAILED ***')
            response = app.response_class(
                response=json.dumps('Process Failed due to: '),
                status=200,
                mimetype='application/json'
            )
        # return result_list
        return response

if __name__ == '__main__':
        app.run(debug = False)