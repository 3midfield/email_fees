import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

articles = ['hello', 2, 5, 'bye']

me = "email@gmail.com"
you = "email@gmail.com"
subject = 'something'

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = me
msg['To'] = you

html = """\

    {% for i in {articles} %}
        <p> {{ i }} </p>
    {% endfor %}

""".format(articles)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login("email@gmail.com", "password")

server.sendmail(me, you, msg.as_string())
server.quit()