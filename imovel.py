from src.models.user import db
from datetime import datetime
from enum import Enum

class TipoImovel(Enum):
    CASA = "casa"
    APARTAMENTO = "apartamento"
    TERRENO = "terreno"
    COMERCIAL = "comercial"
    RURAL = "rural"

class StatusImovel(Enum):
    DISPONIVEL = "disponivel"
    ALUGADO = "alugado"
    VENDIDO = "vendido"
    MANUTENCAO = "manutencao"
    RESERVADO = "reservado"

class Imovel(db.Model):
    __tablename__ = 'imoveis'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.Enum(TipoImovel), nullable=False)
    status = db.Column(db.Enum(StatusImovel), nullable=False, default=StatusImovel.DISPONIVEL)
    
    # Localização
    endereco = db.Column(db.String(300), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(10))
    bairro = db.Column(db.String(100))
    
    # Características
    area_total = db.Column(db.Float)  # em m²
    area_construida = db.Column(db.Float)  # em m²
    quartos = db.Column(db.Integer)
    banheiros = db.Column(db.Integer)
    vagas_garagem = db.Column(db.Integer)
    
    # Valores
    valor_venda = db.Column(db.Float)
    valor_aluguel = db.Column(db.Float)
    valor_condominio = db.Column(db.Float)
    valor_iptu = db.Column(db.Float)
    
    # Informações adicionais
    mobiliado = db.Column(db.Boolean, default=False)
    aceita_pets = db.Column(db.Boolean, default=False)
    tem_piscina = db.Column(db.Boolean, default=False)
    tem_churrasqueira = db.Column(db.Boolean, default=False)
    tem_elevador = db.Column(db.Boolean, default=False)
    
    # Metadados
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    contratos = db.relationship('Contrato', backref='imovel', lazy=True)
    fotos = db.relationship('FotoImovel', backref='imovel', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Imovel {self.titulo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'tipo': self.tipo.value if self.tipo else None,
            'status': self.status.value if self.status else None,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'bairro': self.bairro,
            'area_total': self.area_total,
            'area_construida': self.area_construida,
            'quartos': self.quartos,
            'banheiros': self.banheiros,
            'vagas_garagem': self.vagas_garagem,
            'valor_venda': self.valor_venda,
            'valor_aluguel': self.valor_aluguel,
            'valor_condominio': self.valor_condominio,
            'valor_iptu': self.valor_iptu,
            'mobiliado': self.mobiliado,
            'aceita_pets': self.aceita_pets,
            'tem_piscina': self.tem_piscina,
            'tem_churrasqueira': self.tem_churrasqueira,
            'tem_elevador': self.tem_elevador,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'ativo': self.ativo,
            'fotos': [foto.to_dict() for foto in self.fotos]
        }

class FotoImovel(db.Model):
    __tablename__ = 'fotos_imoveis'
    
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(200))
    principal = db.Column(db.Boolean, default=False)
    ordem = db.Column(db.Integer, default=0)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'descricao': self.descricao,
            'principal': self.principal,
            'ordem': self.ordem,
            'data_upload': self.data_upload.isoformat() if self.data_upload else None
        }

class Contrato(db.Model):
    __tablename__ = 'contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=False)
    
    # Dados do locatário/comprador
    nome_cliente = db.Column(db.String(200), nullable=False)
    cpf_cliente = db.Column(db.String(14))
    telefone_cliente = db.Column(db.String(20))
    email_cliente = db.Column(db.String(120))
    
    # Dados do contrato
    tipo_contrato = db.Column(db.String(20), nullable=False)  # 'aluguel' ou 'venda'
    valor = db.Column(db.Float, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)  # Para aluguéis
    data_vencimento = db.Column(db.Integer)  # Dia do mês para vencimento do aluguel
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Contrato {self.nome_cliente} - {self.tipo_contrato}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'imovel_id': self.imovel_id,
            'nome_cliente': self.nome_cliente,
            'cpf_cliente': self.cpf_cliente,
            'telefone_cliente': self.telefone_cliente,
            'email_cliente': self.email_cliente,
            'tipo_contrato': self.tipo_contrato,
            'valor': self.valor,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'data_vencimento': self.data_vencimento,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'observacoes': self.observacoes
        }

