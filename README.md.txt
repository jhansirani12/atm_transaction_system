1. Title:
#ATM Management System
2. Overview:
This is a simple ATM Management System implemented in Python with MySQL as the backend.
The system allows users to register new cards, log in, perform transactions, generate new PINs, and recover forgotten PINs with OTP verification.
3. Features:
* New User Registration (with OTP verification)
* Login & Logout
* Withdraw Cash
* Balance Enquiry
* Mini Statement (Last 5 transactions)
* New PIN Generation with OTP (while logged in, no card number required)
* Forgot PIN (requires card number + OTP)
* Transaction History
* Secure OTP-based verification for sensitive actions
* Auto logout after PIN change for security
4. Project Structure:
atm_project.py
atm_db.sql
README.md
5. Install MySQL and python
6. Create Data Base
7. Install Required Packages i.e ------> pip install mysql-connector-python
8. Run SQL server and python file
9. Main Menu:
1. Login
  1.Withdraw
  2. Mini Statement
   3. New PIN Generation with OTP
   4. Logout
2. Forgot PIN
3. Exit
10. Security Notes
* PIN must be 4 digits
* OTP is valid only for one use
* After changing PIN, you must re-login
* Balance updates & transactions are recorded in the database
11. Author:
Developed by K.Jhansi Rani for Python + MySQL learning purposes.
E-mail: kalavajhansirani44@gmail.com
LinkedIn: www.linkedin.com/in/kalava-jhansi-rani-129812239

