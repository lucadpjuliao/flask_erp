from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='vendedor')  # admin, gerente, vendedor
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    # Relationships
    team = db.relationship('Team', backref='members')
    leads = db.relationship('Lead', backref='assigned_user', lazy='dynamic')
    tasks = db.relationship('Task', backref='assigned_user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Team {self.name}>'

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    document = db.Column(db.String(20))  # CPF/CNPJ
    document_type = db.Column(db.String(10))  # CPF ou CNPJ
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    status = db.Column(db.String(20), default='ativo')  # ativo, inativo, prospecto
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leads = db.relationship('Lead', backref='client', lazy='dynamic')
    interactions = db.relationship('Interaction', backref='client', lazy='dynamic')
    
    def __repr__(self):
        return f'<Client {self.name}>'

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    value = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50), default='novo')  # novo, qualificado, proposta, negociacao, fechado, perdido
    priority = db.Column(db.String(20), default='media')  # baixa, media, alta
    source = db.Column(db.String(100))  # website, telefone, email, indicacao
    expected_close_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    tasks = db.relationship('Task', backref='lead', lazy='dynamic')
    interactions = db.relationship('Interaction', backref='lead', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lead {self.title}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pendente')  # pendente, em_progresso, concluida, cancelada
    priority = db.Column(db.String(20), default='media')  # baixa, media, alta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    
    # Relationships
    client = db.relationship('Client', backref='tasks')
    
    def __repr__(self):
        return f'<Task {self.title}>'

class Interaction(db.Model):
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # email, telefone, reuniao, visita
    subject = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    user = db.relationship('User', backref='interactions')
    
    def __repr__(self):
        return f'<Interaction {self.type}: {self.subject}>'