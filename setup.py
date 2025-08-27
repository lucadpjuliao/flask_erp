#!/usr/bin/env python3
"""
Setup completo do CRM Profissional
Este script instala todas as dependências e inicializa o sistema
"""

import subprocess
import sys
import os
import importlib.util

def check_module(module_name, install_name=None):
    """Verifica se um módulo está instalado"""
    if install_name is None:
        install_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {module_name} não encontrado. Instalando {install_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            print(f"✅ {install_name} instalado com sucesso!")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao instalar {install_name}")
            return False
    else:
        print(f"✅ {module_name} já está instalado")
        return True

def install_dependencies():
    """Instala todas as dependências necessárias"""
    print("🔄 Verificando e instalando dependências...")
    
    dependencies = [
        ("flask", "Flask"),
        ("flask_sqlalchemy", "Flask-SQLAlchemy"),
        ("flask_migrate", "Flask-Migrate"),
        ("flask_login", "Flask-Login"),
        ("flask_wtf", "Flask-WTF"),
        ("flask_mail", "Flask-Mail"),
        ("wtforms", "WTForms"),
        ("werkzeug", "Werkzeug"),
        ("dotenv", "python-dotenv"),
        ("email_validator", "email-validator")
    ]
    
    all_success = True
    for module_name, install_name in dependencies:
        if not check_module(module_name, install_name):
            all_success = False
    
    return all_success

def initialize_database():
    """Inicializa o banco de dados"""
    print("🔄 Inicializando banco de dados...")
    try:
        # Import here to avoid circular imports
        from app import app
        from database import db
        from models import User, Team
        
        with app.app_context():
            print("Criando tabelas do banco de dados...")
            db.create_all()
            
            # Verificar se já existe usuário admin
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print("✅ Usuário administrador já existe!")
                return True
            
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
            
            db.session.commit()
            
            print("✅ Banco de dados inicializado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return False

def main():
    print("🚀 Setup do CRM Profissional")
    print("=" * 50)
    
    # Verificar Python
    print(f"✅ Python {sys.version.split()[0]} encontrado")
    
    # Atualizar pip
    print("🔄 Atualizando pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip atualizado!")
    except:
        print("⚠️ Não foi possível atualizar o pip, continuando...")
    
    # Instalar dependências
    if not install_dependencies():
        print("❌ Erro ao instalar dependências!")
        return False
    
    # Inicializar banco de dados
    if not initialize_database():
        print("❌ Erro ao inicializar banco de dados!")
        return False
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\n📋 Como usar:")
    print("1. Execute: python app.py")
    print("2. Acesse: http://localhost:5000")
    print("\n👤 Usuários padrão:")
    print("   Admin: admin / admin123")
    print("   Vendedor: vendedor1 / vendedor123")
    print("\n🚀 Pronto para usar!")

if __name__ == "__main__":
    main()