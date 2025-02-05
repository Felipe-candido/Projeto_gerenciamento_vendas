import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import psycopg2
from os import environment

# PASTA PARA SALVAR OS ARQUIVOS CSV
UPLOAD_FOLDER = '/backend'

app = Flask(__name__)
app.config
CORS(app)

# CONFIGURANDO CONEXAO COM BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/vendas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DEFININDO MODELOS DAS TABELAS
class venda(db.Model):
   __tablename__ = 'vendas'
   id = db.Column(db.Integer, primary_key=True, nullable=False)
   produto = db.Column(db.String(255), nullable=False)
   quantidade = db.Column(db.Integer, nullable=False)
   valor_unitario = db.Column(db.Numeric, nullable=False)

# CRIAR TABELA CASO NAO EXISTIR
with app.app_context():
   db.create_all()


# ROTA TESTE NA RAIZ
@app.route('/')
def home():
    return 'Testando api de gerenciamento de vendas'


# ROTA PARA FAZER UPLOAD DO ARQUIVO
@app.route('/upload', methods=['POST'])
def upload_arquivo():
  # VALIDACAO SE O ARQUIVO
  if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado!"}), 400
  
  arquivo = request.files['file']
  if arquivo.filename == '':
        return jsonify({"message": "Arquivo não selecionado!"}), 400
  file_path = os.path.join(UPLOAD_FOLDER, arquivo.filename)
  arquivo.save(file_path)
