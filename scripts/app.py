"""
This script host interface for resume parsing.
"""
#---standard library---
import os

#---Third party library---
from flask import Flask,render_template,request,redirect,url_for
from werkzeug import secure_filename
from flask import send_file, send_from_directory, safe_join, abort

#---Local library---
from aws_s3_image_upload import *
from logger_config import *
import logger_config
from constants import *

#---Configuring log filename---
log_file=os.path.splitext(os.path.basename(__file__))[0]+".log"
log = logger_config.configure_logger('default', ""+DIR+""+LOG_DIR+"/"+log_file+"")

#---Configuring app object---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#---Home page calling function---
@app.route('/')
def hello_world():
    return render_template("home.html")

#---Calls image uploading function---
@app.route('/upload_img',methods = ['POST', 'GET'])
def result():
    """
    This function calls image uploder function that uploads image to s3
    and stores s3 url to database. 
    """
    if request.method == 'POST':
        try:
            f = request.files['file']
            if f:
                filename=secure_filename(f.filename)#Gets uploaded file name.
                #print(filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#Saves input file to specified folder.
                image_url=s3_upload()
                print(image_url)
                #status=get_entity(filename)#Gets all the skill specified in JD
                #txt_filename=filename.rsplit(".")[0]
                #get_similarity(txt_filename)#Match skill with stored resume.
                return redirect(url_for('success',image_url="bikash"))
            else:
                return "<p>File not uploaded</p>"
        except Exception as e:
            log.error(colored(str(e),"red"))
            return render_template("error.html")


#---Returns download option interface---
@app.route('/success/<image_url>')
def success(image_url):
    """
    This function gets called once the file is uploaded successfully.
    """
    try:
        return render_template("success.html",image_url="https://vmoksha-ali.s3.amazonaws.com/best-ugadi-wishes-and-messages.jpg")
    except Exception as e:
        log.error(colored(str(e),"red"))          


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)