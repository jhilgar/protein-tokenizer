from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

    @app.route('/', methods = ['POST'])
    def post():
        input_text = request.form.get('query', '')
        print(input_text)
        return jsonify({'input_text': input_text})
    
    return app