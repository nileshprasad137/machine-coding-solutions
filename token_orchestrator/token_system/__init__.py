from flask import Blueprint

token_system_bp = Blueprint("token_system", __name__)

from . import views

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # @app.route('/keys', methods=(['GET']))
#     # def get_keys():
#     #     available_key = []
#     #     for key_id in api_keys:
#     #         if api_keys[key_id]["status"]:
#     #             # key_val = api_keys[key_id]["key"]
#     #             available_key.append({key_id: api_keys[key_id].copy()})
#     #             api_keys[key_id]["status"] = False
#     #             break
#     #             # API_KEYS_SET.remove(key_val)
#     #     if len(available_key) == 0:
#     #         return {"error": "key not available"}, 404
#     #     return jsonify({"key": available_key})
    
# #     @app.route('/keys', methods=(['POST']))
# #     def create_keys():
# #         key = request.json.get("key")
# #         if key in API_KEYS_SET:
# #             return jsonify({"message": "key creation failed as key is already present."})
# #         cache["MAX_ID_SEEN_SO_FAR"] += 1
# #         id = cache["MAX_ID_SEEN_SO_FAR"]
# #         api_keys[id] = {"status": True, "last_alive": datetime.datetime.now(), "key": key}
# #         API_KEYS_SET.add(key)
# #         print("id : ", cache["MAX_ID_SEEN_SO_FAR"])
# #         print(API_KEYS_SET)
# #         return jsonify({"message": "key created successfully"})
    
# #     @app.route('/keys/<id>', methods=(['GET']))
# #     def get_key_details(id):
# #         if int(id) not in api_keys:
# #             return {"error": "key not available"}, 404
# #         return jsonify({"details": api_keys[int(id)]})
    
# #     @app.route('/keys/<id>', methods=(['DELETE']))
# #     def delete_key(id):
# #         if int(id) not in api_keys:
# #             return {"error": "key not available"}, 404
# #         api_keys.pop(int(id), None)
# #         print(api_keys)
# #         return jsonify({"message": "deleted"})
    
# #     # @app.route('/keys', methods=('POST'))
# #     # def add_keys():
# #     #     return 'Hello, World!'
    
# #     # @app.route('/keys/<key_id>', methods=('GET'))
# #     # def get_key_info():
# #     #     return 'Hello, World!'
    
# #     # @app.route('/keys/<key_id>', methods=('GET'))
# #     # def get_key_info():
# #     #     return 'Hello, World!'
    
# #     # @app.route('/keys/<key_id>', methods=('DELETE'))
# #     # def get_key_info():
# #     #     return 'Hello, World!'
    
# #     # @app.route('/keys/<key_id>', methods=('PUT'))
# #     # def get_key_info():
# #     #     return 'Hello, World!'

# #     return app

# # ----

# # from flask import Flask, jsonify, abort
# # import uuid
# # import time
# # from threading import Lock

# # app = Flask(__name__)

# # # Data structures
# # keys = {}  # Key info storage
# # available_keys = set()  # Available keys index
# # blocked_keys = {}  # Blocked keys with automatic release
# # keys_lock = Lock()  # To ensure thread-safe operations

# # def auto_unblock():
# #     """Automatically unblock keys that are due."""
# #     with keys_lock:
# #         current_time = time.time()
# #         keys_to_unblock = [key for key, unblock_time in blocked_keys.items() if unblock_time <= current_time]
# #         for key in keys_to_unblock:
# #             if key in blocked_keys:
# #                 del blocked_keys[key]
# #                 available_keys.add(key)
# #                 keys[key]['status'] = 'available'

# # @app.route('/keys', methods=['POST'])
# # def create_key():
# #     """Endpoint to create new keys."""
# #     with keys_lock:
# #         new_key = str(uuid.uuid4())
# #         keys[new_key] = {'status': 'available', 'last_accessed_time': time.time()}
# #         available_keys.add(new_key)
# #     return jsonify({'key': new_key}), 201

# # @app.route('/keys', methods=['GET'])
# # def get_key():
# #     """Endpoint to retrieve an available key."""
# #     with keys_lock:
# #         if not available_keys:
# #             abort(404, description="No available keys")
# #         key = available_keys.pop()
# #         blocked_keys[key] = time.time() + 60  # Block for 60 seconds
# #         keys[key]['status'] = 'blocked'
# #     return jsonify({'key': key}), 200

# # @app.route('/keys/<key_id>', methods=['PUT'])
# # def unblock_key(key_id):
# #     """Endpoint to unblock a previously assigned key."""
# #     with keys_lock:
# #         if key_id in blocked_keys:
# #             del blocked_keys[key_id]
# #             available_keys.add(key_id)
# #             keys[key_id]['status'] = 'available'
# #         else:
# #             abort(404, description="Key not found or not blocked")
# #     return jsonify({'status': 'unblocked'}), 200

# # @app.route('/keys/<key_id>', methods=['DELETE'])
# # def delete_key(key_id):
# #     """Endpoint to permanently remove a key from the system."""
# #     with keys_lock:
# #         if key_id in keys:
# #             if key_id in available_keys:
# #                 available_keys.remove(key_id)
# #             if key_id in blocked_keys:
# #                 del blocked_keys[key_id]
# #             del keys[key_id]
# #         else:
# #             abort(404, description="Key not found")
# #     return jsonify({'status': 'deleted'}), 200

# # @app.route('/keepalive/<key_id>', methods=['PUT'])
# # def keepalive_key(key_id):
# #     """Endpoint for key keep-alive functionality."""
# #     with keys_lock:
# #         if key_id in keys:
# #             keys[key_id]['last_accessed_time'] = time.time()
# #             if key_id in blocked_keys:
# #                 blocked_keys[key_id] = time.time() + 60  # Extend block for another 60 seconds
# #         else:
# #             abort(404, description="Key not found")
# #     return jsonify({'status': 'keepalive updated'}), 200

# # if __name__ == '__main__':
# #     app.run(debug=True)
