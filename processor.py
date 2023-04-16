import json
import os
from zipfile import ZipFile

from flask import Flask, render_template, request, send_file,send_from_directory
from requests import get
from inference import detect
from flask_bootstrap import Bootstrap
import cv2
# from forms.map_form import MapForm
from geopy.geocoders import Nominatim

app = Flask(__name__)

# setting encryption key required for forms and email as well
geolocator = Nominatim(user_agent="your email")
# your key and email there
app.config['SECRET_KEY'] = 'your keys'

Bootstrap(app)

def download_image(input):
    latitude, longitude =  [float(value.strip()) for value in input.split(",")]
    location = geolocator.geocode(input)
    response = get(f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&scale=10&zoom=21&maptype=satellite&size=800x800&key=AIzaSyCxAXu13Dw608G7O9ON4iPxDttXeE27DQs", stream=True)
  
    with open('static/map/image.jpg', 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    return location

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':

        coors = request.form.get('coors')
        location=download_image(coors)

      # perform any necessary processing on the image
      # and save the image to processed directory
        image="static/map/image.jpg"
        flag,path_j,di,path_z,fol = detect(image)
        di['Address']= str(location)
        with open(f'{path_j}.json','w')as f:
            json.dump(di,f,indent=4)
        f.close()
        print(path_z)
        with ZipFile(f'{path_z}.zip', 'w') as zip:
            # writing each file one by one
            ls = os.listdir(path_z)
            for file in ls:
                zip.write(f'{path_z}/{file}')
        if flag == True:
            print('*** SUCCESS ***')
            return send_file(f'{path_z}.zip', as_attachment=True)
        else:
            print('*** FAILED ***')



    return render_template('index.html')


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False, threaded=True)