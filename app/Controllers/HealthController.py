"""
Health check controller for monitoring API status.
"""
from flask import current_app
from flask_restx import Namespace, Resource
from app.extensions import db
import time


health_ns = Namespace('health', description='Health check operations')


@health_ns.route('/')
class HealthCheck(Resource):
    """Health check endpoint."""
    
    @health_ns.doc('health_check')
    def get(self):
        """
        Check API health status.
        Returns service status, database connectivity, and timestamp.
        """
        health_status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'service': 'KitchenSync API',
            'version': current_app.config.get('API_VERSION', '1.0')
        }
        
        # Check database connectivity
        try:
            db.engine.connect()
            health_status['database'] = 'connected'
        except Exception as e:
            health_status['status'] = 'degraded'
            health_status['database'] = 'disconnected'
            health_status['database_error'] = str(e)
            current_app.logger.error(f"Database health check failed: {e}")
        
        # Return 503 if service is degraded
        status_code = 200 if health_status['status'] == 'healthy' else 503
        
        return health_status, status_code
