import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import config




def sendMail(subject, to_email):
    msg = MIMEMultipart()
    msg['From'] = config.USER_PISOS
    msg['To'] = COMMASPACE.join(to_email)
    msg['Subject'] = subject

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(config.FILEPATH, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='Houses_dataframe.csv')
    msg.attach(part)

    smtpObj = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(config.USER_PISOS, config.PW_PISOS)
    smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtpObj.quit()
