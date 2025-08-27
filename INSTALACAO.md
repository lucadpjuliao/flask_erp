# 🚀 Guia de Instalação - CRM Profissional

## 📋 Pré-requisitos

- **Python 3.8+** instalado no sistema
- **pip** (gerenciador de pacotes Python)

## 🔧 Instalação Automática

### Windows
```bash
# Execute o instalador automático
install.bat
```

### Linux/Mac
```bash
# Torne o script executável e execute
chmod +x install.sh
./install.sh
```

### Qualquer Sistema
```bash
# Usando Python
python install.py
```

## 🛠️ Instalação Manual

### 1. Instalar Dependências
```bash
# Opção 1: Usando requirements.txt
pip install -r requirements.txt

# Opção 2: Instalação individual
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
```

### 2. Inicializar Banco de Dados
```bash
python init_db.py
```

### 3. Executar Aplicação
```bash
python app.py
```

### 4. Acessar Sistema
- **URL:** http://localhost:5000
- **Admin:** admin / admin123
- **Vendedor:** vendedor1 / vendedor123

## 🐍 Ambiente Virtual (Recomendado)

### Criar ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Instalar dependências no ambiente virtual
```bash
pip install -r requirements.txt
```

## ❌ Solucionando Problemas

### Erro: "ModuleNotFoundError: No module named 'flask_mail'"
```bash
# Solução
pip install Flask-Mail
```

### Erro: "Python não encontrado"
1. Instale Python do site oficial: https://python.org
2. Adicione Python ao PATH do sistema
3. Reinicie o terminal

### Erro: "pip não encontrado"
```bash
# Windows
python -m ensurepip --upgrade

# Linux/Mac
sudo apt install python3-pip  # Ubuntu/Debian
brew install python           # Mac
```

### Erro: "Permission denied"
```bash
# Linux/Mac - Use sudo se necessário
sudo pip install -r requirements.txt

# Ou use --user
pip install --user -r requirements.txt
```

## 🔍 Verificar Instalação

### Testar importações
```python
python -c "import flask, flask_sqlalchemy, flask_login; print('✅ Dependências OK')"
```

### Verificar versões
```bash
python --version
pip --version
```

## 📞 Suporte

Se encontrar problemas:

1. Verifique se Python 3.8+ está instalado
2. Atualize pip: `pip install --upgrade pip`
3. Use ambiente virtual
4. Execute os scripts de instalação automática

## 🎯 Estrutura Final

Após instalação bem-sucedida:
```
flask_erp/
├── app.py              ✅ Aplicação principal
├── init_db.py          ✅ Inicializador do banco
├── requirements.txt    ✅ Dependências
├── install.py          ✅ Instalador Python
├── install.bat         ✅ Instalador Windows
├── install.sh          ✅ Instalador Linux/Mac
└── crm.db             ✅ Banco de dados (após init_db.py)
```

## 🚀 Início Rápido

```bash
# 1. Clone o repositório
git clone https://github.com/lucadpjuliao/flask_erp.git
cd flask_erp

# 2. Execute instalador automático
python install.py

# 3. Inicialize banco
python init_db.py

# 4. Execute aplicação
python app.py

# 5. Acesse http://localhost:5000
```