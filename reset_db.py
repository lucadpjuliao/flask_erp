#!/usr/bin/env python3
"""
Script para resetar o banco de dados e recriar usuários padrão
"""

import os
import sys

def reset_database():
    """Remove o banco existente e recria tudo"""
    print("🔄 Resetando banco de dados...")
    
    try:
        # Remover banco existente se existir
        if os.path.exists('crm.db'):
            os.remove('crm.db')
            print("✅ Banco de dados antigo removido")
        
        # Importar aplicação
        from app import app
        from database import db
        from models import User, Team
        
        with app.app_context():
            print("🔄 Criando novas tabelas...")
            db.create_all()
            print("✅ Tabelas criadas!")
            
            print("🔄 Criando usuários padrão...")
            
            # Criar equipe padrão
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
            
            # Criar usuário vendedor
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
            
            print("✅ Usuários criados com sucesso!")
            print("👤 Admin: admin / admin123")
            print("👤 Vendedor: vendedor1 / vendedor123")
            print("\n🚀 Banco resetado! Execute: python app.py")
            
    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🗄️ Reset do Banco de Dados - CRM Profissional")
    print("=" * 50)
    
    confirm = input("⚠️ Isso vai apagar todos os dados! Continuar? (s/N): ")
    if confirm.lower() in ['s', 'sim', 'y', 'yes']:
        reset_database()
    else:
        print("❌ Operação cancelada")