import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
from dotenv import load_dotenv

load_dotenv()

sales=[{"item_name":"Cupboard","quantity_sold":30, "price":18000},
    {"item_name":"Table","quantity_sold":100, "price":12000},
    {"item_name":"Bed","quantity_sold":50, "price":28000},
    {"item_name":"chair","quantity_sold":25, "price":8000},
    {"item_name":"Glasses","quantity_sold":40, "price":3000},
    {"item_name":"Window panes","quantity_sold":60, "price":35000},
    {"item_name":"Sofa Set","quantity_sold":75, "price":42000},
    {"item_name":"Chandalier","quantity_sold":10, "price":58000},
    {"item_name":"Stool","quantity_sold":80, "price":2500},
    {"item_name":"Plates","quantity_sold":90, "price":1000}
]
report= []

#Calculating the sales of each Item
for data in sales:
    quantity = data["quantity_sold"]
    price = data["price"]
    name = data["item_name"]
    total = quantity * price
    print(f"{name}: KES {total:,}")
    result= ({"Name":name,"Quantity":quantity,"Total":total})
    report.append(result)
    
    
with open("sales.csv","w")as f:
        writer = csv.DictWriter(f,fieldnames=["Name","Quantity","Total"])
        writer.writeheader()
        writer.writerows(report)
        print(f"\nData: {len(report)} saved in sales.csv")


def send_html():
    rows = []

    for data in sales:
        total = data["quantity_sold"] * data["price"]
        rows.append(
            f"<tr>"
            f"<td>{data['item_name']}</td>"
            f"<td>{data['quantity_sold']}</td>"
            f"<td>KES {total:,}</td>"
            f"</tr>"
        )

    html_body = f"""
    <html>
      <body>
        <h2>Sales Summary</h2>
        <table style="border-collapse: collapse;">
          <thead>
            <tr style="background:#1F4E79; color:white;">
              <th style="border: 1px solid #ccc; padding: 8px;">Name</th>
              <th style="border: 1px solid #ccc; padding: 8px;">Quantity Sold</th>
              <th style="border: 1px solid #ccc; padding: 8px;">Total</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["To"] = os.getenv("EMAIL_ADDRESS")
    msg["Subject"] = "Daily Sales Report"
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_APP"))
        server.send_message(msg)

send_html()
    
print("Data sent successfully.")
    