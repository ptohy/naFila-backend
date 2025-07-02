from flask import Blueprint, jsonify, request
from models import Conteudo, db
from flasgger import swag_from

bp = Blueprint('api', __name__)

# Listar conteúdos
@bp.route('/listar', methods=['GET'])
@swag_from({'tags': ['Conteúdos']})
def listar():
    """Lista todos os conteúdos ordenados."""
    conteudos = Conteudo.query.order_by(Conteudo.ordem).all()
    return jsonify([c.to_dict() for c in conteudos])


# Cadastrar conteúdo
@bp.route('/cadastrar', methods=['POST'])
@swag_from({'tags': ['Conteúdos']})
def cadastrar():
    """Cadastra um novo conteúdo."""
    data = request.get_json()

    max_ordem = db.session.query(db.func.max(Conteudo.ordem)).scalar() or 0

    novo = Conteudo(
        titulo=data.get('titulo'),
        tipo=data.get('tipo'),
        link=data.get('link'),
        status='Pendente',
        ordem=max_ordem + 1
    )
    db.session.add(novo)
    db.session.commit()

    return jsonify({'mensagem': 'Conteúdo cadastrado com sucesso.'}), 201

# Deletar conteúdo
@bp.route('/deletar/<int:id>', methods=['DELETE'])
@swag_from({'tags': ['Conteúdos']})
def deletar(id):
    """Deleta um conteúdo."""
    c = Conteudo.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()

    return jsonify({'mensagem': 'Conteúdo deletado com sucesso'})

# Atualizar status
@bp.route('/atualizar_status/<int:id>', methods=['PUT'])
@swag_from({'tags': ['Conteúdos']})
def atualizar_status(id):
    """Atualiza o status de um conteúdo (Ex: Concluído)."""
    c = Conteudo.query.get_or_404(id)
    data = request.get_json()
    c.status = data.get('status', c.status)
    db.session.commit()

    return jsonify({'mensagem': 'Status atualizado com sucesso.'})

# Reordenar conteúdos
@bp.route('/reordenar', methods=['POST'])
@swag_from({'tags': ['Conteúdos']})
def reordenar():
    """Atualiza a ordem dos conteúdos."""
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

# Pesquisar conteúdos
@bp.route('/pesquisar', methods=['GET'])
@swag_from({'tags': ['Conteúdos']})
def pesquisar():
    """Busca conteúdos por título."""
    query = request.args.get('q', '')
    if not query:
        return listar()

    conteudos = Conteudo.query.filter(
        Conteudo.titulo.ilike(f'%{query}%')
    ).order_by(Conteudo.ordem).all()

    return jsonify([c.to_dict() for c in conteudos])
