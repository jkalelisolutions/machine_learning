import schedule
import time
import logging

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(messages)%"
)

def fetch_orders():
    print("Orders Fetch")

def send_notification(send):
    print(f"Your order {send} has been sent to you.")

def check_new_orders():
    print("Checking new orders from Kamau Stores...")
    #Your actual task code here
    try:
        orders= fetch_orders()
        if orders:
            send_notification(orders)
            logging.info(f"OK- {len(orders)} new orders found and sent")
        else:
            logging.info("OK- No new orders")
    except Exception as e:
        logging.error(f"FAILED - {e}")

#Choose your schedule
schedule.every(10).minutes.do(check_new_orders)#every 10 min
schedule.every().hour.do(check_new_orders)#every hour
schedule.every().day.at("08:00").do(check_new_orders)#daily
schedule.every().monday.at("09:00").do(check_new_orders)#every Monday

while True:
    schedule.run_pending()
    time.sleep(30)#check every 30 seconds


