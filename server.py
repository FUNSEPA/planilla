from core import tools
import pathlib
from subprocess import call
from flask import Flask, render_template, request
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = set(['xlsx', ])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/preview', methods=['GET', 'POST'])
def preview():
    data = {
        'quincena': request.form.get('quincena', 1),
        'individual': request.form.get('individual', 0),
        'enviar': request.form.get('enviar', False),
        'file': request.files['archivo']
    }
    if data['file']:
        file_name = str(pathlib.Path(app.config['UPLOAD_FOLDER']) / data['file'].filename)
        data['file'].save(file_name)
        planilla = tools.PlanillaParser(
            quincena=int(data['quincena']),
            file_name=data['file'].filename)
    return render_template("index.html", data=data, planilla=planilla, file_name=data['file'].filename)


@app.route('/send', methods=['POST'])
def enviar():
    data = {
        'quincena': request.form.get('quincena', 1),
        'individual': request.form.get('individual', 0),
        'enviar': request.form.get('enviar', 0),
        'file_name': request.form.get('file_name')
    }
    comando = 'python main.py --quincena={} --individual={} --filename="{}" {}'.format(
        data['quincena'],
        data['individual'],
        data['file_name'],
        '--enviar' if data['enviar'] == "1" else '')
    print(comando)
    call([comando], shell=True)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
