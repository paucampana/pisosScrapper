import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import config
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)



def sendResults():
    try:
        with open(config.FILEPATH) as f:
            csv_length = sum(1 for line in f)
            logging.info("TOTAL FOUND: " + str(csv_length - 1))
            if csv_length > 1:
                subject = "INFORME DIA " + datetime.now().strftime('%Y/%m/%d')
                to_email = [config.MAIL_TO_SEND]
                sendMail(subject, to_email)
            else:
                logging.info("EMPTY CSV. NOT SENT")

    except Exception as e:
        logging.error(e)
        logging.error("***EXCEPTION SENDING MAIL: " + type(e).__name__ + " ***")


def sendMail(subject, to_email):
    msg = MIMEMultipart()
    msg['From'] = config.USER_MAIL
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
    smtpObj.login(config.USER_MAIL, config.PW_MAIL)
    smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtpObj.quit()
