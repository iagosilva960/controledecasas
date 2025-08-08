import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.imovel import Imovel, FotoImovel, Contrato
from src.routes.user import user_bp
from src.routes.imoveis import imoveis_bp
from src.github_sync import GitHubSync

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS
CORS(app)

# Configurar GitHub Sync
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO_OWNER = 'iagosilva960'
GITHUB_REPO_NAME = 'controledecasas'

github_sync = GitHubSync(GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(imoveis_bp, url_prefix='/api')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def backup_to_github():
    """Faz backup dos dados para o GitHub"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        return github_sync.backup_database(db_path)
    except Exception as e:
        print(f"Erro no backup: {e}")
        return False

def restore_from_github():
    """Restaura dados do GitHub"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        return github_sync.restore_database(db_path)
    except Exception as e:
        print(f"Erro na restauração: {e}")
        return False

with app.app_context():
    # Tentar restaurar dados do GitHub primeiro
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado. Tentando restaurar do GitHub...")
        if restore_from_github():
            print("Dados restaurados do GitHub com sucesso!")
        else:
            print("Não foi possível restaurar do GitHub. Criando novo banco...")
    
    db.create_all()
    
    # Fazer backup inicial
    if backup_to_github():
        print("Backup inicial realizado com sucesso!")
    else:
        print("Falha no backup inicial.")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
