from redmail import outlook
import datetime
class send_mails():
    def send_confirmation_mail(name, to_email):
        outlook.username = "sdm.mac.2022@outlook.com"
        outlook.password = "kYDLu6bs2Wz3jcG"
        
        outlook.send(
            receivers=[to_email],
            subject="Welcome to Smart Device Management",
            text="Hi "+name+"\n\nUnnovate is happy to welcome you to the smart device management solutions.\nHope your journey with us is fruitful.\n\nThank You\nSDM Team"
        )


    def send_report(name,to_email,file_path):
        outlook.username = "sdm.mac.2022@outlook.com"
        outlook.password = "kYDLu6bs2Wz3jcG"
        #now = string(datetime.datetime.now()).split('.')[0]
        outlook.send(
            receivers=[to_email],
            subject="Anamoly Detection Report",
            text="Hi "+name+"\n\nUnnovate is happy to welcome you to the smart device management solutions.\nHope your journey with us is fruitful.\n\nThank You\nSDM Team"
        )
