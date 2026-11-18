# EMAIL AUTOMATION SCRIPT

This is a simple script that sends automated Email of sales report daily to a retail shop owner. The script calculates daily sales, saves it in csv format and send a html table of the data collected to the owners Email. This script is good for business when sending emails like invoices, it is also good for schools when sending fee balances to parents, and even for personal use.

## To Setup

1. Go to Google Account -> Security -> 2-step verification -> App Password and create a new password. Format: abcd efgh ijkl mnop and copy it.
2. Create a .gitignore and a .env file.
3. Copy the password in .env file: GMAIL_APP= your_password_here and GMAIL_ADDRESS=<youremail@gmail.com>.
4. Make sure your .env file is in .gitignore file before pushing to GitHub.

### To Run

``` text
python day23_exercise.py
```

I would charge KES 30,000 to build this script.
