@echo off
echo 🚀 Instalador do CRM Profissional - Windows
echo ================================================

echo 🔄 Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

echo 🔄 Atualizando pip...
python -m pip install --upgrade pip

echo 🔄 Instalando dependências...
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

echo.
echo 🎉 Instalação concluída!
echo.
echo 📋 Próximos passos:
echo 1. Execute: python init_db.py
echo 2. Execute: python app.py  
echo 3. Acesse: http://localhost:5000
echo.
echo 👤 Usuários padrão:
echo    Admin: admin / admin123
echo    Vendedor: vendedor1 / vendedor123
echo.
pause