import pickle
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

sys.setrecursionlimit(10000000)

import requests
from bs4 import BeautifulSoup

links = ['https://saopaulo.consulfrance.org/-Vistos-246-',
         'https://saopaulo.consulfrance.org/-Visas-247-',
         'https://saopaulo.consulfrance.org/-Portugues-',
         'https://saopaulo.consulfrance.org/-Francais-',
         'https://saopaulo.consulfrance.org/spip.php?page=article&id_article=4231']


def check_mudanca():
    headers = {'User-Agent': 'Mozilla/5.0'}

    sender_email = "informativos.atha@gmail.com"
    receiver_email = "victorathanasio@usp.br"
    password = 'Givilata_12022518'

    message = MIMEMultipart("alternative")
    text = '''\
        '''

    mud = False

    for i in range(len(links)):
        pickle_in = open("soup{}.pickle".format(i), "rb")
        soup_ref = pickle.load(pickle_in)
        pickle_in.close()
        page = requests.get(links[i], headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        mudanca = not (soup_ref == soup)
        if mudanca:
            mud = True
            message["Subject"] = "IMPORTANTE MUDOU"
            print('Link {} mudou')
            text += """\
                            <p>Link {} mudou</p>""".format(i)

    if not mud:
        message["Subject"] = "Att consulado"
        text += """\
                <p>Nada mudou, apenas funcionando</p>"""


    message["From"] = sender_email
    message["To"] = receiver_email
    message['Cc'] = 'filipe.penna.soares@gmail.com'
    # Create the plain-text and HTML version of your message

    html = """\
    <html>
      <body>
      <p> {} </p>
        <p><br>""".format(text)

    for i, link in enumerate(links):
        html += '<a href="{}">Link {}</a><br>'.format(link, i)

    html += """
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "html")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, [receiver_email, 'filipe.penna.soares@gmail.com'], message.as_string()
        )




def atualiza_ref():
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(len(links)):
        page = requests.get(links[i], headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        pickle_in = open("soup{}.pickle".format(i), "wb")
        soup_ref = pickle.dump(soup, pickle_in)
        pickle_in.close()
