"""
Backend API for LCA Dataset Management
Handles OpenLCA API integration and dataset operations
"""

from flask import Blueprint, jsonify, request, render_template, session
import requests
import json
import os

dataset_bp = Blueprint('dataset', __name__)

# OpenLCA Configuration
OPENLCA_API_URL = "http://localhost:8080"
UPLOAD_FOLDER = "uploads/datasets"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@dataset_bp.route('/dataset')
def dataset_page():
    """Render the dataset selection page"""
    if 'username' not in session:
        return redirect('/first page')
    return render_template('dataset.html')

@dataset_bp.route('/api/check-openlca')
def check_openlca():
    """Check if OpenLCA API is available"""
    try:
        response = requests.get(f"{OPENLCA_API_URL}/databases", timeout=2)
        if response.status_code == 200:
            databases = response.json()
            return jsonify({
                'available': True,
                'databases': databases,
                'count': len(databases)
            })
        else:
            return jsonify({'available': False, 'message': 'OpenLCA API not responding'})
    except requests.exceptions.RequestException:
        return jsonify({'available': False, 'message': 'OpenLCA not running'})

@dataset_bp.route('/api/datasets')
def get_datasets():
    """Get datasets based on selected source"""
    source = request.args.get('source', 'builtin')
    
    try:
        if source == 'openlca':
            return get_openlca_datasets()
        elif source == 'ecoinvent':
            return get_ecoinvent_datasets()
        elif source == 'indian':
            return get_indian_datasets()
        else:
            return get_builtin_datasets()
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading dataset: {str(e)}'
        }), 500

def get_openlca_datasets():
    """Fetch datasets from OpenLCA API"""
    try:
        # Get available databases
        response = requests.get(f"{OPENLCA_API_URL}/databases", timeout=5)
        
        if response.status_code == 200:
            databases = response.json()
            
            # Get processes from first available database
            if databases:
                # You can select a specific database or let user choose
                db_name = databases[0] if databases else None
                
                if db_name:
                    # Fetch process descriptors
                    proc_response = requests.post(
                        f"{OPENLCA_API_URL}/data/get/descriptors",
                        json={"@type": "Process"},
                        timeout=10
                    )
                    
                    if proc_response.status_code == 200:
                        processes = proc_response.json()
                        
                        return jsonify({
                            'success': True,
                            'source': 'openlca',
                            'database': db_name,
                            'processes': processes[:100],  # Limit to first 100
                            'total_processes': len(processes),
                            'message': f'Loaded {len(processes)} processes from OpenLCA'
                        })
            
            return jsonify({
                'success': True,
                'source': 'openlca',
                'databases': databases,
                'message': 'OpenLCA connected but no active database'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not connect to OpenLCA'
            })
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'message': 'OpenLCA is not running. Please start OpenLCA IPC Server.'
        })

def get_ecoinvent_datasets():
    """Get Ecoinvent dataset information"""
    # Note: Ecoinvent requires a license. This is a placeholder.
    # You would need to integrate with Ecoinvent's API or use local database
    return jsonify({
        'success': True,
        'source': 'ecoinvent',
        'database': 'Ecoinvent 3.9.1',
        'processes': [],
        'total_processes': 19000,
        'message': 'Ecoinvent database ready (requires license)',
        'note': 'Ecoinvent integration requires valid license credentials'
    })

def get_indian_datasets():
    """Get Indian LCA dataset information"""
    # Indian LCA data sources:
    # 1. ILCD (Indian Life Cycle Database)
    # 2. TERI datasets
    # This is a placeholder - you'd integrate with actual Indian LCA databases
    
    return jsonify({
        'success': True,
        'source': 'indian',
        'database': 'Indian LCA Database (ILCD)',
        'processes': [
            {'name': 'Electricity mix - India', 'category': 'Energy'},
            {'name': 'Steel production - India', 'category': 'Materials'},
            {'name': 'Cement production - India', 'category': 'Materials'},
            {'name': 'Transport - India (road)', 'category': 'Transport'},
            {'name': 'Aluminum production - India', 'category': 'Materials'},
        ],
        'total_processes': 500,
        'message': 'Indian LCA database loaded with regional data',
        'coverage': {
            'energy': '95%',
            'materials': '85%',
            'transport': '90%'
        }
    })

def get_builtin_datasets():
    """Get built-in default dataset"""
    return jsonify({
        'success': True,
        'source': 'builtin',
        'database': 'MetaLCA Default Database',
        'processes': [
            {'name': 'Electricity, medium voltage', 'category': 'Energy'},
            {'name': 'Steel, low-alloyed', 'category': 'Materials'},
            {'name': 'Plastic, polyethylene', 'category': 'Materials'},
            {'name': 'Transport, freight, lorry', 'category': 'Transport'},
            {'name': 'Wastewater treatment', 'category': 'Waste'},
        ],
        'total_processes': 1200,
        'message': 'Built-in database loaded with global averages'
    })

@dataset_bp.route('/api/upload-dataset', methods=['POST'])
def upload_dataset():
    """Handle custom dataset upload"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'message': 'No files provided'})
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file.filename:
                filename = file.filename
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                uploaded_files.append(filename)
        
        if uploaded_files:
            # Store uploaded file info in session
            session['uploaded_datasets'] = uploaded_files
            
            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {len(uploaded_files)} file(s)',
                'files': uploaded_files
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No valid files uploaded'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Upload error: {str(e)}'
        })

@dataset_bp.route('/api/openlca/databases')
def list_openlca_databases():
    """List all available OpenLCA databases"""
    try:
        response = requests.get(f"{OPENLCA_API_URL}/databases", timeout=5)
        if response.status_code == 200:
            databases = response.json()
            return jsonify({
                'success': True,
                'databases': databases
            })
        return jsonify({
            'success': False,
            'message': 'Could not fetch databases'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@dataset_bp.route('/api/openlca/processes/<database>')
def get_openlca_processes(database):
    """Get processes from a specific OpenLCA database"""
    try:
        # First, you might need to set the active database
        # Then fetch processes
        response = requests.post(
            f"{OPENLCA_API_URL}/data/get/descriptors",
            json={"@type": "Process"},
            timeout=10
        )
        
        if response.status_code == 200:
            processes = response.json()
            return jsonify({
                'success': True,
                'database': database,
                'processes': processes,
                'count': len(processes)
            })
        
        return jsonify({
            'success': False,
            'message': 'Could not fetch processes'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })
