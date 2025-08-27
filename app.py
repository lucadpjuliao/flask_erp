from flask import Flask
import os
from dotenv import load_dotenv
from database import db, migrate, login_manager, mail

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crm.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    mail.init_app(app)
    
    # Import models and routes after app creation
    from models import User
    from routes import register_routes
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register routes
    register_routes(app)
    
    return app

def create_default_users():
    """Cria usuários padrão se não existirem"""
    from models import User, Team
    
    try:
        # Verificar se já existe usuário admin
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("✅ Usuário admin já existe")
            return
        
        print("🔄 Criando usuários padrão...")
        
        # Criar equipe padrão se não existir
        default_team = Team.query.filter_by(name='Equipe Geral').first()
        if not default_team:
            default_team = Team(
                name='Equipe Geral',
                description='Equipe padrão do sistema'
            )
            db.session.add(default_team)
            db.session.flush()
        
        # Criar usuário administrador
        admin_user = User(
            username='admin',
            email='admin@crm.com',
            first_name='Administrador',
            last_name='Sistema',
            role='admin',
            active=True,
            team_id=default_team.id
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Criar usuário vendedor de exemplo
        seller_exists = User.query.filter_by(username='vendedor1').first()
        if not seller_exists:
            seller_user = User(
                username='vendedor1',
                email='vendedor@crm.com',
                first_name='João',
                last_name='Silva',
                role='vendedor',
                active=True,
                team_id=default_team.id
            )
            seller_user.set_password('vendedor123')
            db.session.add(seller_user)
        
        db.session.commit()
        print("✅ Usuários padrão criados:")
        print("   👤 Admin: admin / admin123")
        print("   👤 Vendedor: vendedor1 / vendedor123")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários padrão: {e}")
        db.session.rollback()

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        print("🔄 Inicializando banco de dados...")
        db.create_all()
        print("✅ Tabelas criadas!")
        
        # Criar usuários padrão automaticamente
        create_default_users()
        
        print("🚀 Iniciando servidor...")
        print("📱 Acesse: http://localhost:5000")
        print("👤 Login: admin / admin123")
        print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)