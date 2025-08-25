import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")

recipient_email = os.getenv("RECIPIENT_EMAIL")

def send_test_email():
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Test Email from Python Script"
    
    body = """
    Hello,
    
    This is a test email sent from a Python script.
    
    Best regards,
    Python Email Test Script
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        print(f"Test email successfully sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_confirmation_email(customer_email, form_data):
    """Send a confirmation email to the customer with their form data."""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = customer_email
    message["Subject"] = "Bestätigung Ihrer Anfrage"
    
    # Build email body with form data
    name = f"{form_data.get('vorname', '')} {form_data.get('nachname', '')}"
    address = f"{form_data.get('strasse', '')} {form_data.get('hausnr', '')}, {form_data.get('plz', '')} {form_data.get('ort', '')}"
    products = ", ".join(form_data.get('produkt', [])) if isinstance(form_data.get('produkt'), list) else form_data.get('produkt', 'Keine')
    shipping_method = form_data.get('bestellmethode', 'Nicht angegeben')
    payment_method = form_data.get('zahlungsmethode', 'Nicht angegeben')
    
    body = f"""
    Hallo {name},
    
    vielen Dank für Ihre Anfrage. Hier ist eine Zusammenfassung Ihrer Daten:
    
    Name: {name}
    E-Mail: {form_data.get('email', '')}
    Adresse: {address}
    Land: {form_data.get('land', '')}
    Datum: {form_data.get('datum', '')}
    
    Produktkategorie: {products}
    Bestellmethode: {shipping_method}
    Zahlungsmethode: {payment_method}
    
    Wir werden Ihre Anfrage so schnell wie möglich bearbeiten.
    
    Mit freundlichen Grüßen,
    Ihr Support-Team
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        print(f"Confirmation email successfully sent to {customer_email}")
        return True
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
        return False

if __name__ == "__main__":
    send_test_email()