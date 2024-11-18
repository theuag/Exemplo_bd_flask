from flask import Flask, render_template, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo.db'
db = SQLAlchemy(app)

# Definição do modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def toJSON(self):
        return {"id": self.id, "name": self.nome, "email": self.email}

# Rota para o formulário
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Recebe os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        
        # Cria um novo usuário
        user = User(nome=nome, email=email)
        
        # Adiciona ao banco de dados
        db.session.add(user)
        db.session.commit()
        
        return render_template("index.html", message="Usuário cadastrado com sucesso!")
    
    return render_template("index.html")

# Criação do banco de dados ao iniciar o app

@app.route("/ver")
def ver():
    users = User.query.all()
    userJson = []
    for user in users:
        userJson.append(user.toJSON())
    
    return jsonify(userJson)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
