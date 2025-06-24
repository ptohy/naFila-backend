from extensions import db

class Conteudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pendente")
    link = db.Column(db.String(200), nullable=True)
    ordem = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'status': self.status,
            'link': self.link,
            'ordem': self.ordem
        }