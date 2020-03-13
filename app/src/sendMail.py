import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


FILEPATH = './excels/'
MY_EMAIL = 'informe.casas@gmail.com'
MY_PASSWORD = '17InformeCasas'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def sendMail(subject, filename, to_email):
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = COMMASPACE.join(to_email)
    msg['Subject'] = subject

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(FILEPATH + filename, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(MY_EMAIL, MY_PASSWORD)
    smtpObj.sendmail(MY_EMAIL, to_email, msg.as_string())
    smtpObj.quit()
