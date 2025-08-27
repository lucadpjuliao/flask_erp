#!/usr/bin/env python3
"""
Script para inicializar o banco de dados e criar usuário administrador
"""

from app import app
from database import db
from models import User, Team
from werkzeug.security import generate_password_hash

def init_database():
    """Inicializa o banco de dados e cria dados iniciais"""
    
    with app.app_context():
        print("Criando tabelas do banco de dados...")
        db.create_all()
        
        # Verificar se já existe usuário admin
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("Usuário administrador já existe!")
            return
        
        # Criar equipe padrão
        default_team = Team(
            name='Equipe Geral',
            description='Equipe padrão do sistema'
        )
        db.session.add(default_team)
        db.session.flush()  # Para obter o ID
        
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
        
        # Commit das alterações
        db.session.commit()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print("\n📋 Usuários criados:")
        print("👤 Admin: admin / admin123")
        print("👤 Vendedor: vendedor1 / vendedor123")
        print("\n🚀 Execute: python app.py para iniciar o servidor")

if __name__ == '__main__':
    init_database()