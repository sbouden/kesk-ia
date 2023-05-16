from flask import Flask ,redirect, render_template , url_for,jsonify
#from flask_mysqldb import MySQL
from flask import request
from flask import flash
#import MySQLdb.cursors
#import pymysql
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
import uuid
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor
import requests
from io import BytesIO

API_URL_PREDICT = "https://api-safer-road-ddlzhsitgq-od.a.run.app/predict"


# Warmup
requests.get(API_URL_PREDICT)

### PREDICTION ###

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def detect(upload):
    image = Image.open(upload)
    
    files = {'file':  convert_image(image)}
    response = requests.post(API_URL_PREDICT, files=files)
    predictions = json.loads(response.content)
    print(predictions)
    
    # Image avec les prédictions
    # define a font for the class labels

    draw = ImageDraw.Draw(image, "RGBA")
    img_fraction = image.size[1] / 3200
    font = ImageFont.truetype("arial.ttf", int(max(15, 60 * img_fraction)))
    class_names = {
        0: "Crack",
        1: "Tags",
        2: "Pothole",
        # add more class numbers and names as needed
    }

    class_colors = {
        0: "red",
        1: "blue",
        2: "orange",
    }
    for p in predictions:
        cls, (x, y, w, h, proba) = p

        # get the color for this class label
        name = class_names.get(cls, "unknown")
        color = class_colors.get(cls, "white")

        # get the RGB values of the color and add alpha for transparency
        fill_color = tuple(list(ImageColor.getrgb(color)) + [int(255*0.05)])

        # draw the bounding box
        draw.rectangle([(x, y), (w, h)], outline=color, fill=fill_color, width=2)

        # draw the class label on top of the bounding box
        label = f"{name} ({proba:.2f})"
        draw.text((x, y-20), label, fill=color, font=font)
    return image

### END PREDICTION ###

UPLOAD_FOLDER = 'static/uploads/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/safer_road'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#connection = pymysql.connect(host="localhost", user="root", password="", database="safer_road")
#cursor = connection.cursor()

#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

""" debuglar icin """
if __name__ == "__main__":
    app.run(debug=True)



# """ MODELS """

# class Response(db.Model):
#     db.init_app(app)
#     migrate.init_app(app, db)
#     id = db.Column("id",db.Integer, primary_key=True)
#     img = db.Column("image",db.String(500))
#     risk = db.Column("risk",db.String(500))
#     explain = db.Column("explain",db.String(500))

# class User(db.Model):
#     db.init_app(app)
#     migrate.init_app(app, db)
#     id = db.Column("id",db.Integer, primary_key=True)
#     img = db.Column("img",db.String(500))
#     ip_no = db.Column("ip_no",db.String(20))
#     location = db.Column("location",db.String(500))
#     img_size = db.Column("size",db.Integer())
#     img_type = db.Column("type",db.String(50))

#     def __init__( self, img:str, location:str, ip:int, img_size:int, img_type:str ):
#         self.img = img
#         self.ip_no = ip
#         self.location = location
#         self.img_size = img_size
#         self.img_type = img_type

# class Admin(db.Model):
#     db.init_app(app)
#     migrate.init_app(app, db)
#     id = db.Column("id",db.Integer, primary_key=True)
#     name = db.Column("name",db.String(50))
#     surname = db.Column("surname",db.String(50))
#     email = db.Column("email",db.String(150),unique=True)
#     passwordhash = db.Column("passwordhash",db.String(500))

# class TEST(db.Model):
#     db.init_app(app)
#     migrate.init_app(app, db)
#     id = db.Column("id", db.Integer, primary_key=True)
#     name = db.Column("name", db.String(50))




@app.route('/')
def index():

    User_Info = request.remote_addr
    return render_template('about.html', IP = User_Info)
    

@app.route('/index.html')
def index_2():
    User_Info = request.remote_addr
    return render_template('index.html', IP = User_Info)


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/envoyephoto.html')
def envoyephoto():
    User_Info = request.remote_addr
    return render_template('envoyephoto.html',IP = User_Info)
    
""" Admin Routes """

@app.route('/admin.html')
def admin_home():

    users = get_data()
    return users

@app.route('/api')
def api():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})

@app.route('/upload',methods=['POST'])
@staticmethod
def create(): 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            
            flash('No file part')

            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':            
            flash('No selected file')
            return redirect(request.url)
        

        if file and allowed_file(file.filename):
            
            image = detect(file)
            image.save('static/uploads/output/detected.jpg')



            file_type = file.filename.split(".")[-1]
            file_size  = request.files['file']
            file_size.seek(0, os.SEEK_END)
            file_length = file_size.tell()

            unique_filename = str(uuid.uuid4())

            file.filename = unique_filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))        

            file_name_path = app.config['UPLOAD_FOLDER']+"/"+file.filename
            ip_no = request.remote_addr
            #user_data = User(location=request.form['adress'],ip = ip_no ,img = file_name_path, img_size =file_length, img_type = file_type) 

            #db.session.add(user_data)
            #db.session.commit()

            User_Info = request.remote_addr
            return render_template('image_output.html', IP = User_Info)

def get_data():
    cursor.execute("SELECT * FROM USER")
    rows = cursor.fetchall()
    return rows

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




@app.route("/check")
def home():
    return render_template("check_image.html")


@app.route('/predict', methods=['POST'])
def predict():
    # Resim dosyasını yükle
    file = request.files['image'].read()
    image = Image.open(io.BytesIO(file))
    image = np.array(image)
    
    # Detectron2 kullanarak şekil tespiti yap
    outputs = predictor(image)
    boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    
    # HTML şablonuna tahmin sonuçlarını gönder
    return render_template('predict.html', boxes=boxes)