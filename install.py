#!/usr/bin/env python3
"""
Script de instalação automática do CRM Profissional
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}:")
        print(f"   {e.stderr}")
        return False

def main():
    print("🚀 Instalador do CRM Profissional")
    print("=" * 50)
    
    # Verificar se Python está instalado
    try:
        python_version = sys.version
        print(f"✅ Python encontrado: {python_version.split()[0]}")
    except:
        print("❌ Python não encontrado!")
        return False
    
    # Instalar dependências
    commands = [
        ("python -m pip install --upgrade pip", "Atualizando pip"),
        ("pip install Flask>=2.3.0", "Instalando Flask"),
        ("pip install Flask-SQLAlchemy>=3.0.0", "Instalando Flask-SQLAlchemy"),
        ("pip install Flask-Migrate>=4.0.0", "Instalando Flask-Migrate"),
        ("pip install Flask-Login>=0.6.0", "Instalando Flask-Login"),
        ("pip install Flask-WTF>=1.1.0", "Instalando Flask-WTF"),
        ("pip install Flask-Mail>=0.9.0", "Instalando Flask-Mail"),
        ("pip install WTForms>=3.0.0", "Instalando WTForms"),
        ("pip install Werkzeug>=2.3.0", "Instalando Werkzeug"),
        ("pip install python-dotenv>=1.0.0", "Instalando python-dotenv"),
        ("pip install email-validator>=2.0.0", "Instalando email-validator")
    ]
    
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
            break
    
    if success:
        print("\n🎉 Instalação concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Execute: python init_db.py")
        print("2. Execute: python app.py")
        print("3. Acesse: http://localhost:5000")
        print("\n👤 Usuários padrão:")
        print("   Admin: admin / admin123")
        print("   Vendedor: vendedor1 / vendedor123")
    else:
        print("\n❌ Erro durante a instalação!")
        print("Tente executar manualmente: pip install -r requirements.txt")

if __name__ == "__main__":
    main()