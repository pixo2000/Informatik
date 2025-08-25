import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import EMAIL_CONFIG

class EmailService:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.email = EMAIL_CONFIG['email']
        self.password = EMAIL_CONFIG['password']
        self.sender_name = EMAIL_CONFIG['sender_name']
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send an email with HTML content"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.email}>"
            message["To"] = to_email
            
            # Create text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                server.sendmail(self.email, to_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_verification_email(self, to_email, verification_code):
        """Send email verification code"""
        subject = "RaphCup - E-Mail Verifizierung"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0f1419; color: #ffffff; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1e2328; border-radius: 10px; padding: 30px; border: 1px solid #3c4043;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #ff4655; font-size: 2rem; margin: 0;">RaphCup</h1>
                    <p style="color: #ffffff; opacity: 0.8; margin: 10px 0;">Valorant Tournament Platform</p>
                </div>
                
                <h2 style="color: #ff4655; text-align: center;">E-Mail Verifizierung</h2>
                
                <p style="font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                    Willkommen beim RaphCup! Um Ihre Registrierung abzuschließen, geben Sie bitte den folgenden Verifizierungscode ein:
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <div style="background-color: #ff4655; color: white; padding: 15px 30px; border-radius: 5px; font-size: 24px; font-weight: bold; letter-spacing: 3px; display: inline-block;">
                        {verification_code}
                    </div>
                </div>
                
                <p style="font-size: 14px; color: #ffffff; opacity: 0.7; text-align: center; margin-top: 30px;">
                    Dieser Code ist 15 Minuten gültig. Falls Sie sich nicht bei RaphCup registriert haben, ignorieren Sie diese E-Mail.
                </p>
                
                <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #3c4043;">
                    <p style="font-size: 12px; color: #ffffff; opacity: 0.5;">
                        &copy; 2024 RaphCup. Alle Rechte vorbehalten.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        RaphCup - E-Mail Verifizierung
        
        Willkommen beim RaphCup!
        
        Ihr Verifizierungscode: {verification_code}
        
        Geben Sie diesen Code auf der Website ein, um Ihre Registrierung abzuschließen.
        
        Dieser Code ist 15 Minuten gültig.
        
        Falls Sie sich nicht bei RaphCup registriert haben, ignorieren Sie diese E-Mail.
        
        © 2024 RaphCup. Alle Rechte vorbehalten.
        """
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_password_reset_email(self, to_email, reset_token):
        """Send password reset email"""
        subject = "RaphCup - Passwort zurücksetzen"
        reset_link = f"http://localhost:5000/reset-password?token={reset_token}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0f1419; color: #ffffff; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1e2328; border-radius: 10px; padding: 30px; border: 1px solid #3c4043;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #ff4655; font-size: 2rem; margin: 0;">RaphCup</h1>
                    <p style="color: #ffffff; opacity: 0.8; margin: 10px 0;">Valorant Tournament Platform</p>
                </div>
                
                <h2 style="color: #ff4655; text-align: center;">Passwort zurücksetzen</h2>
                
                <p style="font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                    Sie haben eine Passwort-Zurücksetzung für Ihr RaphCup-Konto angefordert.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" 
                       style="background-color: #ff4655; color: white; padding: 15px 30px; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block;">
                        Passwort zurücksetzen
                    </a>
                </div>
                
                <p style="font-size: 14px; color: #ffffff; opacity: 0.7;">
                    Alternativ können Sie den folgenden Link in Ihren Browser kopieren:<br>
                    <span style="word-break: break-all;">{reset_link}</span>
                </p>
                
                <p style="font-size: 14px; color: #ffffff; opacity: 0.7; text-align: center; margin-top: 30px;">
                    Dieser Link ist 1 Stunde gültig. Falls Sie keine Passwort-Zurücksetzung angefordert haben, ignorieren Sie diese E-Mail.
                </p>
                
                <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #3c4043;">
                    <p style="font-size: 12px; color: #ffffff; opacity: 0.5;">
                        &copy; 2024 RaphCup. Alle Rechte vorbehalten.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        RaphCup - Passwort zurücksetzen
        
        Sie haben eine Passwort-Zurücksetzung für Ihr RaphCup-Konto angefordert.
        
        Klicken Sie auf den folgenden Link, um Ihr Passwort zurückzusetzen:
        {reset_link}
        
        Dieser Link ist 1 Stunde gültig.
        
        Falls Sie keine Passwort-Zurücksetzung angefordert haben, ignorieren Sie diese E-Mail.
        
        © 2024 RaphCup. Alle Rechte vorbehalten.
        """
        
        return self.send_email(to_email, subject, html_content, text_content)

# Global email service instance
email_service = EmailService()
