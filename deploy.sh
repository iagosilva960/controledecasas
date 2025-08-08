#!/bin/bash

echo "=== Script de Deploy - Controle de Casas ==="
echo ""

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto"
    exit 1
fi

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "🔧 Configurando variáveis de ambiente..."
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
export PORT="${PORT:-8080}"

echo ""
echo "🚀 Iniciando aplicação em modo produção..."
echo "Porta: $PORT"
echo "GitHub Sync: Habilitado"
echo ""

# Executar com Gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 src.main:app

