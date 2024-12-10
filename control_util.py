from mysql.connector import Error

class ControlUtil:
    @staticmethod
    def get_config(config_id, connection):
        global cursor
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("control.GetConfig", (config_id,))
            for result in cursor.stored_results():
                data = result.fetchone()
                return data
        except Error as e:
            print(e.msg)
            if connection.is_connected():
                cursor.close()
                connection.close()
            return None


    @staticmethod
    def get_resource(resource_id, connection):
        global cursor
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("control.GetResource", (resource_id,))
            for result in cursor.stored_results():
                data = result.fetchone()
                return data
        except Error as e:
            print(e.msg)
            if connection.is_connected():
                cursor.close()
                connection.close()
            return None

    @staticmethod
    def insert_log(config_id, file_name, file_size, records_count, message, process_id, connection):
        global cursor
        try:
            cursor = connection.cursor()
            cursor.callproc("control.InsertLog", (config_id, file_name, file_size, records_count, message, process_id))
            connection.commit()
            connection.close()
        except Error as e:
            print(e.msg)
            cursor.close()
            connection.close()


    @staticmethod
    def get_log(config_id, process_id, date, connection):
        global cursor
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("control.GetLog", (config_id, process_id, date))
            for result in cursor.stored_results():
                data = result.fetchone()
                return data
        except Error as e:
            print(e.msg)
            if connection.is_connected():
                cursor.close()
                connection.close()
            return None


    @staticmethod
    def update_log(log_id, message, process_id, connection):
        global cursor
        try:
            cursor = connection.cursor()
            cursor.callproc("control.UpdateLog", (int(log_id), str(message), int(process_id)))
            connection.commit()
        except Error as e:
            print(e.msg)
            cursor.close()
            connection.close()

    @staticmethod
    def get_process(process_id, connection):
        global cursor
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("control.GetProcess", (process_id,))
            for result in cursor.stored_results():
                data = result.fetchone()
                return data
        except Error as e:
            print(e.msg)
            if connection.is_connected():
                cursor.close()
                connection.close()
            return None
