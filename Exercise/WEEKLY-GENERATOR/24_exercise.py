import os, csv,smtplib
import shutil
import logging
import schedule
from datetime import datetime
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
import anthropic
from dotenv import load_dotenv
load_dotenv()
Source= Path("C:/Users/DELL/Documents/Sales")
Log= Path("C:/Users/DELL/Documents/Sales/Sales.log")
Processed_file=Path("C:/Users/DELL/Documents/Sales/processed_sales.log")
client= anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API"))


def get_processed():
    if not Processed_file.exists():
        return set()
    return {
        line.strip()
        for line in Processed_file.read_text(encoding="utf-8").splitlines()
        if line.strip()

    }

def mark_processed(filename:str) -> None:
    with Processed_file.open("a", encoding="utf-8") as f:
        f.write(f"{filename}\n")

def process_file_daily():
    today= Source/f"{datetime.today().isoformat()}.csv"
    processed= get_processed()
    if today.is_file() and today.name in processed:
        with today.open("r",encoding="utf-8-sig", newline="") as f:
            reader= csv.DictReader(f)
            if not reader.fieldnames or not any(name and name.strip() for name in reader.fieldnames):
                return f"{today.name}: skipped because it has no columns"
            
        mark_processed(today.name)



def merge_files(file: Path)->None:
    output= file/"Merged_Sales.csv"
    
    csv_path= [
        p for p in file.iterdir()
        if p.is_file() and p.suffix.lower()== ".csv" and p != output
    ]
    
    if not csv_path:
        raise FileNotFoundError(f"No csv file found in {file}")
    fieldnames= None

    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer= None
        for paths in csv_path:
            with paths.open( newline="", encoding="utf-8-sig") as input:
                reader= csv.DictReader(input)
                if not reader.fieldnames:
                    continue
                if fieldnames is None:
                    fieldnames= reader.fieldnames
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                elif reader.fieldnames != fieldnames:
                    raise ValueError(f"{paths} has different columns.")
    

def send_email(summary):
    email=  merge_files(summary)
    sales= [] 
    if email:
        with open(email,"r", encoding="utf-8", newline="")as f:
            data= list(csv.DictReader(f))
        for data in summary:
            name= data["Name"]
            total= float(sum(data["Totals"]))
            sales.append(
                f"<tr>"
                f"<td>{name}</td>"
                f"<td>KES {total}</td>"
                f"</tr>"
            )

            html_body = f"""
                 <html>
                    <body>
                       <h2>Sales Summary</h2>
                         <table style="border-collapse: collapse; border="1" cellpadding="8"">
                            <thead>
                              <tr style="background:#1F4E79; color:white;">
                                 <th style="border: 1px solid #ccc; padding: 8px;">Name</th>
                                 <th style="border: 1px solid #ccc; padding: 8px;">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                              {''.join(sales)}
                            </tbody>
                          </table>
                    </body>
                </html>
             """
            system_prompt="""You are a professional Sales Trend Analyzer
            Your Rules:
            1. Be brief and professional. Your answer should not be above four sentences.
            2. You analyze the weekly summary of the merged_files(), and provide a comment about the weekly sales.
            3. You only task is to provide analysis about the sales every end of week, do not go out of scope.
            """

            response= client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=512,
                system=system_prompt,
                messages=[{"role":"user","content":summary}]
            )
            
            text_parts = [
                   block.text
                   for block in response.content
                   if block.type == "text"
                ]
            if not text_parts:
                 raise ValueError("Anthropic response contained no text block")

            reply = "\n".join(text_parts)

            msg= MIMEMultipart("alternative")
            msg["Subject"]= "Consolidated Weekly Report"
            if msg["To"] :
                os.getenv("EMAIL_ADDRESS")
            msg.attach(MIMEText(html_body,"html"))
            msg.attach(MIMEText(reply,"plain", "utf-8"))

            with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
                server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_APP"))
                server.send_message(msg)
    return f"{email}"



logging.basicConfig(
    filename=Log,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

if __name__ == "__main__":
    raise SystemExit(send_email(Source))

print("Success")