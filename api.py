from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import pytz
import requests

app = Flask(__name__)
CORS(app)

TEHRAN_TZ = pytz.timezone('Asia/Tehran')
DATA_FILE = 'data/aqi_data.json'
SITE_URL = 'https://aqms.doe.ir/App/'


def load_aqi_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error: {e}")
    return {}


def get_tehran_time():
    return datetime.now(TEHRAN_TZ)


def check_site_status():
    """بررسی وضعیت سایت"""
    try:
        response = requests.get(SITE_URL, timeout=5)
        return response.status_code == 200
    except:
        return False


@app.route('/api/health', methods=['GET'])
def health():
    site_status = check_site_status()
    data_exists = os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0
    
    return jsonify({
        'status': 'ok',
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran',
        'site_status': 'UP' if site_status else 'DOWN',
        'data_available': data_exists
    })


@app.route('/api/site-status', methods=['GET'])
def site_status():
    """بررسی وضعیت سایت AQI"""
    status = check_site_status()
    return jsonify({
        'site': SITE_URL,
        'status': 'UP' if status else 'DOWN',
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran'
    })


@app.route('/api/aqi', methods=['GET'])
def get_all_aqi():
    dt = load_aqi_data()
    
    if not dt:
        return jsonify({'error': 'No data', 'status': 'no_data'}), 404
    
    return jsonify({
        'status': 'success',
        'count': len(dt),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': dt
    })


@app.route('/api/aqi/<state>', methods=['GET'])
def get_aqi_by_state(state):
    dt = load_aqi_data()
    
    sn = state.strip()
    fs = None
    fd = None
    
    for k, v in dt.items():
        if k.lower() == sn.lower():
            fs = k
            fd = v
            break
    
    if not fd:
        return jsonify({'error': f'State "{state}" not found', 'status': 'not_found'}), 404
    
    return jsonify({
        'status': 'success',
        'state': fs,
        'aqi': fd.get('aqi'),
        'timestamp': fd.get('timestamp'),
        'current_time': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)'
    })


@app.route('/api/aqi/range/<min_aqi>-<max_aqi>', methods=['GET'])
def get_aqi_by_range(min_aqi, max_aqi):
    try:
        mv = int(min_aqi)
        Mv = int(max_aqi)
    except ValueError:
        return jsonify({'error': 'Invalid range', 'status': 'invalid_input'}), 400
    
    dt = load_aqi_data()
    fd = {}
    
    for st, inf in dt.items():
        aqi = inf.get('aqi', 0)
        if mv <= aqi <= Mv:
            fd[st] = inf
    
    return jsonify({
        'status': 'success',
        'range': f'{min_aqi}-{max_aqi}',
        'count': len(fd),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': fd
    })


@app.route('/api/aqi/worst', methods=['GET'])
def get_worst_aqi():
    dt = load_aqi_data()
    
    if not dt:
        return jsonify({'error': 'No data', 'status': 'no_data'}), 404
    
    sd = sorted(dt.items(), key=lambda x: x[1].get('aqi', 0), reverse=True)
    
    lim = request.args.get('limit', 5, type=int)
    ws = dict(sd[:lim])
    
    return jsonify({
        'status': 'success',
        'type': 'worst_aqi',
        'limit': lim,
        'count': len(ws),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': ws
    })


@app.route('/api/aqi/best', methods=['GET'])
def get_best_aqi():
    dt = load_aqi_data()
    
    if not dt:
        return jsonify({'error': 'No data', 'status': 'no_data'}), 404
    
    sd = sorted(dt.items(), key=lambda x: x[1].get('aqi', 0))
    
    lim = request.args.get('limit', 5, type=int)
    bs = dict(sd[:lim])
    
    return jsonify({
        'status': 'success',
        'type': 'best_aqi',
        'limit': lim,
        'count': len(bs),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': bs
    })


@app.route('/api/aqi/stats', methods=['GET'])
def get_aqi_stats():
    dt = load_aqi_data()
    
    if not dt:
        return jsonify({'error': 'No data', 'status': 'no_data'}), 404
    
    vals = [inf.get('aqi', 0) for inf in dt.values()]
    
    st = {
        'total_states': len(dt),
        'average': round(sum(vals) / len(vals), 2),
        'minimum': min(vals),
        'maximum': max(vals),
        'median': sorted(vals)[len(vals)//2]
    }
    
    return jsonify({
        'status': 'success',
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'stats': st
    })


@app.route('/api/time', methods=['GET'])
def get_time():
    return jsonify({
        'status': 'success',
        'time': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'utc_offset': '+03:30'
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'not_found',
        'timestamp': get_tehran_time().isoformat()
    }), 404


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'not_found',
        'message': 'Use /api/health or /api/aqi for valid endpoints',
        'timestamp': get_tehran_time().isoformat()
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'error': 'Server error',
        'status': 'server_error',
        'timestamp': get_tehran_time().isoformat()
    }), 500


@app.route('/', methods=['GET'])
def root():
    """صفحه اصلی - راهنمای API"""
    return jsonify({
        'status': 'ok',
        'message': 'AQI Iran API Server',
        'version': '2.0.0',
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'timestamp': get_tehran_time().isoformat(),
        'endpoints': {
            'health': '/api/health',
            'site_status': '/api/site-status',
            'all_aqi': '/api/aqi',
            'specific_state': '/api/aqi/<state>',
            'aqi_range': '/api/aqi/range/<min>-<max>',
            'worst_quality': '/api/aqi/worst?limit=5',
            'best_quality': '/api/aqi/best?limit=5',
            'statistics': '/api/aqi/stats',
            'current_time': '/api/time'
        }
    })


if __name__ == '__main__':
    print("="*70)
    print("🌍 AQI Data API")
    print("="*70)
    print(f"Timezone: Asia/Tehran (UTC+03:30)")
    print(f"Current time: {get_tehran_time().isoformat()}")
    print("="*70)
    print("\nEndpoints:")
    print("  GET /api/health          - Health check")
    print("  GET /api/aqi             - All AQI data")
    print("  GET /api/aqi/<state>     - State AQI")
    print("  GET /api/aqi/range/<min>-<max>")
    print("  GET /api/aqi/worst?limit=5")
    print("  GET /api/aqi/best?limit=5")
    print("  GET /api/aqi/stats")
    print("  GET /api/time")
    print("="*70)
    print("\nStarting server...\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
