# Controle de Imóveis

Sistema completo para gerenciamento de imóveis, contratos de aluguel e vendas. Desenvolvido com Flask (backend) e React (frontend), totalmente compatível com deploy no Fly.io.

## 🏠 Funcionalidades

### Dashboard
- Visão geral dos imóveis cadastrados
- Estatísticas de imóveis disponíveis, alugados e vendidos
- Receita mensal estimada com aluguéis
- Distribuição de imóveis por tipo

### Gestão de Imóveis
- Cadastro completo de imóveis (casas, apartamentos, terrenos, comerciais, rurais)
- Informações detalhadas: localização, características, valores
- Upload e gerenciamento de fotos
- Filtros avançados de busca
- Status de disponibilidade

### Contratos
- Contratos de aluguel e venda
- Dados completos dos clientes
- Controle de datas e valores
- Histórico de contratos

## 🚀 Tecnologias

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **Flask-CORS** - Suporte a CORS
- **SQLite** - Banco de dados (desenvolvimento)
- **Gunicorn** - Servidor WSGI para produção

### Frontend
- **React** - Biblioteca JavaScript
- **Tailwind CSS** - Framework CSS
- **shadcn/ui** - Componentes UI
- **Lucide React** - Ícones
- **React Router** - Roteamento

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### Desenvolvimento Local

1. **Clone o repositório:**
```bash
git clone https://github.com/iagosilva960/controledecasas.git
cd controledecasas
```

2. **Configure o backend:**
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python src/main.py
```

3. **Configure o frontend (desenvolvimento separado):**
```bash
# Em outro terminal, na pasta do frontend
cd imoveis_frontend
npm install
npm run dev
```

O backend estará disponível em `http://localhost:5000` e o frontend em `http://localhost:3000`.

### Produção (Integrado)

O projeto já está configurado para produção com o frontend integrado ao backend:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar com Gunicorn
gunicorn --bind 0.0.0.0:8080 --workers 2 src.main:app
```

## 🌐 Deploy no Fly.io

O projeto está 100% compatível com o Fly.io. Siga os passos:

### 1. Instalar o Fly CLI
```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Fazer login no Fly.io
```bash
fly auth login
```

### 3. Deploy da aplicação
```bash
# Na pasta do projeto
fly deploy
```

### 4. Configurar volume para persistência (opcional)
```bash
# Criar volume para o banco de dados
fly volumes create controle_imoveis_data --region gru --size 1
```

### Configurações do Fly.io

O arquivo `fly.toml` já está configurado com:
- **Região**: GRU (São Paulo)
- **Porta**: 8080
- **Memória**: 1GB
- **Auto-scaling**: Habilitado
- **HTTPS**: Forçado
- **Volume**: Configurado para persistência do banco

## 📁 Estrutura do Projeto

```
controledecasas/
├── src/
│   ├── models/          # Modelos do banco de dados
│   │   ├── user.py      # Modelo de usuário
│   │   └── imovel.py    # Modelos de imóvel, contrato, fotos
│   ├── routes/          # Rotas da API
│   │   ├── user.py      # Rotas de usuário
│   │   └── imoveis.py   # Rotas de imóveis e contratos
│   ├── static/          # Frontend React (build)
│   ├── database/        # Banco de dados SQLite
│   └── main.py          # Aplicação principal
├── Dockerfile           # Configuração Docker
├── fly.toml            # Configuração Fly.io
├── requirements.txt    # Dependências Python
└── README.md          # Documentação
```

## 🔧 API Endpoints

### Imóveis
- `GET /api/imoveis` - Listar imóveis (com filtros)
- `POST /api/imoveis` - Criar imóvel
- `GET /api/imoveis/{id}` - Obter imóvel específico
- `PUT /api/imoveis/{id}` - Atualizar imóvel
- `DELETE /api/imoveis/{id}` - Remover imóvel
- `POST /api/imoveis/{id}/fotos` - Adicionar foto

### Contratos
- `GET /api/contratos` - Listar contratos
- `POST /api/contratos` - Criar contrato

### Dashboard
- `GET /api/dashboard` - Dados do dashboard

## 🎨 Interface

A interface foi desenvolvida com foco na usabilidade e design moderno:

- **Dashboard intuitivo** com métricas importantes
- **Listagem de imóveis** com filtros e busca
- **Formulários responsivos** para cadastro
- **Design mobile-first** compatível com todos os dispositivos
- **Tema claro** com cores profissionais

## 🔒 Segurança

- Validação de dados no backend
- Sanitização de inputs
- CORS configurado adequadamente
- Soft delete para preservar histórico

## 📊 Banco de Dados

### Tabelas Principais

**imoveis**
- Informações completas do imóvel
- Localização e características
- Valores de venda/aluguel
- Status e metadados

**contratos**
- Dados do cliente
- Tipo de contrato (aluguel/venda)
- Datas e valores
- Relacionamento com imóvel

**fotos_imoveis**
- URLs das fotos
- Ordem e descrição
- Foto principal

## 🚀 Próximos Passos

- [ ] Sistema de autenticação
- [ ] Upload de fotos direto na aplicação
- [ ] Relatórios em PDF
- [ ] Notificações de vencimento
- [ ] API para integração com portais
- [ ] App mobile

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através do GitHub Issues.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido com ❤️ para facilitar a gestão de imóveis**

