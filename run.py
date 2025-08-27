#!/usr/bin/env python3
"""
Script para executar o CRM Profissional
"""

import sys
import os

def main():
    print("🚀 Iniciando CRM Profissional...")
    
    try:
        # Verificar se o banco de dados existe
        if not os.path.exists('crm.db'):
            print("⚠️ Banco de dados não encontrado!")
            print("Execute primeiro: python setup.py")
            return
        
        # Importar e executar a aplicação
        from app import app
        
        print("✅ CRM Profissional iniciado!")
        print("📱 Acesse: http://localhost:5000")
        print("👤 Admin: admin / admin123")
        print("👤 Vendedor: vendedor1 / vendedor123")
        print("\n🛑 Para parar: Ctrl+C")
        print("-" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Execute primeiro: python setup.py")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

if __name__ == "__main__":
    main()