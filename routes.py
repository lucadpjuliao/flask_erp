from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta
from database import db
from models import User, Client, Lead, Task, Interaction, Team
from forms import LoginForm, ClientForm, LeadForm, TaskForm, InteractionForm, UserForm, SearchForm

def register_routes(app):
    @app.route('/')
    @login_required
    def dashboard():
        """Dashboard principal com métricas e resumos"""
        # Métricas básicas
        total_clients = Client.query.count()
        total_leads = Lead.query.count()
        active_leads = Lead.query.filter(Lead.status.in_(['novo', 'qualificado', 'proposta', 'negociacao'])).count()
        closed_leads = Lead.query.filter_by(status='fechado').count()
        pending_tasks = Task.query.filter_by(status='pendente').count()
        
        # Leads por status para o gráfico
        leads_by_status = db.session.query(Lead.status, func.count(Lead.id)).group_by(Lead.status).all()
        
        # Tarefas próximas do vencimento (próximos 7 dias)
        upcoming_tasks = Task.query.filter(
            Task.due_date >= datetime.now(),
            Task.due_date <= datetime.now() + timedelta(days=7),
            Task.status.in_(['pendente', 'em_progresso'])
        ).order_by(Task.due_date).limit(5).all()
        
        # Leads recentes
        recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()
        
        return render_template('dashboard.html',
                             total_clients=total_clients,
                             total_leads=total_leads,
                             active_leads=active_leads,
                             closed_leads=closed_leads,
                             pending_tasks=pending_tasks,
                             leads_by_status=leads_by_status,
                             upcoming_tasks=upcoming_tasks,
                             recent_leads=recent_leads)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Página de login"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                flash('Login realizado com sucesso!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            flash('Usuário ou senha inválidos', 'error')
        
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        """Logout do usuário"""
        logout_user()
        flash('Logout realizado com sucesso!', 'info')
        return redirect(url_for('login'))

    # CLIENTES
    @app.route('/clients')
    @login_required
    def clients():
        """Lista de clientes com busca e filtros"""
        search_form = SearchForm()
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        query = Client.query
        
        # Aplicar filtros de busca
        search_query = request.args.get('query', '').strip()
        if search_query:
            query = query.filter(or_(
                Client.name.contains(search_query),
                Client.email.contains(search_query),
                Client.document.contains(search_query)
            ))
        
        status_filter = request.args.get('status', '').strip()
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        clients = query.order_by(Client.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('clients/list.html', clients=clients, search_form=search_form)

    @app.route('/clients/new', methods=['GET', 'POST'])
    @login_required
    def new_client():
        """Criar novo cliente"""
        form = ClientForm()
        
        if form.validate_on_submit():
            client = Client(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                document=form.document.data,
                document_type=form.document_type.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zip_code=form.zip_code.data,
                status=form.status.data,
                notes=form.notes.data
            )
            
            db.session.add(client)
            db.session.commit()
            flash('Cliente criado com sucesso!', 'success')
            return redirect(url_for('clients'))
        
        return render_template('clients/form.html', form=form, title='Novo Cliente')

    @app.route('/clients/<int:id>')
    @login_required
    def view_client(id):
        """Visualizar detalhes do cliente"""
        client = Client.query.get_or_404(id)
        leads = client.leads.order_by(Lead.created_at.desc()).limit(10).all()
        interactions = client.interactions.order_by(Interaction.date.desc()).limit(10).all()
        tasks = client.tasks.order_by(Task.created_at.desc()).limit(10).all()
        
        return render_template('clients/view.html', 
                             client=client, 
                             leads=leads, 
                             interactions=interactions,
                             tasks=tasks)

    @app.route('/clients/<int:id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_client(id):
        """Editar cliente"""
        client = Client.query.get_or_404(id)
        form = ClientForm(obj=client)
        
        if form.validate_on_submit():
            form.populate_obj(client)
            client.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('view_client', id=client.id))
        
        return render_template('clients/form.html', form=form, title='Editar Cliente', client=client)

    # LEADS
    @app.route('/leads')
    @login_required
    def leads():
        """Lista de leads com pipeline visual"""
        search_form = SearchForm()
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        query = Lead.query
        
        # Aplicar filtros
        search_query = request.args.get('query', '').strip()
        if search_query:
            query = query.join(Client).filter(or_(
                Lead.title.contains(search_query),
                Client.name.contains(search_query)
            ))
        
        status_filter = request.args.get('status', '').strip()
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        user_filter = request.args.get('user_id', type=int)
        if user_filter:
            query = query.filter_by(user_id=user_filter)
        
        leads = query.order_by(Lead.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Dados para o pipeline
        pipeline_data = {}
        statuses = ['novo', 'qualificado', 'proposta', 'negociacao', 'fechado', 'perdido']
        for status in statuses:
            pipeline_data[status] = Lead.query.filter_by(status=status).all()
        
        users = User.query.filter_by(active=True).all()
        
        return render_template('leads/list.html', 
                             leads=leads, 
                             search_form=search_form,
                             pipeline_data=pipeline_data,
                             users=users)

    @app.route('/leads/new', methods=['GET', 'POST'])
    @login_required
    def new_lead():
        """Criar novo lead"""
        form = LeadForm()
        
        # Carregar opções para selects
        form.client_id.choices = [(0, 'Selecione...')] + [(c.id, c.name) for c in Client.query.all()]
        form.user_id.choices = [(u.id, f"{u.first_name} {u.last_name}") for u in User.query.filter_by(active=True).all()]
        
        if form.validate_on_submit():
            lead = Lead(
                title=form.title.data,
                description=form.description.data,
                value=form.value.data,
                status=form.status.data,
                priority=form.priority.data,
                source=form.source.data,
                expected_close_date=form.expected_close_date.data,
                client_id=form.client_id.data if form.client_id.data != 0 else None,
                user_id=form.user_id.data
            )
            
            db.session.add(lead)
            db.session.commit()
            flash('Lead criado com sucesso!', 'success')
            return redirect(url_for('leads'))
        
        return render_template('leads/form.html', form=form, title='Novo Lead')

    @app.route('/tasks')
    @login_required
    def tasks():
        """Lista de tarefas"""
        search_form = SearchForm()
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        query = Task.query
        
        # Aplicar filtros
        search_query = request.args.get('query', '').strip()
        if search_query:
            query = query.filter(Task.title.contains(search_query))
        
        status_filter = request.args.get('status', '').strip()
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        user_filter = request.args.get('user_id', type=int)
        if user_filter:
            query = query.filter_by(user_id=user_filter)
        
        tasks = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        users = User.query.filter_by(active=True).all()
        
        return render_template('tasks/list.html', tasks=tasks, search_form=search_form, users=users)

    # ERROR HANDLERS
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500