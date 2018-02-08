from core.config import EMAIL_DATA
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_message(from_addr, to_addr, sub, file_name, file_folder=''):
    print("Enviando a {}...".format(to_addr))
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Boleta de pago"

    automatico = """
    Boleta de pago: {}.
    Este mensaje fue generado de forma automática.
    Para dudas o comentarios favor escribir a {} o escanee el código QR en el documento
    """.format(sub, EMAIL_DATA['from'])

    msg.attach(MIMEText(automatico, 'plain'))
    with open(str(file_folder / file_name), 'rb') as f:
        pdf = MIMEApplication(f.read())
        pdf.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(pdf)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL_DATA['gmail_user'], EMAIL_DATA['gmail_password'])
        server.send_message(msg)
        server.close()
    except Exception as e:
        print('Hubo un error al enviar el archivo {}'.format(file_name))
        print(e)
        return False

    return True
