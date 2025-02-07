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
class Venda(db.Model):
  __tablename__ = 'vendas'
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  produto = db.Column(db.String(255), nullable=False)
  quantidade = db.Column(db.Integer, nullable=False)
  valor_unitario = db.Column(db.Numeric, nullable=False)

  def __repr__(self):
    return f'<Produto: {self.produto}>'

# # DEFININDO TABELA DOS ARQUIVOS BRUTOS
# class arquivoCSV(db.Model):
#     __tablename__ = 'arquivo_csv'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nome = db.Column(db.String(255), nullable=False)
#     path = db.Column(db.String(255), nullable=False)
    
#     def __repr__(self):
#         return f'<ArquivoCSV {self.nome_arquivo}>'

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
  # VALIDACOES
  if 'file' not in request.files:
    return jsonify({"message": "Nenhum arquivo enviado!"}), 400
  
  arquivo = request.files['file']
  if arquivo.filename == '':
    return jsonify({"message": "Arquivo não selecionado!"}), 400
  
  # LER O CSV COM PANDAS
  try:
    pd_file = pd.read_csv(arquivo)
  except Exception as e:
    return jsonify({"mensagem": f"Erro ao ler o arquivo {str(e)}"}), 400
  
  # Verificar se as colunas estão corretas
  colunas_req = {'produto', 'quantidade', 'valor'}
  if not colunas_req.issubset(pd_file.columns):
    return jsonify({"o arquivo CSV precisa ter as colunas: 'produto', 'quantidade', 'valor'"})


  # SALVAR OS DADOS NO POSTGRES
  try:
    for _, row in pd_file.iterrows():
      nova_venda = Venda(
        produto = row['produto'],
        quantidade = int(row['quantidade']),
        valor = float(row['valor'])
      )

      db.session.add(nova_venda)
    db.session.commit()

  except Exception as e:
    db.session.rollback()
    return jsonify({"mensagem: " f"Erro ao salvar no banco de dados {str(e)}"}), 500
  

if __name__ == '__main__':
    app.run(debug=True)