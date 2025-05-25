from flask import Flask, request, jsonify
from flask_cors import CORS
from tasks import process_task, get_task_status, celery_app, submit_task_with_priority
import os
from dotenv import load_dotenv
import logging
import traceback
from celery.result import AsyncResult

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure Flask to handle trailing slashes
app.url_map.strict_slashes = False

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Task Processing System API',
        'endpoints': {
            'submit_task': '/api/tasks (POST)',
            'get_task': '/api/tasks/<task_id> (GET)'
        }
    })

@app.route('/api/tasks', methods=['POST', 'OPTIONS'])
def submit_task():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        task_type = data.get('task_type')
        priority = data.get('priority', 'normal')
        parameters = data.get('parameters', {})
        delay = data.get('delay', 0)
        
        if not task_type:
            return jsonify({'error': 'task_type is required'}), 400
            
        if not isinstance(delay, (int, float)) or delay < 0:
            return jsonify({'error': 'delay must be a non-negative number'}), 400
            
        app.logger.info(f"Submitting task: type={task_type}, priority={priority}, parameters={parameters}, delay={delay}")
        
        # Submit task with priority-based routing
        task = submit_task_with_priority(
            task_type=task_type,
            priority=priority,
            parameters=parameters,
            delay=delay
        )
        
        app.logger.info(f"Task submitted successfully: {task.id}")
        return jsonify({
            'task_id': task.id,
            'status': 'pending',
            'message': f'Task submitted successfully. Will start in {delay} seconds.'
        }), 202
        
    except Exception as e:
        app.logger.error(f"Error submitting task: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET', 'OPTIONS'])
def get_task(task_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        status = get_task_status(task_id)
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': {
                'traceback': traceback.format_exc()
            }
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested URL was not found on the server',
        'path': request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'details': {
            'traceback': traceback.format_exc()
        }
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)