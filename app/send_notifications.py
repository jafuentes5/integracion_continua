import base64
import time
import mysql.connector
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def read_database():
    try:
        #Se realiza conexión y se ejecutan las consultas correspondientes
        cnx = mysql.connector.connect(user='root', database='notifications', host='localhost', password='prueba2024*')
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from host_notifications where notification_status = 'not send'")
        cursor.execute(query)
        for data in cursor:
            #Se envian mensajes con los datos obtenidos de la base de datos
            print(data)
            send_message()
    except Exception as e:
        print(str(e))
    finally:
        cursor.close()
        cnx.close()
    
def send_message():
    try:
        #Se definen los alcances del api en cuestion
        SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        
        #Se intentan obtener las credenciales del token
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        #Se guardan los datos para la siguiente conexión
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        
        #Se instancia el servicio de gmail para el envio del correo
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()
        message.set_content("Test\prueba\n\neste texto va despues de 2 saltos de linea")
        message["To"] = "jafuentes5@poligran.edu.co"        
        message["Subject"] = "Nagios Alert"

        #Se codifica el mensaje y se envia
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        return True
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    #Se lee la base de datos y se envian mensajes
    while True:
        read_database()
        time.sleep(10)