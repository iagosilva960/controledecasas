# Instruções para Deploy - Controle de Casas

## 🚀 Deploy no Fly.io

### Pré-requisitos
1. Conta no Fly.io
2. Fly CLI instalado
3. Repositório GitHub conectado

### Passos para Deploy

#### 1. Preparar o Ambiente
```bash
# Clonar o repositório (se necessário)
git clone https://github.com/iagosilva960/controledecasas.git
cd controledecasas
```

#### 2. Configurar o Fly.io
```bash
# Fazer login no Fly.io
fly auth login

# Verificar configuração (arquivo fly.toml já existe)
fly status
```

#### 3. Deploy da Aplicação
```bash
# Deploy direto
fly deploy

# Ou usando o script personalizado
./deploy.sh
```

#### 4. Configurar Variáveis de Ambiente (se necessário)
```bash
# Definir token do GitHub (já configurado no código)
fly secrets set GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
```

## 🔧 Deploy Manual (Servidor Próprio)

### Usando o Script de Deploy
```bash
# Dar permissão de execução
chmod +x deploy.sh

# Executar
./deploy.sh
```

### Deploy Manual Passo a Passo
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
export PORT=8080

# 3. Executar em produção
gunicorn --bind 0.0.0.0:8080 --workers 2 src.main:app
```

## 📋 Verificações Pós-Deploy

### 1. Testar Endpoints
```bash
# Dashboard
curl https://sua-app.fly.dev/api/dashboard

# Listar imóveis
curl https://sua-app.fly.dev/api/imoveis

# Listar contratos
curl https://sua-app.fly.dev/api/contratos
```

### 2. Verificar Interface
- Acesse: `https://sua-app.fly.dev`
- Teste navegação entre abas
- Verifique se dados são exibidos corretamente

### 3. Testar Sincronização GitHub
- Crie um imóvel via interface
- Verifique se backup foi criado no repositório GitHub
- Caminho: `data/database_backup.db`

## 🔍 Monitoramento

### Logs da Aplicação
```bash
# Ver logs do Fly.io
fly logs

# Logs em tempo real
fly logs -f
```

### Verificar Backups
- Acesse: https://github.com/iagosilva960/controledecasas
- Navegue para: `data/database_backup.db`
- Verifique timestamp das atualizações

## 🛠️ Solução de Problemas

### Problema: Aplicação não inicia
**Solução**: Verificar logs e dependências
```bash
fly logs
pip install -r requirements.txt
```

### Problema: Backup não funciona
**Solução**: Verificar token GitHub
```bash
# Testar token manualmente
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
     https://api.github.com/user
```

### Problema: Interface não carrega
**Solução**: Verificar arquivos estáticos
- Confirmar que pasta `src/static` existe
- Verificar se `index.html` está presente

## 📊 Configurações do fly.toml

O arquivo `fly.toml` já está configurado com:
- **Região**: GRU (São Paulo)
- **Porta**: 8080
- **Memória**: 1GB
- **Auto-scaling**: Habilitado
- **HTTPS**: Forçado

## 🔐 Segurança

### Token GitHub
- Token configurado com permissões mínimas necessárias
- Acesso apenas ao repositório `controledecasas`
- Renovar token periodicamente

### Dados
- Backup automático protege contra perda de dados
- Soft delete preserva histórico
- Validação de dados no backend

## 📞 Suporte

### Em caso de problemas:
1. Verificar logs da aplicação
2. Testar endpoints individualmente
3. Verificar conectividade com GitHub
4. Consultar documentação do Fly.io

### Comandos Úteis
```bash
# Status da aplicação
fly status

# Reiniciar aplicação
fly restart

# Escalar aplicação
fly scale count 2

# Abrir shell na aplicação
fly ssh console
```

## ✅ Checklist Final

- [ ] Aplicação deployada com sucesso
- [ ] Interface carregando corretamente
- [ ] Dashboard mostrando dados
- [ ] Criação de imóveis funcionando
- [ ] Criação de contratos funcionando
- [ ] Backup automático ativo
- [ ] Logs sem erros críticos
- [ ] Performance adequada

**Status**: ✅ PRONTO PARA PRODUÇÃO

