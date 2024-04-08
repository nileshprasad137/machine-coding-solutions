### Token Orchestrator

Design a server capable of generating, assigning, and managing API keys with specific functionalities. The server should offer various endpoints for interaction:

 - An endpoint to create new keys.
 - An endpoint to retrieve an available key, ensuring the key is randomly selected and not currently in use. This key should then be blocked from being served again until its status changes. If no keys are available, a 404 error should be returned.
 - An endpoint to unblock a previously assigned key, making it available for reuse.
 - An endpoint to permanently remove a key from the system.
 - An endpoint for key keep-alive functionality, requiring clients to signal every minute to prevent the key from being deleted.
 - Automatically release blocked keys within 60 seconds if not unblocked explicitly.

### Constraints:
Ensuring efficient key management without the need to iterate through all keys for any operation. The complexity of endpoint requests should be aimed at O(log n) or O(1) for scalability and efficiency.

#### Endpoints:
 - POST /keys: Generate new keys.
 - GET /keys: Retrieve an available key for client use.
 - HEAD /keys/:id: Provide information (e.g., assignment timestamps) about a specific key.
 - DELETE /keys/:id: Remove a specific key, identified by :id, from the system.
 - PUT /keys/:id: Unblock a key for further use.
 - PUT /keepalive/:id: Signal the server to keep the specified key, identified by :id, from being deleted.
