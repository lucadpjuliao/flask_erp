#!/bin/bash

echo "🚀 Instalador do CRM Profissional - Linux/Mac"
echo "=============================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado! Instale o Python3 primeiro."
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"

# Criar ambiente virtual (opcional)
read -p "🤔 Deseja criar um ambiente virtual? (s/n): " create_venv
if [[ $create_venv == "s" || $create_venv == "S" ]]; then
    echo "🔄 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado!"
fi

# Atualizar pip
echo "🔄 Atualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependências
echo "🔄 Instalando dependências..."
pip install Flask>=2.3.0
pip install Flask-SQLAlchemy>=3.0.0
pip install Flask-Migrate>=4.0.0
pip install Flask-Login>=0.6.0
pip install Flask-WTF>=1.1.0
pip install Flask-Mail>=0.9.0
pip install WTForms>=3.0.0
pip install Werkzeug>=2.3.0
pip install python-dotenv>=1.0.0
pip install email-validator>=2.0.0

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: python3 init_db.py"
echo "2. Execute: python3 app.py"
echo "3. Acesse: http://localhost:5000"
echo ""
echo "👤 Usuários padrão:"
echo "   Admin: admin / admin123"
echo "   Vendedor: vendedor1 / vendedor123"
echo ""