def send_mail(message, receiver_email):

    import smtplib, ssl
    from decouple import config
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = config('MAIL_USERNAME')
    password = config('MAIL_PASSWORD')

    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        pass
    finally:
        server.quit()

