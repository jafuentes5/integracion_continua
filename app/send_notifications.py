import sys
import base64
import time
import mysql.connector
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#Se define diccionario con las propiedades de conexión
connection_config = {
    "user":"root",
    "database":"notifications",
    #"host":"localhost",
    "host":"mysql-container",
    "password":"prueba2024*",
    "port":3306
}

#Se define metodo para lectura de la base de datos
def read_database():
    cursor = None
    cnx = None
    try:
        #Se realiza conexión y se ejecutan las consultas correspondientes
        cnx = mysql.connector.connect(**connection_config)
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from nagios_notifications where notification_status = 'not send'")
        cursor.execute(query)
        records = cursor.fetchall()
        if len(records)>0:
            return True, False, records
        else:
            return True, True
    except Exception as e:        
        return False, str(e)
    finally:
        cursor.close()
        cnx.close()
    
def update_database(record_id):
    cursor = None
    cnx = None
    record_id = (record_id,)
    try:
        #Se realiza conexión y se ejecutan las consultas correspondientes
        cnx = mysql.connector.connect(**connection_config)
        cursor = cnx.cursor(buffered=True)
        query = ("UPDATE nagios_notifications set notification_status = 'sent' where notification_id = %s")
        cursor.execute(query, record_id)
        cnx.commit()
        return True
    except Exception as e:
        return(str(e))        
    finally:
        cursor.close()
        cnx.close()

def send_message(notification_type, hostname, hoststate = None, hostoutput=None, servicestate = None, serviceoutput = None, datetime = None):
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
        message["To"] = "jafuentes5@poligran.edu.co"
        if hoststate != None:        
            message["Subject"] = f"** {notification_type} Host Alert: {hostname} Status is {hoststate} **"
            message.set_content(f"Notification type: {notification_type}\nHost Name: {hostname}\nHost State: {hoststate}\nAdditional info: {hostoutput}\n\nDate: {str(datetime)}")
        else:
            message["Subject"] = f"** {notification_type} Service Alert: {hostname} Status is {servicestate} **"
            message.set_content(f"Notification type: {notification_type}\nHost Name: {hostname}\Service State: {servicestate}\nAdditional info: {serviceoutput}\n\nDate: {str(datetime)}")
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
        return(str(e))

if __name__ == "__main__":
    #Se lee la base de datos y se envian mensajes
    while True:        
        result_read_database = read_database()
        #Si el proceso es satisfactorio y retorna datos continua
        if result_read_database[0] == True and result_read_database[1] == False:
            records = result_read_database[2]
            for record in records:
                #Se intenta enviar mensaje de notificacion por correo                
                result_send_message = send_message(*record[1:8])
                if result_send_message == True:
                    #Se actualiza el registro en la base de datos para indicar que se envio el mensaje
                    result_update_record = update_database(record[0])
                    if result_update_record != True:
                        print(f"Ocurrio el siguiente error mientras se intentaba actualizar el registro:\n\nError: {result_send_message}\n\nEl programa no podrá continuar...")
                        sys.exit(1)
                else:
                    print(f"Ocurrio el siguiente error mientras se intentaba enviar el mensaje:\n\nError: {result_send_message}\n\nEl programa no podrá continuar...")
                    sys.exit(1)
            print("Espera 10 segundos antes de conectarse nuevamente a la base de datos")
            time.sleep(10)
        #Continua el flujo del proceso
        elif result_read_database[0] == True and result_read_database[1] == True:
            print("Espera 10 segundos antes de conectarse nuevamente a la base de datos")
            time.sleep(10)
        else:
            print(f"Ocurrio el siguiente error mientras se intentaba leer la base de datos:\n\nError: {result_read_database[1]}\n\nEl programa no podrá continuar...")
            sys.exit(1)