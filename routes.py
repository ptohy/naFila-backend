# backend/routes.py

from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app import db
from models import Conteudo

bp = Blueprint('api', __name__)

@bp.route('/listar', methods=['GET'])
@swag_from({
    'tags': ['Conteúdos'],
    'summary': 'Lista todos os conteúdos ordenados.',
    'responses': {
        '200': {
            'description': 'Uma lista de todos os conteúdos.',
            'examples': {
                'application/json': [
                    {
                        "id": 1, "titulo": "Aprender Flask", "tipo": "Vídeo", 
                        "status": "Pendente", "link": "http://youtube.com/...", "ordem": 1
                    }
                ]
            }
        }
    }
})
def listar():
    """Lista todos os conteúdos ordenados."""
    conteudos = Conteudo.query.order_by(Conteudo.ordem).all()
    return jsonify([
        {'id': c.id, 'titulo': c.titulo, 'tipo': c.tipo, 'status': c.status, 'link': c.link, 'ordem': c.ordem}
        for c in conteudos
    ])

@bp.route('/cadastrar', methods=['POST'])
@swag_from({
    'tags': ['Conteúdos'],
    'summary': 'Adiciona um novo conteúdo à fila.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'id': 'ConteudoInput',
                'properties': {
                    'titulo': {'type': 'string', 'example': 'Meu Novo Artigo'},
                    'tipo': {'type': 'string', 'example': 'Artigo'},
                    'link': {'type': 'string', 'example': 'http://meusite.com/artigo'}
                }
            }
        }
    ],
    'responses': {
        '201': {'description': 'Conteúdo cadastrado com sucesso.'}
    }
})
def cadastrar():
    """Cadastra um novo conteúdo."""
    data = request.get_json()
    max_ordem = db.session.query(db.func.max(Conteudo.ordem)).scalar() or 0
    novo = Conteudo(
        titulo=data.get('titulo'), tipo=data.get('tipo'), link=data.get('link'),
        status='Pendente', ordem=max_ordem + 1
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Conteúdo cadastrado com sucesso.'}), 201

@bp.route('/deletar/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Conteúdos'],
    'summary': 'Deleta um conteúdo específico.',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'ID do conteúdo a ser deletado'}
    ],
    'responses': {
        '200': {'description': 'Conteúdo deletado com sucesso.'},
        '404': {'description': 'Conteúdo não encontrado.'}
    }
})
def deletar(id):
    """Deleta um conteúdo."""
    c = Conteudo.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'mensagem': 'Conteúdo deletado com sucesso'})

@bp.route('/atualizar_status/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Conteúdos'],
    'summary': 'Atualiza o status de um conteúdo (ex: para Concluído).',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'ID do conteúdo a ser atualizado'},
        {
            'in': 'body', 'name': 'body', 'required': True,
            'schema': {
                'properties': {'status': {'type': 'string', 'example': 'Concluído'}}
            }
        }
    ],
    'responses': {
        '200': {'description': 'Status atualizado com sucesso.'},
        '404': {'description': 'Conteúdo não encontrado.'}
    }
})
def atualizar_status(id):
    """Atualiza o status de um conteúdo (ex: para Concluído)."""
    c = Conteudo.query.get_or_404(id)
    data = request.get_json()
    c.status = data.get('status', c.status)
    db.session.commit()
    return jsonify({'mensagem': 'Status atualizado com sucesso.'})

@bp.route('/reordenar', methods=['POST'])
@swag_from({
    'tags': ['Conteúdos'],
    'summary': 'Recebe uma lista de IDs e atualiza a ordem de exibição.',
    'parameters': [
        {
            'in': 'body', 'name': 'body', 'required': True,
            'schema': {
                'properties': {
                    'order': {'type': 'array', 'items': {'type': 'integer'}, 'example': [3, 1, 2]}
                }
            }
        }
    ],
    'responses': {
        '200': {'description': 'Ordem atualizada com sucesso.'}
    }
})
def reordenar():
    """Recebe uma lista de IDs e atualiza a ordem."""
    data = request.get_json()
    id_order_list = data.get('order')
    if not id_order_list:
        return jsonify({'erro': 'Lista de ordem não fornecida'}), 400
    for index, item_id in enumerate(id_order_list):
        item = Conteudo.query.get(item_id)
        if item:
            item.ordem = index
    db.session.commit()
    return jsonify({'mensagem': 'Ordem atualizada com sucesso.'})

@bp.route('/pesquisar', methods=['GET'])
@swag_from({
    'tags': ['Conteúdos'],
    'summary': 'Busca conteúdos por título.',
    'parameters': [
        {'name': 'q', 'in': 'query', 'type': 'string', 'required': True, 'description': 'Termo a ser buscado no título'}
    ],
    'responses': {
        '200': {'description': 'Uma lista de conteúdos que correspondem à busca.'}
    }
})
def pesquisar():
    """Busca conteúdos por título."""
    query = request.args.get('q', '')
    if not query:
        return listar()
    conteudos = Conteudo.query.filter(Conteudo.titulo.ilike(f'%{query}%')).order_by(Conteudo.ordem).all()
    return jsonify([
        {'id': c.id, 'titulo': c.titulo, 'tipo': c.tipo, 'status': c.status, 'link': c.link, 'ordem': c.ordem}
        for c in conteudos
    ])
