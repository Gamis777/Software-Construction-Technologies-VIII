from flask import Flask, jsonify, request
from flask_language import Language, current_language
from email.mime import message
from flask import Flask, jsonify, make_response, request
app = Flask(__name__)
lang = Language(app)

@lang.allowed_languages
def get_allowed_languages():
    return ['en', 'es']

@lang.default_language
def get_default_language():
    return 'en'

@app.route('/api/lang')
def get_language():
    return jsonify({
        'lang': str(current_language),
    })

@app.route('/api/lang', methods=['POST'])
def set_language():
    req = request.get_json()
    language = req.get('lang', None)

    lang.change_language(language)

    return jsonify({
        'lang': str(current_language),
    })

@app.route('/cookies',methods=['GET'])
def cookie_example():
    resp=request.cookies.get('lang')
    if (resp is None):
        response = make_response ('Por defecto hemos selecccioando el idioma Ingles')
        response.set_cookie ('lang','Inglés')
        return response,200

    elif (resp == 'Inglés'):
        response = {'message' :'El idioma seleccionado es Inglés'}
        return jsonify(response),200
        
    elif (resp == 'Español'):
        response = {'message':'El idioma seleccionado Español'}
        return jsonify(response),200
    else:
        response = {'message':'No hay idioma seleccionado'}
        return jsonify(response),200

if __name__ == "__main__":
    app.run(debug=True)