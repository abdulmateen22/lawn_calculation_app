from flask import Flask, render_template, request, send_file
from requests import get

from flask_bootstrap import Bootstrap
from forms.map_form import MapForm 

app = Flask(__name__)

# setting encryption key required for forms
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

Bootstrap(app)

def download_image(input):
    latitude, longitude =  [float(value.strip()) for value in input.split(",")]

    response = get(f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&scale=0&zoom=20&maptype=satellite&size=800x800&key=AIzaSyCxAXu13Dw608G7O9ON4iPxDttXeE27DQs", stream=True)
  
    with open('static/map/image.png', 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
      coors = request.form.get('coors')
      download_image(coors)

      # perform any necessary processing on the image
      # and save the image to processed directory

      return send_file("static/map/image.png", as_attachment=True)

    return render_template('index.html')


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False, threaded=True, use_reloader=True)