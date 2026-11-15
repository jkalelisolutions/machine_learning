import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

def send_email(to,subject,body):
    msg= MIMEText(body)
    msg["from"]= os.getenv("GMAIL_ADDRESS")
    msg["to"]= to


def send_html_report(to, data):
    html_body = (
        '<html><body style="font-family: Arial, sans-serif;">'
        '<h2 style="color: #1F4E79;">Weekly Sales Report</h2>'
        '<table border="1" cellpadding="8" style="border-collapse:collapse;">'
        '<tr style="background:#1F4E79; color:white;"><th>County</th><th>Orders</th><th>Revenue (KES)</th></tr>'
        f'<tr><td>Nairobi</td><td>{data["nairobi_orders"]}</td><td>{data["nairobi_revenue"]:,}</td></tr>'
        f'<tr><td>Mombasa</td><td>{data["mombasa_orders"]}</td><td>{data["mombasa_revenue"]:,}</td></tr>'
        '</table></body></html>'
    )
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Weekly Sales Report"
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(os.getenv("EMAIL_ADDRESS"),
                     os.getenv("EMAIL_APP"))
        server.send_message(msg)

#Testing it
send_email(
    to="kamau@example.co.ke",
    subject="Weekly Report",
    body="Hello DESC," \
    "\nYour weekly sales report is attached." \
    "\nRegards"
)
send_html_report(to="descorner47@gmail.com", data={"nairobi_orders":20,"nairobi_revenue":2000000,"mombasa_orders":15, "mombasa_revenue":3000000})
print("Success")