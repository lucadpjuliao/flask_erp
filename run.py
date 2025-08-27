#!/usr/bin/env python3
"""
Script para executar o CRM Profissional
"""

import sys
import os

def create_default_users_if_needed():
    """Cria usuários padrão se necessário"""
    try:
        from app import app
        from database import db
        from models import User, Team
        
        with app.app_context():
            # Verificar se admin existe
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                return True
            
            print("🔄 Criando usuário admin automaticamente...")
            
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
            db.session.commit()
            
            print("✅ Usuário admin criado: admin / admin123")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        return False

def main():
    print("🚀 Iniciando CRM Profissional...")
    
    try:
        # Importar a aplicação
        from app import app
        from database import db
        
        # Inicializar banco e criar usuários se necessário
        with app.app_context():
            print("🔄 Verificando banco de dados...")
            db.create_all()
            create_default_users_if_needed()
        
        print("✅ CRM Profissional iniciado!")
        print("📱 Acesse: http://localhost:5000")
        print("👤 Login: admin / admin123")
        print("\n🛑 Para parar: Ctrl+C")
        print("-" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Instale as dependências: pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Mail WTForms python-dotenv email-validator")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

if __name__ == "__main__":
    main()