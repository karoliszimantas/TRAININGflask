from app import app
from flask import render_template, request, redirect, make_response, jsonify, send_from_directory, abort
import os

@app.template_filter('custom_filter')
def custom_filter(a):
    return 'Custom filter + {0}'.format(a)


@app.route("/")
def main():
    print(f'Flask env is {app.config["ENV"]}')
    return render_template('public/templates/index.html')


@app.route("/about")
def about():
    return '<h1>About</h1>'


@app.route("/sign_up", methods=['GET', 'POST'])
def sig_up():
    if request.method == 'POST':
        req = request.form
    return render_template('public/templates/sign_up.html')


@app.route('/profile/<username>')
def profile(username):
    return render_template('public/templates/profile.html')


app.config['IMAGE_UPLOADS'] = r"C:\Users\User\Desktop\python courses\draft\app\app\templates\static\img\uploads"

@app.route('/upload-image', methods=['POST', 'GET'])
def upload_image():

    if request.method == "POST":
        if request.files:
            image=request.files["image"]
            if image.filename == "":
                print('Image must have a filename')
                return redirect(request.url)
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
            return redirect(request.url)

    return render_template('public/templates/upload.html')


app.config['CLIENT_IMAGES'] = r'C:\Users\User\Desktop\python courses\draft\app\app\templates\static\client\img'
app.config['CLIENT_CSV']= r'C:\Users\User\Desktop\python courses\draft\app\app\templates\static\client\csv'

@app.route('/get-image/<picture>')
def get_image(picture):
    try:
        return send_from_directory(app.config['CLIENT_IMAGES'], filename=picture, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app.route('/get-csv/<csv>')
def get_csv(csv):
    try:
        return send_from_directory(app.config['CLIENT_IMAGES'], filename=csv, as_attachment=False)
    except FileNotFoundError:
        abort(404)


@app.route('/json', methods=['POST'])
def json():

    if request.is_json:
        req = request.get_json()
        response = {
            "name":req.get("name")
        }
        res = make_response(jsonify(response), 200)

        return res

    else:
        res = make_response(jsonify({"message":"No json received"}), 400)

    return "no Json received", 400


@app.route("/guestbook")
def guestbook():
    return render_template("public/templates/guestbook.html")

@app.route("/jinja")
def jinja():

    my_name = 'Name'

    langs = ['Python', 'Java', 'C#']

    more = {'Steve':30,
            'John':45,
            'Mete':89,
            'Vere':45}

    other=('Last', 'Lost')

    class New:
        def __init__(self, name, other):
            self.name = name
            self.other = other

        def pull(self):
            return f'Name is {self.name}'

    def repeat(x, qty):
        return x * qty

    my_new=New('First', 'Second')

    return render_template('public/templates/jinja.html',
                           langs=langs,
                           more=more,
                           New=New,
                           repeat=repeat,
                           my_new=my_new,
                           my_name=my_name,
                           other=other)