import os
from flask import Flask, request, render_template, send_from_directory
from scipy.misc import imsave,imread ,imresize
import numpy as np
import keras.models
import re
import sys
from keras.preprocessing import image as image_utils

sys.path.append(os.path.abspath('./model'))
from load import *

global model,graph,predict
model,graph= init()

app = Flask(__name__)
APP_ROOT = os.path.join(app.root_path, "")

@app.route("/")
def index():
    
    print("working")
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])

def upload():
    target = os.path.join(APP_ROOT, 'dataset')
   # print("target",target)
    
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
      #  print(upload)
       # print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
       # print ("Accept incoming file:", filename)
       # print ("Save it to:", destination)
        upload.save(destination)
        
        from keras.preprocessing import image as image_utils
        import numpy as np
        
        test_image = image_utils.load_img(destination, target_size=(64, 64))
        test_image = image_utils.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
         
        result = model.predict_on_batch(test_image)
        predict=1
        if(result==1):
            print("dog")
            predict="Dog"
        else:
            print("cat")
            predict="Cat"
      
    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete_display_image.html", image_name=filename,prediction =predict)


@app.route('/upload/<filename>')
def send_image(filename):
    print("sending image",filename)
    return send_from_directory("dataset", filename)


if __name__ == "__main__":
    app.run(port="5001")