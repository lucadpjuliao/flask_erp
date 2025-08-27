# CRM Profissional

Um sistema CRM (Customer Relationship Management) completo, desenvolvido com Flask (Python) no back-end e um front-end moderno, responsivo e intuitivo. O sistema visa facilitar a gestão de clientes, leads, contatos, oportunidades de venda, tarefas e equipes de forma centralizada, segura e escalável.

## 🔧 Tecnologias Utilizadas

- **Back-End:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, Flask-Login, Flask-Mail
- **Banco de Dados:** PostgreSQL (recomendado) ou SQLite (desenvolvimento)
- **Front-End:** HTML5, CSS3, Bootstrap 5, JavaScript (AJAX, jQuery)
- **Autenticação:** Flask-Login com sessão segura
- **Validações:** WTForms + validações personalizadas

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd crm-profissional
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Inicialize o banco de dados
```bash
python init_db.py
```

### 6. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 👤 Usuários Padrão

Após a inicialização do banco de dados, os seguintes usuários estarão disponíveis:

- **Administrador:** admin / admin123
- **Vendedor:** vendedor1 / vendedor123

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