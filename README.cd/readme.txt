CRM Profissional em Flask

Um sistema CRM (Customer Relationship Management) completo, desenvolvido com Flask (Python) no back-end e um front-end moderno, responsivo e intuitivo. O sistema visa facilitar a gestão de clientes, leads, contatos, oportunidades de venda, tarefas e equipes de forma centralizada, segura e escalável.

🔧 Tecnologias Utilizadas

Back-End: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, Flask-Login, Flask-Mail

Banco de Dados: PostgreSQL (recomendado) ou SQLite (desenvolvimento)

Front-End: HTML5, CSS3, Bootstrap 5, JavaScript (AJAX, jQuery)

Autenticação: JWT ou Flask-Login com sessão segura

Validações: WTForms + validações personalizadas

Ambiente de Desenvolvimento: Docker (opcional), .env para variáveis sensíveis

✅ Funcionalidades do Sistema
👤 Gestão de Usuários e Equipes

Cadastro, login e logout com autenticação segura

Recuperação de senha via e-mail

Permissões por cargo (admin, gerente, vendedor, etc.)

CRUD de usuários

Associação de usuários a equipes

🧑‍💼 Gestão de Clientes

Cadastro completo de clientes (CPF/CNPJ, endereço, contatos, status)

Histórico de interações

Upload de documentos e contratos

Busca avançada com filtros por nome, cidade, status, etc.

📇 Leads & Oportunidades

Funil de vendas (pipeline visual com estágios)

Cadastro e qualificação de leads

Conversão de lead em cliente

Anotações e tarefas associadas a cada lead

Atribuição de leads por usuário ou equipe

📆 Tarefas & Compromissos

Calendário de atividades (com integração fullcalendar.js)

Alertas e notificações por e-mail

Vínculo entre tarefas, leads e clientes

📊 Relatórios e Dashboard

Dashboard com métricas principais (leads ativos, oportunidades, conversões, receita estimada)

Relatórios por período, por usuário, por status

Exportação em PDF/CSV

📩 Integrações (futuro)

Integração com e-mail (envio/recebimento por IMAP/SMTP)

Webhooks para integração com sistemas externos

API RESTful para integração com apps mobile ou sistemas terceiros

🧪 Validações
Backend (WTForms)

Campos obrigatórios

Validação de CPF/CNPJ

E-mail válido e único

Números de telefone com formatação

Datas válidas e coerentes (ex: data de fechamento posterior à de criação)

Restrições por permissão de usuário

Front-End (JS + Bootstrap)

Máscaras de input (telefone, CPF/CNPJ, datas)

Campos com validação em tempo real

Feedback visual (campos com erro em vermelho, sucesso em verde)