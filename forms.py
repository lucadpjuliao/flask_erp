from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, PasswordField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
from wtforms.widgets import TextArea
import re

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')

class UserForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Cargo', choices=[
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('vendedor', 'Vendedor')
    ], default='vendedor')
    team_id = SelectField('Equipe', coerce=int, validators=[Optional()])

def validate_cpf_cnpj(form, field):
    """Validação básica de CPF/CNPJ"""
    if field.data:
        # Remove caracteres especiais
        doc = re.sub(r'\D', '', field.data)
        
        if len(doc) == 11:  # CPF
            # Validação simples de CPF
            if doc == doc[0] * 11:  # Verifica se todos os dígitos são iguais
                raise ValidationError('CPF inválido')
        elif len(doc) == 14:  # CNPJ
            # Validação simples de CNPJ
            if doc == doc[0] * 14:  # Verifica se todos os dígitos são iguais
                raise ValidationError('CNPJ inválido')
        else:
            raise ValidationError('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos')

class ClientForm(FlaskForm):
    name = StringField('Nome/Razão Social', validators=[DataRequired(), Length(max=200)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    document = StringField('CPF/CNPJ', validators=[Optional(), validate_cpf_cnpj])
    document_type = SelectField('Tipo de Documento', choices=[
        ('', 'Selecione...'),
        ('CPF', 'CPF'),
        ('CNPJ', 'CNPJ')
    ], validators=[Optional()])
    address = StringField('Endereço', validators=[Optional(), Length(max=500)])
    city = StringField('Cidade', validators=[Optional(), Length(max=100)])
    state = StringField('Estado', validators=[Optional(), Length(max=50)])
    zip_code = StringField('CEP', validators=[Optional(), Length(max=10)])
    status = SelectField('Status', choices=[
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('prospecto', 'Prospecto')
    ], default='ativo')
    notes = TextAreaField('Observações', validators=[Optional()])

class LeadForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    value = DecimalField('Valor Estimado', validators=[Optional(), NumberRange(min=0)])
    status = SelectField('Status', choices=[
        ('novo', 'Novo'),
        ('qualificado', 'Qualificado'),
        ('proposta', 'Proposta Enviada'),
        ('negociacao', 'Em Negociação'),
        ('fechado', 'Fechado'),
        ('perdido', 'Perdido')
    ], default='novo')
    priority = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta')
    ], default='media')
    source = StringField('Origem', validators=[Optional(), Length(max=100)])
    expected_close_date = DateField('Data Esperada de Fechamento', validators=[Optional()])
    client_id = SelectField('Cliente', coerce=int, validators=[Optional()])
    user_id = SelectField('Responsável', coerce=int, validators=[DataRequired()])

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    due_date = DateTimeField('Data de Vencimento', validators=[Optional()], format='%Y-%m-%d %H:%M')
    status = SelectField('Status', choices=[
        ('pendente', 'Pendente'),
        ('em_progresso', 'Em Progresso'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada')
    ], default='pendente')
    priority = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta')
    ], default='media')
    user_id = SelectField('Responsável', coerce=int, validators=[DataRequired()])
    lead_id = SelectField('Lead Relacionado', coerce=int, validators=[Optional()])
    client_id = SelectField('Cliente Relacionado', coerce=int, validators=[Optional()])

class InteractionForm(FlaskForm):
    type = SelectField('Tipo', choices=[
        ('email', 'Email'),
        ('telefone', 'Telefone'),
        ('reuniao', 'Reunião'),
        ('visita', 'Visita'),
        ('outros', 'Outros')
    ], validators=[DataRequired()])
    subject = StringField('Assunto', validators=[Optional(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    date = DateTimeField('Data/Hora', validators=[Optional()], format='%Y-%m-%d %H:%M')
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    lead_id = SelectField('Lead Relacionado', coerce=int, validators=[Optional()])

class SearchForm(FlaskForm):
    query = StringField('Buscar', validators=[Optional()])
    status = SelectField('Status', choices=[('', 'Todos')], validators=[Optional()])
    user_id = SelectField('Responsável', choices=[('', 'Todos')], coerce=int, validators=[Optional()])
    date_from = DateField('Data Inicial', validators=[Optional()])
    date_to = DateField('Data Final', validators=[Optional()])