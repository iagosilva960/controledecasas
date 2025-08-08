import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class GitHubSync:
    def __init__(self, token: str, repo_owner: str, repo_name: str):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
    def _get_file_sha(self, file_path: str) -> Optional[str]:
        """Obtém o SHA de um arquivo no repositório"""
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get('sha')
        return None
    
    def save_data_to_github(self, data: Dict[str, Any], file_path: str = "data/backup.json") -> bool:
        """Salva dados no repositório GitHub"""
        try:
            # Preparar dados com timestamp
            backup_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            
            # Converter para JSON
            content = json.dumps(backup_data, indent=2, ensure_ascii=False)
            
            # Codificar em base64
            import base64
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            # Verificar se arquivo já existe
            sha = self._get_file_sha(file_path)
            
            # Preparar payload
            payload = {
                "message": f"Backup automático - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
                "content": encoded_content,
                "branch": "main"
            }
            
            if sha:
                payload["sha"] = sha
            
            # Fazer upload
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
            response = requests.put(url, headers=self.headers, json=payload)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"Erro ao salvar no GitHub: {e}")
            return False
    
    def load_data_from_github(self, file_path: str = "data/backup.json") -> Optional[Dict[str, Any]]:
        """Carrega dados do repositório GitHub"""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                import base64
                content = base64.b64decode(response.json()['content']).decode('utf-8')
                backup_data = json.loads(content)
                return backup_data.get('data', {})
            
            return None
            
        except Exception as e:
            print(f"Erro ao carregar do GitHub: {e}")
            return None
    
    def backup_database(self, db_path: str) -> bool:
        """Faz backup do banco de dados SQLite"""
        try:
            # Ler arquivo do banco
            with open(db_path, 'rb') as f:
                db_content = f.read()
            
            # Codificar em base64
            import base64
            encoded_content = base64.b64encode(db_content).decode('utf-8')
            
            # Verificar se arquivo já existe
            file_path = "data/database_backup.db"
            sha = self._get_file_sha(file_path)
            
            # Preparar payload
            payload = {
                "message": f"Backup do banco de dados - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
                "content": encoded_content,
                "branch": "main"
            }
            
            if sha:
                payload["sha"] = sha
            
            # Fazer upload
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
            response = requests.put(url, headers=self.headers, json=payload)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"Erro ao fazer backup do banco: {e}")
            return False
    
    def restore_database(self, db_path: str) -> bool:
        """Restaura o banco de dados do GitHub"""
        try:
            file_path = "data/database_backup.db"
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                import base64
                db_content = base64.b64decode(response.json()['content'])
                
                # Criar diretório se não existir
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                
                # Escrever arquivo
                with open(db_path, 'wb') as f:
                    f.write(db_content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao restaurar banco: {e}")
            return False

