# gr-dashboard-backend
## Setting Up Environment Variables
1. Copy the `.env.dist` file to create a `.env` file:
   ```bash
   cp .env.dist .env
   ```
2. Replace the placeholders in `.env` with your actual values.
3. Start the application.

## Using the tests
- `read_db.py`: This script reads the database and prints its output in the terminal. Run it from the root directory using the command: `python -m tests.read_db`
- `delete_db.py`: In case you want to delete the entries made to the database so far and reset the id increment counter to 1, use this script from the root directory using the command: `python -m tests.delete_db`
- `certificate_sender_test.py` and `certificate_preview_test.py` You can run these test as it is to check if the certificate sender is working or not. If you want to run this on postman:
1. Copy the json from the top of the respective test file
2. Go to postman
3. Enter the address for the resource you want to test
4. Change the method to post
5. Paste the json in body (choose format as json)
6. Send the request

> PS for the certificate_sender_test.py enter your email id in the placeholders before running the code or in the json before running it on postman
