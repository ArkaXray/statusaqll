from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

TEHRAN_TZ = pytz.timezone('Asia/Tehran')
DATA_FILE = 'data/aqi_data.json'


def load_aqi_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
    return {}


def get_tehran_time():
    return datetime.now(TEHRAN_TZ)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran'
    })


@app.route('/api/aqi', methods=['GET'])
def get_all_aqi():
    data = load_aqi_data()
    
    if not data:
        return jsonify({
            'error': 'No data available',
            'status': 'no_data'
        }), 404
    
    response = {
        'status': 'success',
        'count': len(data),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': data
    }
    
    return jsonify(response)


@app.route('/api/aqi/<state>', methods=['GET'])
def get_aqi_by_state(state):
    data = load_aqi_data()
    
    state_name = state.strip()
    
    found_state = None
    found_data = None
    
    for key, value in data.items():
        if key.lower() == state_name.lower():
            found_state = key
            found_data = value
            break
    
    if not found_data:
        return jsonify({
            'error': f'State "{state}" not found',
            'status': 'not_found'
        }), 404
    
    response = {
        'status': 'success',
        'state': found_state,
        'aqi': found_data.get('aqi'),
        'timestamp': found_data.get('timestamp'),
        'current_time': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)'
    }
    
    return jsonify(response)


@app.route('/api/aqi/range/<min_aqi>-<max_aqi>', methods=['GET'])
def get_aqi_by_range(min_aqi, max_aqi):
    try:
        min_val = int(min_aqi)
        max_val = int(max_aqi)
    except ValueError:
        return jsonify({
            'error': 'Invalid range values',
            'status': 'invalid_input'
        }), 400
    
    data = load_aqi_data()
    filtered_data = {}
    
    for state, info in data.items():
        aqi = info.get('aqi', 0)
        if min_val <= aqi <= max_val:
            filtered_data[state] = info
    
    response = {
        'status': 'success',
        'range': f'{min_aqi}-{max_aqi}',
        'count': len(filtered_data),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': filtered_data
    }
    
    return jsonify(response)


@app.route('/api/aqi/worst', methods=['GET'])
def get_worst_aqi():
    data = load_aqi_data()
    
    if not data:
        return jsonify({
            'error': 'No data available',
            'status': 'no_data'
        }), 404
    
    sorted_data = sorted(data.items(), key=lambda x: x[1].get('aqi', 0), reverse=True)
    
    limit = request.args.get('limit', 5, type=int)
    worst_states = dict(sorted_data[:limit])
    
    response = {
        'status': 'success',
        'type': 'worst_aqi',
        'limit': limit,
        'count': len(worst_states),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': worst_states
    }
    
    return jsonify(response)


@app.route('/api/aqi/best', methods=['GET'])
def get_best_aqi():
    data = load_aqi_data()
    
    if not data:
        return jsonify({
            'error': 'No data available',
            'status': 'no_data'
        }), 404
    
    sorted_data = sorted(data.items(), key=lambda x: x[1].get('aqi', 0))
    
    limit = request.args.get('limit', 5, type=int)
    best_states = dict(sorted_data[:limit])
    
    response = {
        'status': 'success',
        'type': 'best_aqi',
        'limit': limit,
        'count': len(best_states),
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'data': best_states
    }
    
    return jsonify(response)


@app.route('/api/aqi/stats', methods=['GET'])
def get_aqi_stats():
    data = load_aqi_data()
    
    if not data:
        return jsonify({
            'error': 'No data available',
            'status': 'no_data'
        }), 404
    
    aqi_values = [info.get('aqi', 0) for info in data.values()]
    
    stats = {
        'total_states': len(data),
        'average': round(sum(aqi_values) / len(aqi_values), 2),
        'minimum': min(aqi_values),
        'maximum': max(aqi_values),
        'median': sorted(aqi_values)[len(aqi_values)//2]
    }
    
    response = {
        'status': 'success',
        'timestamp': get_tehran_time().isoformat(),
        'timezone': 'Asia/Tehran (UTC+03:30)',
        'stats': stats
    }
    
    return jsonify(response)


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


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'error': 'Internal server error',
        'status': 'server_error',
        'timestamp': get_tehran_time().isoformat()
    }), 500


if __name__ == '__main__':
    print("="*70)
    print("🌍 AQI Data API")
    print("="*70)
    print(f"Timezone: Asia/Tehran (UTC+03:30)")
    print(f"Current time: {get_tehran_time().isoformat()}")
    print("="*70)
    print("\nEndpoints:")
    print("  GET /api/health                    - Health check")
    print("  GET /api/aqi                       - Get all AQI data")
    print("  GET /api/aqi/<state>               - Get AQI for specific state")
    print("  GET /api/aqi/range/<min>-<max>     - Get AQI in range")
    print("  GET /api/aqi/worst?limit=5         - Get worst AQI states")
    print("  GET /api/aqi/best?limit=5          - Get best AQI states")
    print("  GET /api/aqi/stats                 - Get AQI statistics")
    print("  GET /api/time                      - Get current Tehran time")
    print("="*70)
    print("\nStarting server...\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )
