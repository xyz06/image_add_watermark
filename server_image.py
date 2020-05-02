import flask
import os
import image_add_watermark
import urllib.parse


app = flask.Flask(__name__)

def getFile(fileName):
    data = b""
    if os.path.exists(fileName):
        fobj = open(fileName, "rb")
        data = fobj.read()
        fobj.close()
    return data


@app.route("/")
def index():
    return getFile("index.html")


@app.route("/upload",methods=['POST'])
def upload():
    img = flask.request.files.get('fileName')
    text = flask.request.form.get('text')
    if not img or not text:
        return flask.render_template("alert.html",alert="No img or no text")

    dir_path = os.path.abspath(os.path.dirname(__file__)+"/static/image")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    img_path = dir_path +"\\"+ img.filename
    img.save(img_path)
    filename = image_add_watermark.image_add_text(img_path,text)

    return flask.render_template("download.html",img_name= 'image_watermark/'+filename)

@app.route("/download")
def download():
    if "img" in flask.request.values:
        img = urllib.parse.quote(flask.request.values.get("img"))
        dir_path = os.path.abspath(os.path.dirname(__file__)) + "/static/"
        print(dir_path)
        return flask.send_from_directory(dir_path, img, as_attachment=True)
    else:
        return "No image"


if __name__=="__main__":
    app.run()