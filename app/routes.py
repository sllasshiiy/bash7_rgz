from flask import Blueprint, request, jsonify
from . import db
from .models import Subscription, User, AuditLog
from datetime import datetime
import logging

bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

def log_audit(user_id, action, table_name, record_id, old_values=None, new_values=None):
    """Helper function to log audit actions"""
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_values=old_values,
        new_values=new_values
    )
    db.session.add(audit_log)

@bp.route('/subscriptions', methods=['POST'])
def create_subscription():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'name', 'amount', 'periodicity', 'start_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            next_billing_date = start_date
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate periodicity
        if data['periodicity'] not in ['monthly', 'yearly', 'weekly']:
            return jsonify({'error': 'Invalid periodicity. Use: monthly, yearly, weekly'}), 400
        
        # Create subscription
        subscription = Subscription(
            user_id=data['user_id'],
            name=data['name'],
            amount=data['amount'],
            periodicity=data['periodicity'],
            start_date=start_date,
            next_billing_date=next_billing_date
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        # Log audit
        log_audit(
            user_id=data['user_id'],
            action='CREATE',
            table_name='subscriptions',
            record_id=subscription.id,
            new_values={
                'name': data['name'],
                'amount': float(data['amount']),
                'periodicity': data['periodicity'],
                'start_date': data['start_date']
            }
        )
        db.session.commit()
        
        return jsonify({
            'id': subscription.id,
            'message': 'Subscription created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating subscription: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<int:user_id>/subscriptions', methods=['GET'])
def get_subscriptions(user_id):
    try:
        subscriptions = Subscription.query.filter_by(
            user_id=user_id, 
            is_active=True
        ).all()
        
        result = []
        for sub in subscriptions:
            result.append({
                'id': sub.id,
                'name': sub.name,
                'amount': float(sub.amount),
                'periodicity': sub.periodicity,
                'start_date': sub.start_date.isoformat(),
                'next_billing_date': sub.next_billing_date.isoformat(),
                'created_at': sub.created_at.isoformat()
            })
        
        return jsonify({'subscriptions': result})
        
    except Exception as e:
        logger.error(f"Error fetching subscriptions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    try:
        data = request.get_json()
        subscription = Subscription.query.get_or_404(subscription_id)
        
        old_values = {
            'amount': float(subscription.amount),
            'periodicity': subscription.periodicity,
            'next_billing_date': subscription.next_billing_date.isoformat()
        }
        
        # Update fields if provided
        if 'amount' in data:
            subscription.amount = data['amount']
        if 'periodicity' in data:
            if data['periodicity'] not in ['monthly', 'yearly', 'weekly']:
                return jsonify({'error': 'Invalid periodicity'}), 400
            subscription.periodicity = data['periodicity']
        if 'next_billing_date' in data:
            try:
                subscription.next_billing_date = datetime.strptime(
                    data['next_billing_date'], '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        subscription.updated_at = datetime.utcnow()
        
        new_values = {
            'amount': float(subscription.amount),
            'periodicity': subscription.periodicity,
            'next_billing_date': subscription.next_billing_date.isoformat()
        }
        
        db.session.commit()
        
        # Log audit
        log_audit(
            user_id=subscription.user_id,
            action='UPDATE',
            table_name='subscriptions',
            record_id=subscription.id,
            old_values=old_values,
            new_values=new_values
        )
        db.session.commit()
        
        return jsonify({'message': 'Subscription updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating subscription: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    try:
        subscription = Subscription.query.get_or_404(subscription_id)
        
        old_values = {
            'name': subscription.name,
            'amount': float(subscription.amount),
            'periodicity': subscription.periodicity
        }
        
        user_id = subscription.user_id
        db.session.delete(subscription)
        db.session.commit()
        
        # Log audit
        log_audit(
            user_id=user_id,
            action='DELETE',
            table_name='subscriptions',
            record_id=subscription_id,
            old_values=old_values
        )
        db.session.commit()
        
        return jsonify({'message': 'Subscription deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting subscription: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
# Добавим тестовый корневой маршрут
@bp.route('/')
def index():
    return jsonify({
        'message': 'Financial Subscriptions API is running!',
        'endpoints': {
            'create_subscription': 'POST /subscriptions',
            'get_subscriptions': 'GET /users/<user_id>/subscriptions', 
            'update_subscription': 'PUT /subscriptions/<subscription_id>',
            'delete_subscription': 'DELETE /subscriptions/<subscription_id>'
        }
    })
