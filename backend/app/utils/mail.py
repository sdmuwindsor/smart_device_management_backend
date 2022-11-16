from redmail import outlook
import datetime
class send_mails():
    def send_confirmation_mail(name, to_email):
        outlook.username = "sdm.mac.2022@outlook.com"
        outlook.password = "kYDLu6bs2Wz3jcG"
        
        outlook.send(
            receivers=[to_email],
            subject="Welcome to Smart Device Management",
            text="Hi "+name.title()+"\n\nUnnovate is happy to welcome you to the smart device management solutions.\nHope your journey with us is fruitful.\n\nThank You\nSDM Team"
        )


    def send_report(name, to_email, file_path, device_name, room_name):
        outlook.username = "sdm.mac.2022@outlook.com"
        outlook.password = "kYDLu6bs2Wz3jcG"

        outlook.send(
            receivers=[to_email],
            subject=f"Alert! Anamoly Detected",
            text="Hi "+name.title()+"\n\nThis is an auto generated email.\nThis email is sent to report an anamoly detected by our system for your smart device '"+device_name+"' in '"+room_name+"' room.\nPFA, the anamoly detection report.\n\nThank You\nSDM Team",
            attachments={
                'anamoly.pdf':Path(file_path)
            }
        )
