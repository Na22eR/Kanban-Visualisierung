import smtplib
import ssl


tlsContext = ssl.create_default_context()
defaultSMTP = 'smtp.gmail.com'
defaultPort = 587


def sendEMail(username, password, text, subject, mFrom, mTo):
    server = smtplib.SMTP(defaultSMTP, defaultPort)
    server.starttls(context=tlsContext)
    server.login(username, password)
    data = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (mFrom, mTo, subject, text)
    server.sendmail(mFrom, mTo, data.encode('utf-8'))
    server.quit()

    print('Mail sent! :)')


# Main Methode
if __name__ == '__main__':

    sendEMail('kanban.rational@gmail.com', 'wRNrXpGmezzWQjfc', "Teeeäst", "Python sagt Hi", "<kanban.rational@gamil.com>", "<na22er.yacine@gmail.com>")


