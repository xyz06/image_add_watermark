import flask
import os
import image_add_watermark
import urllib.parse


app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/upload",methods=["POST"])
def upload():
    img = flask.request.files.get("fileName")
    text = flask.request.form.get("text")
    color = flask.request.form.get("color")
    if not img or not text:
        return flask.render_template("alert.html", alert="No img or no text")
    if not color or color not in ['white', 'blue', 'red', 'orange', 'yellow', 'green', 'black']:
        color = "white"
    dir_path = os.path.dirname(os.path.abspath(__file__))+"/static/image"
    # print(dir_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    img_path = dir_path +"\\"+ img.filename
    img.save(img_path)
    filename = image_add_watermark.image_add_text(img_path,text,color)

    return flask.render_template("download.html",img_name="image_watermark/"+filename)

@app.route("/download")
def download():
    if "img" in flask.request.values:
        img = urllib.parse.quote(flask.request.values.get("img"))
        dir_path = os.path.dirname(os.path.abspath(__file__)) + "/static/"
        # print(dir_path)
        return flask.send_from_directory(dir_path, img, as_attachment=True)
    else:
        return flask.render_template("alert.html", alert="No image")


if __name__ == "__main__":
    app.run()