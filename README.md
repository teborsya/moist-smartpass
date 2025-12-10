# smartpass

Task Lists:

1. Crontab Library (turn off/on scheduler)  
   ✅ test auto on/off

2. QR code scanner then send obtained data to specific API endpoint  

   🔲 test a POST requests.  

        🔲 2.1 If no internet connection is detected:
        - Add a status field named `is_submitted` with choices `(True, False)`
        - Store the obtained data locally

        🔲 2.2 If internet connection is detected:
        - Check all rows where `is_submitted = False` and submit them to the API endpoint

   🔲 test if a 200 status response recieved.

3. SMS notification with SIM7600 module  
   🔲 limit 30 sms every 5 mins.

4. Websockets (socket.io)  
   🔲 emmiter to trigger server and RSP
