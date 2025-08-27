"""
Funções profissionais para gestão de leads
Sistema CRM Profissional
"""

from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
from database import db
from models import Lead, Client, User, Task, Interaction

class LeadManager:
    """Gerenciador profissional de leads com funcionalidades avançadas"""
    
    @staticmethod
    def create_lead_with_validation(data, user_id):
        """
        Cria um lead com validações profissionais
        """
        try:
            # Validar dados obrigatórios
            if not data.get('title') or not data.get('title').strip():
                return {'success': False, 'error': 'Título é obrigatório'}
            
            # Verificar se já existe lead similar
            existing = Lead.query.filter(
                and_(
                    Lead.title.ilike(f"%{data['title']}%"),
                    Lead.client_id == data.get('client_id') if data.get('client_id') else True
                )
            ).first()
            
            if existing:
                return {'success': False, 'error': 'Lead similar já existe'}
            
            # Criar lead
            lead = Lead(
                title=data['title'],
                description=data.get('description', ''),
                value=data.get('value'),
                status='novo',
                priority=data.get('priority', 'media'),
                source=data.get('source', ''),
                expected_close_date=data.get('expected_close_date'),
                client_id=data.get('client_id'),
                user_id=user_id
            )
            
            db.session.add(lead)
            db.session.commit()
            
            # Criar tarefa automática de follow-up
            LeadManager.create_followup_task(lead.id, user_id)
            
            return {'success': True, 'lead': lead, 'message': 'Lead criado com sucesso'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': f'Erro ao criar lead: {str(e)}'}
    
    @staticmethod
    def update_lead_status(lead_id, new_status, user_id, notes=None):
        """
        Atualiza status do lead com histórico
        """
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead não encontrado'}
            
            old_status = lead.status
            lead.status = new_status
            lead.updated_at = datetime.utcnow()
            
            # Registrar interação de mudança de status
            interaction = Interaction(
                type='sistema',
                subject=f'Status alterado: {old_status} → {new_status}',
                description=notes or f'Status do lead alterado de {old_status} para {new_status}',
                client_id=lead.client_id,
                lead_id=lead.id,
                user_id=user_id,
                date=datetime.utcnow()
            )
            
            db.session.add(interaction)
            
            # Criar tarefas automáticas baseadas no status
            if new_status == 'qualificado':
                LeadManager.create_qualification_tasks(lead_id, user_id)
            elif new_status == 'proposta':
                LeadManager.create_proposal_tasks(lead_id, user_id)
            elif new_status == 'negociacao':
                LeadManager.create_negotiation_tasks(lead_id, user_id)
            elif new_status == 'fechado':
                LeadManager.create_post_sale_tasks(lead_id, user_id)
            
            db.session.commit()
            
            return {'success': True, 'message': f'Status atualizado para {new_status}'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': f'Erro ao atualizar status: {str(e)}'}
    
    @staticmethod
    def create_followup_task(lead_id, user_id):
        """Cria tarefa automática de follow-up"""
        try:
            lead = Lead.query.get(lead_id)
            task = Task(
                title=f'Follow-up: {lead.title}',
                description=f'Fazer contato inicial com o lead {lead.title}',
                due_date=datetime.now() + timedelta(days=1),
                status='pendente',
                priority='alta',
                user_id=user_id,
                lead_id=lead_id,
                client_id=lead.client_id
            )
            db.session.add(task)
            return True
        except:
            return False
    
    @staticmethod
    def create_qualification_tasks(lead_id, user_id):
        """Cria tarefas para lead qualificado"""
        lead = Lead.query.get(lead_id)
        tasks = [
            {
                'title': f'Qualificar necessidades: {lead.title}',
                'description': 'Identificar necessidades específicas do cliente',
                'days': 2,
                'priority': 'alta'
            },
            {
                'title': f'Análise de orçamento: {lead.title}',
                'description': 'Verificar orçamento disponível do cliente',
                'days': 3,
                'priority': 'media'
            }
        ]
        
        for task_data in tasks:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                due_date=datetime.now() + timedelta(days=task_data['days']),
                status='pendente',
                priority=task_data['priority'],
                user_id=user_id,
                lead_id=lead_id,
                client_id=lead.client_id
            )
            db.session.add(task)
    
    @staticmethod
    def create_proposal_tasks(lead_id, user_id):
        """Cria tarefas para proposta"""
        lead = Lead.query.get(lead_id)
        tasks = [
            {
                'title': f'Elaborar proposta: {lead.title}',
                'description': 'Criar proposta comercial detalhada',
                'days': 3,
                'priority': 'alta'
            },
            {
                'title': f'Enviar proposta: {lead.title}',
                'description': 'Enviar proposta para o cliente',
                'days': 5,
                'priority': 'alta'
            },
            {
                'title': f'Follow-up proposta: {lead.title}',
                'description': 'Verificar se cliente recebeu e analisar proposta',
                'days': 7,
                'priority': 'media'
            }
        ]
        
        for task_data in tasks:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                due_date=datetime.now() + timedelta(days=task_data['days']),
                status='pendente',
                priority=task_data['priority'],
                user_id=user_id,
                lead_id=lead_id,
                client_id=lead.client_id
            )
            db.session.add(task)
    
    @staticmethod
    def create_negotiation_tasks(lead_id, user_id):
        """Cria tarefas para negociação"""
        lead = Lead.query.get(lead_id)
        task = Task(
            title=f'Negociar condições: {lead.title}',
            description='Negociar preços, prazos e condições comerciais',
            due_date=datetime.now() + timedelta(days=2),
            status='pendente',
            priority='alta',
            user_id=user_id,
            lead_id=lead_id,
            client_id=lead.client_id
        )
        db.session.add(task)
    
    @staticmethod
    def create_post_sale_tasks(lead_id, user_id):
        """Cria tarefas pós-venda"""
        lead = Lead.query.get(lead_id)
        tasks = [
            {
                'title': f'Onboarding cliente: {lead.title}',
                'description': 'Processo de integração do novo cliente',
                'days': 1,
                'priority': 'alta'
            },
            {
                'title': f'Follow-up satisfação: {lead.title}',
                'description': 'Verificar satisfação do cliente após fechamento',
                'days': 7,
                'priority': 'media'
            }
        ]
        
        for task_data in tasks:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                due_date=datetime.now() + timedelta(days=task_data['days']),
                status='pendente',
                priority=task_data['priority'],
                user_id=user_id,
                lead_id=lead_id,
                client_id=lead.client_id
            )
            db.session.add(task)
    
    @staticmethod
    def get_lead_analytics(user_id=None, period_days=30):
        """
        Retorna análises profissionais de leads
        """
        try:
            # Filtro de período
            date_filter = datetime.now() - timedelta(days=period_days)
            
            # Query base
            query = Lead.query.filter(Lead.created_at >= date_filter)
            if user_id:
                query = query.filter(Lead.user_id == user_id)
            
            # Métricas básicas
            total_leads = query.count()
            
            # Leads por status
            leads_by_status = db.session.query(
                Lead.status, 
                func.count(Lead.id).label('count')
            ).filter(Lead.created_at >= date_filter)
            
            if user_id:
                leads_by_status = leads_by_status.filter(Lead.user_id == user_id)
            
            leads_by_status = leads_by_status.group_by(Lead.status).all()
            
            # Taxa de conversão
            fechados = query.filter(Lead.status == 'fechado').count()
            perdidos = query.filter(Lead.status == 'perdido').count()
            conversion_rate = (fechados / total_leads * 100) if total_leads > 0 else 0
            loss_rate = (perdidos / total_leads * 100) if total_leads > 0 else 0
            
            # Valor total em negociação
            total_value = db.session.query(func.sum(Lead.value)).filter(
                Lead.created_at >= date_filter,
                Lead.status.in_(['novo', 'qualificado', 'proposta', 'negociacao'])
            )
            if user_id:
                total_value = total_value.filter(Lead.user_id == user_id)
            total_value = total_value.scalar() or 0
            
            # Valor fechado
            closed_value = db.session.query(func.sum(Lead.value)).filter(
                Lead.created_at >= date_filter,
                Lead.status == 'fechado'
            )
            if user_id:
                closed_value = closed_value.filter(Lead.user_id == user_id)
            closed_value = closed_value.scalar() or 0
            
            # Tempo médio de conversão
            avg_conversion_time = db.session.query(
                func.avg(func.julianday(Lead.updated_at) - func.julianday(Lead.created_at))
            ).filter(
                Lead.created_at >= date_filter,
                Lead.status == 'fechado'
            )
            if user_id:
                avg_conversion_time = avg_conversion_time.filter(Lead.user_id == user_id)
            avg_conversion_time = avg_conversion_time.scalar() or 0
            
            # Top performers
            top_users = db.session.query(
                User.first_name,
                User.last_name,
                func.count(Lead.id).label('leads_count'),
                func.sum(Lead.value).label('total_value')
            ).join(Lead).filter(
                Lead.created_at >= date_filter,
                Lead.status == 'fechado'
            ).group_by(User.id).order_by(func.sum(Lead.value).desc()).limit(5).all()
            
            return {
                'success': True,
                'analytics': {
                    'total_leads': total_leads,
                    'leads_by_status': {status: count for status, count in leads_by_status},
                    'conversion_rate': round(conversion_rate, 2),
                    'loss_rate': round(loss_rate, 2),
                    'total_value': float(total_value),
                    'closed_value': float(closed_value),
                    'avg_conversion_days': round(avg_conversion_time, 1),
                    'top_performers': [
                        {
                            'name': f"{user.first_name} {user.last_name}",
                            'leads': user.leads_count,
                            'value': float(user.total_value or 0)
                        } for user in top_users
                    ]
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Erro ao gerar analytics: {str(e)}'}
    
    @staticmethod
    def get_leads_by_priority(user_id=None):
        """Retorna leads ordenados por prioridade e urgência"""
        try:
            query = Lead.query.filter(
                Lead.status.in_(['novo', 'qualificado', 'proposta', 'negociacao'])
            )
            
            if user_id:
                query = query.filter(Lead.user_id == user_id)
            
            # Ordenar por prioridade e data de fechamento esperada
            leads = query.order_by(
                Lead.priority.desc(),
                Lead.expected_close_date.asc().nullslast(),
                Lead.created_at.desc()
            ).all()
            
            # Categorizar leads
            urgent = []
            important = []
            normal = []
            
            for lead in leads:
                if lead.expected_close_date and lead.expected_close_date <= datetime.now().date() + timedelta(days=7):
                    urgent.append(lead)
                elif lead.priority == 'alta':
                    important.append(lead)
                else:
                    normal.append(lead)
            
            return {
                'success': True,
                'leads': {
                    'urgent': urgent,
                    'important': important,
                    'normal': normal
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Erro ao buscar leads: {str(e)}'}
    
    @staticmethod
    def forecast_revenue(months=3):
        """Previsão de receita baseada em leads ativos"""
        try:
            end_date = datetime.now() + timedelta(days=months * 30)
            
            # Leads com data de fechamento esperada
            leads_with_date = Lead.query.filter(
                Lead.status.in_(['qualificado', 'proposta', 'negociacao']),
                Lead.expected_close_date.isnot(None),
                Lead.expected_close_date <= end_date.date(),
                Lead.value.isnot(None)
            ).all()
            
            # Probabilidades por status
            probabilities = {
                'qualificado': 0.3,
                'proposta': 0.6,
                'negociacao': 0.8
            }
            
            forecast = 0
            lead_details = []
            
            for lead in leads_with_date:
                probability = probabilities.get(lead.status, 0)
                expected_value = float(lead.value) * probability
                forecast += expected_value
                
                lead_details.append({
                    'title': lead.title,
                    'value': float(lead.value),
                    'status': lead.status,
                    'probability': probability,
                    'expected_value': expected_value,
                    'close_date': lead.expected_close_date.strftime('%d/%m/%Y')
                })
            
            return {
                'success': True,
                'forecast': {
                    'total_forecast': round(forecast, 2),
                    'period_months': months,
                    'leads_count': len(leads_with_date),
                    'details': lead_details
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Erro ao calcular previsão: {str(e)}'}
    
    @staticmethod
    def get_overdue_leads():
        """Retorna leads em atraso"""
        try:
            today = datetime.now().date()
            
            overdue_leads = Lead.query.filter(
                Lead.status.in_(['novo', 'qualificado', 'proposta', 'negociacao']),
                Lead.expected_close_date.isnot(None),
                Lead.expected_close_date < today
            ).order_by(Lead.expected_close_date.asc()).all()
            
            return {
                'success': True,
                'overdue_leads': [
                    {
                        'id': lead.id,
                        'title': lead.title,
                        'status': lead.status,
                        'value': float(lead.value) if lead.value else 0,
                        'expected_date': lead.expected_close_date.strftime('%d/%m/%Y'),
                        'days_overdue': (today - lead.expected_close_date).days,
                        'assigned_user': f"{lead.assigned_user.first_name} {lead.assigned_user.last_name}"
                    } for lead in overdue_leads
                ]
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Erro ao buscar leads em atraso: {str(e)}'}