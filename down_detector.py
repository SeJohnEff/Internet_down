import time
import ping3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
# Configure the target IP address and email settings
target_ip = "8.8.8.8"
sender_email = "YOURSENDER@gmail.com"
sender_password = "HERE_GOES_YOUR_GMAIL_PASSWORD_OR_APP_PASSWORD"
receiver_email = "YOURRECIEVER@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 465

# Flag variable to track internet connection status
is_internet_up = True
downtime_start = None

# Logfile configuration
logfile = "down_log.txt"

# Start time of the log
log_start_time = datetime.now()

def write_to_log(message):
    with open(logfile, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {message}\n")

def send_email(subject, message):
    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add body to the email
    msg.attach(MIMEText(message, "plain"))

    try:
        # Create a secure SSL connection to the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        write_to_log("Email sent successfully.")
    except Exception as e:
        write_to_log(f"Failed to send email. Error: {str(e)}")

def main():
    global is_internet_up
    global downtime_start

    while True:
        try:
            result = ping3.ping(target_ip)

            if result is not None:
                if not is_internet_up:
                    downtime_end = datetime.now()
                    downtime_duration = (downtime_end - downtime_start).total_seconds() / 60
                    downtime_start_str = downtime_start.strftime("%Y-%m-%d %H:%M:%S")
                    downtime_end_str = downtime_end.strftime("%Y-%m-%d %H:%M:%S")
                    # Calculate uptime percentage
                    uptime_duration = datetime.now() - log_start_time
                    total_duration = uptime_duration + timedelta(minutes=downtime_duration)
                    uptime_percentage = (uptime_duration.total_seconds() / total_duration.total_seconds()) * 100
                    write_to_log(f"Ping successful. Internet is back. Downtime duration: {downtime_duration:.2f} minutes.")
                    send_email("Internet Restored", f"The internet connection is back.\n\nDowntime start: {downtime_start_str}\nDowntime end: {downtime_end_str}\nDowntime duration: {downtime_duration:.2f} minutes.\nUptime percentage: {uptime_percentage:.2f}%")
                    is_internet_up = True
                else:
                    write_to_log("Ping successful. Internet is up.")
            else:
                if is_internet_up:
                    downtime_start = datetime.now()
                    write_to_log("Ping failed. Internet is down.")
                    is_internet_up = False
                else:
                    write_to_log("Ping failed. Internet is still down.")
        except Exception as e:
            write_to_log(f"An error occurred: {str(e)}")
        # Sleep for 1 minute before the next ping
        time.sleep(60)
if __name__ == "__main__":
    main()
