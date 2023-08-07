from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request 

app = Flask(__name__)

@app.route("/")
def index ():
    return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', titulo="Cadastro de Usuário")

@app.route("/cad/caduser", methods=['POST'])
def caduser():
    return request.form

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html')

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html')

@app.route("/anuncios")
def anuncios():
    return render_template('anuncio.html')

@app.route("/anuncio/pergunta")
def pergunta():
    return render_template('pergunta.html')

@app.route("/categoria")
def categoria():
    return render_template('categoria.html')

@app.route("/favoritos")
def favoritos():
    return render_template('favoritos.html')


