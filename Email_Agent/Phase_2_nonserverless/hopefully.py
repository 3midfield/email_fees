import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
# csv, sender, receiver, emailing_list
def push_to_sendgrid():
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('*************'))
    
    # for i in range(len(csv)):
    #     from_email = Email(sender[i])  # Change to your verified sender
    #     to_email = To(receiver[i])  # Change to your recipient
    #     subject = emailing_list[t]
    #     content = Content("text/plain", emailing_list[t + 1])
    #     t = t + 2
    #     mail = Mail(from_email, to_email, subject, content)

    #     # Get a JSON-ready representation of the Mail object
    #     mail_json = mail.get()

    #     # Send an HTTP POST request to /mail/send
    #     response = sg.client.mail.send.post(request_body=mail_json)
    #     print(response.status_code)
    #     print(response.headers)
    from_email = Email("*********")  # Change to your verified sender
    to_email = To("***************")  # Change to your recipient
    subject = "Subject 1"
    content = Content("text/plain","Content 1")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
    print('nice')

push_to_sendgrid