from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
import os

#-------------- Carregando o Modelo -------------------
import pickle

with open("../../models/modelo.sav", 'rb') as arquivo:
    modelo = pickle.load(arquivo)

colunas = ['tamanho', 'ano', 'garagem']
#------------------------------------------------------

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tradutor = Translator()
    frase_en = tradutor.translate(frase, dest='en')
    tb_en = TextBlob(frase_en.text)
    polaridade = tb_en.sentiment.polarity

    return f"polaridade: {polaridade}"

"""
@app.route('/cotacao/<int:tamanho>')
def cotacao(tamanho):
    preco = modelo.predict([[tamanho]])
    return str(preco)
"""
@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')