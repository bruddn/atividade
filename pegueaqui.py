from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request 
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
import hashlib


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testeuser:22toledoads24@localhost:3306/pegueaqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://brunadneves:22toledoads24@brunadneves.mysql.pythonanywhere-services.com:3306/brunadneves$pegueaqui'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = '22tadstoledo24'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
global userlogado



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
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


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

class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column('fav_id', db.Integer, primary_key=True)
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id', db.Integer, db.ForeignKey("anuncio.anu_id"))

    def __init__(self, usu_id, anu_id):
        self.usu_id = usu_id
        self.anu_id = anu_id

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/login", methods=['GET', 'POST'])
def login():
    global userlogado
    if request.method == 'POST':
        email =  request.form.get('email')
        passwd = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(email=email, senha=passwd). first()

        if user:
            userlogado = user.id
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
@login_required
def index ():
    return render_template('index.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncios")

@app.route("/cad/usuario")
def cadusuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo = 'Usuario')


@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    hash = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('user'), request.form.get('email'), hash)
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
        usuario.senha = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()
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
    return render_template('relCompras.html', relatoriocs = Relatorioc.query.all(), titulo = 'Relatório de Compras')

@app.route("/relatoriosc/criar", methods=['POST'])
def criarrelatorioc():
    relatorioc = Relatorioc (request.form.get('qtd'), request.form.get('preco'), request.form.get('total'), request.form.get('usu'), request.form.get('anu'))
    db.session.add(relatorioc)
    db.session.commit()
    return redirect(url_for('relCompras'))

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html', relatoriovs = Relatoriov.query.all(), titulo = 'Relatório de Vendas')

@app.route("/relatoriosv/criar", methods=['POST'])
def criarrelatoriov():
    relatoriov = Relatoriov (request.form.get('qtd'), request.form.get('preco'), request.form.get('total'), request.form.get('usu'), request.form.get('anu'))
    db.session.add(relatoriov)
    db.session.commit()
    return redirect(url_for('relVendas'))

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio") # Anuncio.filter_by(usu_id=userlogado) não funcionou, apareceu attributerror: type object 'Anuncio' has no attribute 'filter'

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    global userlogado
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'), request.form.get('qtd'), request.form.get('preco'), request.form.get('cat'), userlogado) # request.form.get('uso'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/editar/<int:id>", methods=['GET', 'POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method =='POST':
        anuncio.nome = request.form.get('nome')
        anuncio.descricao = request.form.get('desc')
        anuncio.quantidade = request.form.get('qtd')
        anuncio.preco = request.form.get('preco')
        anuncio.categoria = request.form.get('cat')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))
    
    return render_template('editanuncio.html', anuncio = anuncio, titulo = 'Anuncio')

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
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
    return render_template('favoritos.html', favoritos = Favorito.query.all(), titulo='Favoritos')

@app.route("/favoritos/criar", methods=['POST'])
def criarfavoritos():
    favoritos = Favorito(request.form.get('usu'), request.form.get('anu'))
    db.session.add(favoritos)
    db.session.commit()
    return redirect(url_for('favoritos'))


if __name__ == 'pegueaqui':
    with app.app_context():
        db.create_all()
   


