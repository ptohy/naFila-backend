from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from extensions import db


def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'naFila API',
        'uiversion': 3
    }

    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    Swagger(app)

    # Importar os modelos e criar o banco
    with app.app_context():
        from models import Conteudo
        db.create_all()

    # Registrar as rotas
    from routes import bp
    app.register_blueprint(bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)