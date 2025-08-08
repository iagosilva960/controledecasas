from flask import Blueprint, request, jsonify
from src.models.imovel import db, Imovel, FotoImovel, Contrato, TipoImovel, StatusImovel
from datetime import datetime, date
import json
import os

imoveis_bp = Blueprint('imoveis', __name__)

def trigger_backup():
    """Dispara backup para o GitHub após mudanças"""
    try:
        from src.main import backup_to_github
        backup_to_github()
    except Exception as e:
        print(f"Erro no backup automático: {e}")

@imoveis_bp.route('/imoveis', methods=['GET'])
def listar_imoveis():
    """Lista todos os imóveis com filtros opcionais"""
    try:
        # Parâmetros de filtro
        tipo = request.args.get('tipo')
        status = request.args.get('status')
        cidade = request.args.get('cidade')
        valor_min = request.args.get('valor_min', type=float)
        valor_max = request.args.get('valor_max', type=float)
        quartos_min = request.args.get('quartos_min', type=int)
        
        # Query base
        query = Imovel.query.filter_by(ativo=True)
        
        # Aplicar filtros
        if tipo:
            query = query.filter(Imovel.tipo == TipoImovel(tipo))
        if status:
            query = query.filter(Imovel.status == StatusImovel(status))
        if cidade:
            query = query.filter(Imovel.cidade.ilike(f'%{cidade}%'))
        if valor_min:
            query = query.filter(
                (Imovel.valor_venda >= valor_min) | 
                (Imovel.valor_aluguel >= valor_min)
            )
        if valor_max:
            query = query.filter(
                (Imovel.valor_venda <= valor_max) | 
                (Imovel.valor_aluguel <= valor_max)
            )
        if quartos_min:
            query = query.filter(Imovel.quartos >= quartos_min)
        
        imoveis = query.order_by(Imovel.data_cadastro.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [imovel.to_dict() for imovel in imoveis],
            'total': len(imoveis)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/imoveis', methods=['POST'])
def criar_imovel():
    """Cria um novo imóvel"""
    try:
        data = request.get_json()
        
        # Validações básicas
        if not data.get('titulo'):
            return jsonify({'success': False, 'error': 'Título é obrigatório'}), 400
        if not data.get('endereco'):
            return jsonify({'success': False, 'error': 'Endereço é obrigatório'}), 400
        if not data.get('cidade'):
            return jsonify({'success': False, 'error': 'Cidade é obrigatória'}), 400
        if not data.get('tipo'):
            return jsonify({'success': False, 'error': 'Tipo é obrigatório'}), 400
        
        # Criar novo imóvel
        imovel = Imovel(
            titulo=data['titulo'],
            descricao=data.get('descricao', ''),
            tipo=TipoImovel(data['tipo']),
            status=StatusImovel(data.get('status', 'disponivel')),
            endereco=data['endereco'],
            cidade=data['cidade'],
            estado=data.get('estado', ''),
            cep=data.get('cep'),
            bairro=data.get('bairro'),
            area_total=data.get('area_total'),
            area_construida=data.get('area_construida'),
            quartos=data.get('quartos'),
            banheiros=data.get('banheiros'),
            vagas_garagem=data.get('vagas_garagem'),
            valor_venda=data.get('valor_venda'),
            valor_aluguel=data.get('valor_aluguel'),
            valor_condominio=data.get('valor_condominio'),
            valor_iptu=data.get('valor_iptu'),
            mobiliado=data.get('mobiliado', False),
            aceita_pets=data.get('aceita_pets', False),
            tem_piscina=data.get('tem_piscina', False),
            tem_churrasqueira=data.get('tem_churrasqueira', False),
            tem_elevador=data.get('tem_elevador', False)
        )
        
        db.session.add(imovel)
        db.session.commit()
        
        # Adicionar fotos se fornecidas
        if data.get('fotos'):
            for i, foto_data in enumerate(data['fotos']):
                foto = FotoImovel(
                    imovel_id=imovel.id,
                    url=foto_data['url'],
                    descricao=foto_data.get('descricao', ''),
                    principal=foto_data.get('principal', i == 0),
                    ordem=i
                )
                db.session.add(foto)
            db.session.commit()
        
        # Fazer backup após criar imóvel
        trigger_backup()
        
        return jsonify({
            'success': True,
            'data': imovel.to_dict(),
            'message': 'Imóvel criado com sucesso'
        }), 201
    
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Valor inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/imoveis/<int:imovel_id>', methods=['GET'])
def obter_imovel(imovel_id):
    """Obtém um imóvel específico"""
    try:
        imovel = Imovel.query.filter_by(id=imovel_id, ativo=True).first()
        
        if not imovel:
            return jsonify({'success': False, 'error': 'Imóvel não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'data': imovel.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/imoveis/<int:imovel_id>', methods=['PUT'])
def atualizar_imovel(imovel_id):
    """Atualiza um imóvel existente"""
    try:
        imovel = Imovel.query.filter_by(id=imovel_id, ativo=True).first()
        
        if not imovel:
            return jsonify({'success': False, 'error': 'Imóvel não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos
        for field in ['titulo', 'descricao', 'endereco', 'cidade', 'estado', 'cep', 'bairro',
                     'area_total', 'area_construida', 'quartos', 'banheiros', 'vagas_garagem',
                     'valor_venda', 'valor_aluguel', 'valor_condominio', 'valor_iptu',
                     'mobiliado', 'aceita_pets', 'tem_piscina', 'tem_churrasqueira', 'tem_elevador']:
            if field in data:
                setattr(imovel, field, data[field])
        
        if 'tipo' in data:
            imovel.tipo = TipoImovel(data['tipo'])
        if 'status' in data:
            imovel.status = StatusImovel(data['status'])
        
        imovel.data_atualizacao = datetime.utcnow()
        
        db.session.commit()
        
        # Fazer backup após atualizar imóvel
        trigger_backup()
        
        return jsonify({
            'success': True,
            'data': imovel.to_dict(),
            'message': 'Imóvel atualizado com sucesso'
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Valor inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def deletar_imovel(imovel_id):
    """Deleta (desativa) um imóvel"""
    try:
        imovel = Imovel.query.filter_by(id=imovel_id, ativo=True).first()
        
        if not imovel:
            return jsonify({'success': False, 'error': 'Imóvel não encontrado'}), 404
        
        # Soft delete
        imovel.ativo = False
        imovel.data_atualizacao = datetime.utcnow()
        
        db.session.commit()
        
        # Fazer backup após deletar imóvel
        trigger_backup()
        
        return jsonify({
            'success': True,
            'message': 'Imóvel removido com sucesso'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/imoveis/<int:imovel_id>/fotos', methods=['POST'])
def adicionar_foto(imovel_id):
    """Adiciona uma foto ao imóvel"""
    try:
        imovel = Imovel.query.filter_by(id=imovel_id, ativo=True).first()
        
        if not imovel:
            return jsonify({'success': False, 'error': 'Imóvel não encontrado'}), 404
        
        data = request.get_json()
        
        if not data.get('url'):
            return jsonify({'success': False, 'error': 'URL da foto é obrigatória'}), 400
        
        # Determinar ordem
        ultima_foto = FotoImovel.query.filter_by(imovel_id=imovel_id).order_by(FotoImovel.ordem.desc()).first()
        ordem = (ultima_foto.ordem + 1) if ultima_foto else 0
        
        foto = FotoImovel(
            imovel_id=imovel_id,
            url=data['url'],
            descricao=data.get('descricao', ''),
            principal=data.get('principal', False),
            ordem=ordem
        )
        
        # Se esta foto é principal, remover principal das outras
        if foto.principal:
            FotoImovel.query.filter_by(imovel_id=imovel_id).update({'principal': False})
        
        db.session.add(foto)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': foto.to_dict(),
            'message': 'Foto adicionada com sucesso'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/contratos', methods=['GET'])
def listar_contratos():
    """Lista todos os contratos"""
    try:
        tipo = request.args.get('tipo')  # 'aluguel' ou 'venda'
        ativo = request.args.get('ativo', type=bool)
        
        query = Contrato.query
        
        if tipo:
            query = query.filter(Contrato.tipo_contrato == tipo)
        if ativo is not None:
            query = query.filter(Contrato.ativo == ativo)
        
        contratos = query.order_by(Contrato.data_cadastro.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [contrato.to_dict() for contrato in contratos],
            'total': len(contratos)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/contratos', methods=['POST'])
def criar_contrato():
    """Cria um novo contrato"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('imovel_id'):
            return jsonify({'success': False, 'error': 'ID do imóvel é obrigatório'}), 400
        if not data.get('nome_cliente'):
            return jsonify({'success': False, 'error': 'Nome do cliente é obrigatório'}), 400
        if not data.get('tipo_contrato'):
            return jsonify({'success': False, 'error': 'Tipo do contrato é obrigatório'}), 400
        if not data.get('valor'):
            return jsonify({'success': False, 'error': 'Valor é obrigatório'}), 400
        if not data.get('data_inicio'):
            return jsonify({'success': False, 'error': 'Data de início é obrigatória'}), 400
        
        # Verificar se o imóvel existe
        imovel = Imovel.query.filter_by(id=data['imovel_id'], ativo=True).first()
        if not imovel:
            return jsonify({'success': False, 'error': 'Imóvel não encontrado'}), 404
        
        # Criar contrato
        contrato = Contrato(
            imovel_id=data['imovel_id'],
            nome_cliente=data['nome_cliente'],
            cpf_cliente=data.get('cpf_cliente'),
            telefone_cliente=data.get('telefone_cliente'),
            email_cliente=data.get('email_cliente'),
            tipo_contrato=data['tipo_contrato'],
            valor=data['valor'],
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else None,
            data_vencimento=data.get('data_vencimento'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(contrato)
        
        # Atualizar status do imóvel
        if data['tipo_contrato'] == 'aluguel':
            imovel.status = StatusImovel.ALUGADO
        elif data['tipo_contrato'] == 'venda':
            imovel.status = StatusImovel.VENDIDO
        
        db.session.commit()
        
        # Fazer backup após criar contrato
        trigger_backup()
        
        return jsonify({
            'success': True,
            'data': contrato.to_dict(),
            'message': 'Contrato criado com sucesso'
        }), 201
    
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Formato de data inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@imoveis_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Retorna dados para o dashboard"""
    try:
        # Estatísticas gerais
        total_imoveis = Imovel.query.filter_by(ativo=True).count()
        imoveis_disponiveis = Imovel.query.filter_by(ativo=True, status=StatusImovel.DISPONIVEL).count()
        imoveis_alugados = Imovel.query.filter_by(ativo=True, status=StatusImovel.ALUGADO).count()
        imoveis_vendidos = Imovel.query.filter_by(ativo=True, status=StatusImovel.VENDIDO).count()
        
        # Contratos ativos
        contratos_aluguel_ativos = Contrato.query.filter_by(ativo=True, tipo_contrato='aluguel').count()
        contratos_venda_ativos = Contrato.query.filter_by(ativo=True, tipo_contrato='venda').count()
        
        # Receita mensal estimada (aluguéis)
        receita_mensal = db.session.query(db.func.sum(Contrato.valor)).filter_by(
            ativo=True, tipo_contrato='aluguel'
        ).scalar() or 0
        
        # Imóveis por tipo
        imoveis_por_tipo = {}
        for tipo in TipoImovel:
            count = Imovel.query.filter_by(ativo=True, tipo=tipo).count()
            imoveis_por_tipo[tipo.value] = count
        
        return jsonify({
            'success': True,
            'data': {
                'estatisticas_gerais': {
                    'total_imoveis': total_imoveis,
                    'imoveis_disponiveis': imoveis_disponiveis,
                    'imoveis_alugados': imoveis_alugados,
                    'imoveis_vendidos': imoveis_vendidos
                },
                'contratos': {
                    'aluguel_ativos': contratos_aluguel_ativos,
                    'venda_ativos': contratos_venda_ativos
                },
                'financeiro': {
                    'receita_mensal_estimada': receita_mensal
                },
                'imoveis_por_tipo': imoveis_por_tipo
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

