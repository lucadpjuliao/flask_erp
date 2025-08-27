# 🚀 CRM Profissional

Sistema completo de gestão de relacionamento com clientes desenvolvido em Flask.

## ⚡ Instalação Rápida

### Opção 1: Setup Automático (Recomendado)
```bash
# 1. Clone o repositório
git clone https://github.com/lucadpjuliao/flask_erp.git
cd flask_erp

# 2. Execute o setup automático
python setup.py

# 3. Execute a aplicação
python run.py
```

### Opção 2: Instalação Manual
```bash
# 1. Instalar dependências
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Flask-WTF Flask-Mail WTForms Werkzeug python-dotenv email-validator

# 2. Inicializar banco
python init_db.py

# 3. Executar aplicação
python app.py
```

## 🌐 Acesso ao Sistema

- **URL:** http://localhost:5000
- **👤 ADMIN:** `admin` / `admin123`
- **👤 Vendedor:** `vendedor1` / `vendedor123`

> ⚠️ **IMPORTANTE:** Os usuários são criados automaticamente na primeira execução!

## 🔧 Tecnologias

- **Backend:** Flask, SQLAlchemy
- **Frontend:** Bootstrap 5, JavaScript
- **Banco:** SQLite (desenvolvimento)
- **Autenticação:** Flask-Login

## 🛠️ Solução de Problemas

### ❌ "Usuário ou senha inválidos"
```bash
# O usuário admin é criado automaticamente, mas se houver problemas:
python reset_db.py  # Reseta o banco e recria usuários
```

### ❌ "ModuleNotFoundError"
```bash
# Instale as dependências:
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Mail WTForms python-dotenv email-validator
```

### ❌ Banco de dados corrompido
```bash
# Delete o arquivo crm.db e execute novamente:
rm crm.db  # Linux/Mac
del crm.db  # Windows
python app.py
```

## ✅ Funcionalidades Implementadas

### 👤 Gestão de Usuários e Equipes
- ✅ Cadastro, login e logout com autenticação segura
- ✅ Permissões por cargo (admin, gerente, vendedor)
- ✅ Sistema de equipes

### 🧑‍💼 Gestão de Clientes
- ✅ Cadastro completo de clientes (CPF/CNPJ, endereço, contatos, status)
- ✅ Busca avançada com filtros por nome, email, documento, status
- ✅ Validação de CPF/CNPJ
- ✅ Interface responsiva e intuitiva

### 📇 Leads & Oportunidades
- ✅ Cadastro e qualificação de leads
- ✅ Pipeline visual com estágios
- ✅ Atribuição de leads por usuário
- ✅ Vinculação com clientes

### 📆 Tarefas & Compromissos
- ✅ Cadastro de tarefas com prioridades
- ✅ Vínculo entre tarefas, leads e clientes
- ✅ Sistema de status (pendente, em progresso, concluída)

### 📊 Dashboard
- ✅ Métricas principais (clientes, leads, tarefas)
- ✅ Gráficos interativos
- ✅ Visão geral do pipeline
- ✅ Tarefas próximas do vencimento

### 🎨 Interface
- ✅ Design moderno com Bootstrap 5
- ✅ Responsivo para mobile e desktop
- ✅ Sidebar de navegação intuitiva
- ✅ Feedback visual para ações do usuário

## 📁 Estrutura do Projeto

```
crm-profissional/
├── app.py              # Aplicação principal Flask
├── models.py           # Modelos do banco de dados
├── routes.py           # Rotas e views da aplicação
├── forms.py            # Formulários WTForms
├── init_db.py          # Script de inicialização do banco
├── requirements.txt    # Dependências Python
├── .env.example        # Exemplo de variáveis de ambiente
├── templates/          # Templates HTML
│   ├── base.html       # Template base
│   ├── dashboard.html  # Dashboard principal
│   ├── login.html      # Página de login
│   └── clients/        # Templates de clientes
├── static/             # Arquivos estáticos (CSS, JS)
└── README.md          # Este arquivo
```

## 🔐 Segurança

- Senhas criptografadas com Werkzeug
- Proteção CSRF em todos os formulários
- Validação de dados no backend e frontend
- Controle de acesso baseado em roles
- Sessões seguras com Flask-Login

## 🧪 Validações Implementadas

### Backend (WTForms)
- ✅ Campos obrigatórios
- ✅ Validação de CPF/CNPJ
- ✅ E-mail válido e único
- ✅ Validação de formatos (telefone, CEP)

### Frontend (JavaScript + Bootstrap)
- ✅ Máscaras de input (telefone, CPF/CNPJ, CEP)
- ✅ Validação em tempo real
- ✅ Feedback visual (campos com erro em vermelho, sucesso em verde)

## 📈 Próximas Funcionalidades

- [ ] Sistema de relatórios avançados
- [ ] Exportação de dados (PDF/CSV)
- [ ] Integração com e-mail
- [ ] API RESTful
- [ ] Sistema de notificações
- [ ] Upload de documentos
- [ ] Calendário integrado

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte, envie um email para suporte@crm.com ou abra uma issue no GitHub.

---

Desenvolvido com ❤️ para facilitar a gestão de relacionamento com clientes.