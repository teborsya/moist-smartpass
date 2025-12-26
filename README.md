# SmartPass Project Task List

### 1. Crontab Library (Turn Off / On Scheduler)
- ✅ Implement and test automatic system shutdown and startup using `python-crontab`.

### 2. QR Code Scanner → API Communication
- ✅ Implement code to send scanned QR code data to a specific API endpoint.  
- ✅ Test POST requests for successful submission.

    **Subtasks:**  
    - 🔲 2.1 No Internet Connection Detected  
    - Add a status field `is_submitted` with choices `(True, False)`.  
    - Store scanned QR code data locally for later submission.  

    - 🔲 2.2 Internet Connection Detected  
    - Check all rows where `is_submitted = False`.  
    - Submit stored data to the API endpoint.  

    - 🔲 Verify that a 200 OK response is received from the API.

### 3. SMS Notification with SIM7600 Module
- 🔲 Implement an SMS blasting system for students when they scan their QR code.  
- 🔲 Enforce a rate limit: maximum 30 SMS per 5 minutes.

### 4. WebSockets (Socket.IO)
- 🔲 Implement emitter to trigger the server and RSP.  
