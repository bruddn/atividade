from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request 
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testeuser:22toledoads24@localhost:3306/pegueaqui'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha 

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__(self, nome, desc):
        self.nome = nome
        self.desc = desc

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id', db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id

class Relatorioc(db.Model):
    __tablename__ = "relCompras"
    id = db.Column('comp_id', db.Integer, primary_key=True)
    qtd = db.Column('comp_qtd', db.Integer)
    preco = db.Column('comp_preco', db.Float)
    total = db.Column('comp_total', db.Float)
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey("anuncio.anu_id"))

    def __init__(self, qtd, preco, total, usu_id, anu_id):
        self.qtd = qtd
        self.preco = preco
        self.total = total
        self.usu_id = usu_id
        self.anu_id = anu_id

class Relatoriov(db.Model):
    __tablename__ = "relVendas"
    id = db.Column('vend_id', db.Integer, primary_key=True)
    qtd = db.Column('vend_qtd', db.Integer)
    preco = db.Column('vend_preco', db.Float)
    total = db.Column('vend_total', db.Float)
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey("anuncio.anu_id"))

    def __init__(self, qtd, preco, total, usu_id, anu_id):
        self.qtd = qtd
        self.preco = preco
        self.total = total
        self.usu_id = usu_id
        self.anu_id = anu_id

class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column('perg_id', db.Integer, primary_key=True)
    perguna = db.Column('perg_pergunta', db.String(256))
    resposta = db.Column('perg_resposta', db.String(256))
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey("anuncio.anu_id"))

    def __init__(self, pergunta, resposta, usu_id, anu_id):
        self.pergunta = pergunta
        self.resposta = resposta
        self.usu_id = usu_id
        self.anu_id = anu_id

class Favoritos(db.Model):
    __tablename__ = "favoritos"
    id = db.Column('fav_id', db.Integer, primary_key=True)
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey("anuncio.anu_id"))

    def __init__(self, usu_id, anu_id):
        self.usu_id = usu_id
        self.anu_id = anu_id

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@app.route("/")
def index ():
    return render_template('index.html')

@app.route("/cad/usuario")
def cadusuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo = 'Usuario')

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('user'), request.form.get('email'), request.form.get('passwd'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method =='POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('passwd')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('cadusuario'))
    
    return render_template('editusuario.html', usuario = usuario, titulo = 'Usuario')

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html', relatoriocs = Relatorioc.query.all(), titulo = 'Relatorio de Compras')

@app.route("/relatoriosc/criar", methods=['POST'])
def criarrelatorioc():
    relatorioc = Relatorioc (request.form.get('qtd'), request.form.get('preco'), request.form.get('total'), request.form.get('usu'), request.form.get('anu'))
    db.session.add(relatorioc)
    db.session.commit()
    return redirect(url_for('relCompras'))

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html', relatoriovs = Relatoriov.query.all(), titulo = 'Relatorio de Vendas')

@app.route("/relatoriosv/criar", methods=['POST'])
def criarrelatoriov():
    relatoriov = Relatoriov (request.form.get('qtd'), request.form.get('preco'), request.form.get('total'), request.form.get('usu'), request.form.get('anu'))
    db.session.add(relatoriov)
    db.session.commit()
    return redirect(url_for('relVendas'))

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', categorias = Categoria.query.all(), anuncios = Anuncio.query.all(), titulo='Anuncios')

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'), request.form.get('qtd'), request.form.get('preco'), request.form.get('cat'), request.form.get('uso'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/pergunta")
def pergunta():
    return render_template('pergunta.html', perguntas = Pergunta.query.all(), titulo='Perguntas')

@app.route("/pergunta/criar", methods=['POST'])
def criarpergunta():
    pergunta = Pergunta (request.form.get('pergunta'), request.form.get('resposta'), request.form.get('usu'), request.form.get('anu'))
    db.session.add(pergunta)
    db.session.commit()
    return redirect(url_for('pergunta'))


@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/favoritos")
def favoritos():
    return render_template('favoritos.html', favoritos = Favoritos.query.all(), titulo='Favoritos')

@app.route("/favoritos/criar", methods=['POST'])
def criarfavoritos():
    favoritos = Favoritos(request.form.get('usu'), request.form.get('anu'))
    db.session.add(favoritos)
    db.session.commit()
    return redirect(url_for('favoritos'))


if __name__ == 'pegueaqui':
    with app.app_context():
        db.create_all()
   


