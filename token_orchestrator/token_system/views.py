from flask import Flask, jsonify, abort
import uuid
import time
from threading import Lock

from token_system import token_system_bp

app = Flask(__name__)

# Data structures
keys = {}  # Key info storage
available_keys = set()  # Available keys index
blocked_keys = {}  # Blocked keys with automatic release
keys_lock = Lock()  # To ensure thread-safe operations

def auto_unblock():
    """Automatically unblock keys that are due."""
    with keys_lock:
        current_time = time.time()
        keys_to_unblock = [key for key, unblock_time in blocked_keys.items() if unblock_time <= current_time]
        print("keys_to_unblock: ", keys_to_unblock)
        for key in keys_to_unblock:
            if key in blocked_keys:
                del blocked_keys[key]
                available_keys.add(key)
                keys[key]['status'] = 'available'

@token_system_bp.route('/keys', methods=['POST'])
def create_key():
    """Endpoint to create new keys."""
    with keys_lock:
        new_key = str(uuid.uuid4())
        keys[new_key] = {'status': 'available', 'last_accessed_time': time.time()}
        available_keys.add(new_key)
        print("keys: ", keys)
        print("available_keys: ", available_keys)
    return jsonify({'key': new_key}), 201

@token_system_bp.route('/keys', methods=['GET'])
def get_key():
    """Endpoint to retrieve an available key."""
    with keys_lock:
        if not available_keys:
            abort(404, description="No available keys")
        key = available_keys.pop()
        blocked_keys[key] = time.time() + 60  # Block for 60 seconds
        keys[key]['status'] = 'blocked'
    return jsonify({'key': key}), 200

@token_system_bp.route('/keys/<key_id>', methods=['PUT'])
def unblock_key(key_id):
    """Endpoint to unblock a previously assigned key."""
    with keys_lock:
        if key_id in blocked_keys:
            del blocked_keys[key_id]
            available_keys.add(key_id)
            keys[key_id]['status'] = 'available'
        else:
            abort(404, description="Key not found or not blocked")
    return jsonify({'status': 'unblocked'}), 200

@token_system_bp.route('/keys/<key_id>', methods=['DELETE'])
def delete_key(key_id):
    """Endpoint to permanently remove a key from the system."""
    with keys_lock:
        if key_id in keys:
            if key_id in available_keys:
                available_keys.remove(key_id)
            if key_id in blocked_keys:
                del blocked_keys[key_id]
            del keys[key_id]
        else:
            abort(404, description="Key not found")
    return jsonify({'status': 'deleted'}), 200

@token_system_bp.route('/keepalive/<key_id>', methods=['PUT'])
def keepalive_key(key_id):
    """Endpoint for key keep-alive functionality."""
    with keys_lock:
        if key_id in keys:
            keys[key_id]['last_accessed_time'] = time.time()
            if key_id in blocked_keys:
                blocked_keys[key_id] = time.time() + 60  # Extend block for another 60 seconds
        else:
            abort(404, description="Key not found")
    return jsonify({'status': 'keepalive updated'}), 200

