import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector
import xml.etree.ElementTree as ET
from mysql.connector import Error
from os.path import dirname, join
import smtplib

from numpy.compat import os_fspath


class Util:
    @staticmethod
    def get_config_of_database_in_xml(db_name):
        config_file = join(dirname(__file__), 'config.xml')
        tree = ET.parse(config_file)
        root = tree.getroot()
        element_db = root.find(f".//database[@name='{db_name}']")
        if element_db is not None:
            comfig_of_db = {
                "host": root.find(".//database/host").text,
                "port": root.find(".//database/port").text,
                "database": root.find(".//database/db_name").text,
                "user": root.find(".//database/user").text,
                "password": root.find(".//database/password").text,
                "allow_local_infile": True
            }
            return comfig_of_db
        else:
            # print(f"Không tìm thấy cấu hình database với {db_name}")
            return None

    @staticmethod
    def connect_to_database(db_name):
        try:
            db_config = Util.get_config_of_database_in_xml(db_name)
            if db_config:
                connection = mysql.connector.connect(**db_config)
                if connection.is_connected():
                    print(f"Kết nối thành công tới '{db_name}' database")
                    return connection
        except Error as e:
            print("Lỗi khi kết nối tới '{}' database:", e)

    @staticmethod
    def send_mail(subject, mail_recipient, content, is_html):
        mail_sender =  os.getenv("MAIL_SENDER")
        mail_server = os.getenv("MAIL_SERVER")
        mail_port = int(os.getenv("MAIL_PORT"))
        mail_password = os.getenv("MAIL_PASSWORD")

        try:
            message = MIMEMultipart()
            message["From"] = mail_sender
            message["To"] = mail_recipient
            message["Subject"] = subject
            body_content = MIMEText(content, "html" if is_html else "plain")
            message.attach(body_content)

            with smtplib.SMTP(mail_server, mail_port) as server:
                server.starttls()
                server.login(mail_recipient, mail_password)
                server.sendmail(mail_server, mail_recipient, message.as_string())
        except Exception as e:
            return f"Failed to send email: {e}"






