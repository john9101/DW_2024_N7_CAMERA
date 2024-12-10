from mysql.connector import Error


class StagingUtil:
    @staticmethod
    def load_into_temporary(temp_table, file_path, column_names, connection):

        try:
            cursor = connection.cursor()
            sql_truncate = f"TRUNCATE TABLE staging.{temp_table}"
            on_local_infile="SET GLOBAL local_infile = 1"
            off_local_infile="SET GLOBAL local_infile = 0"
            sql_load = f"""
            LOAD DATA LOCAL INFILE '{file_path}' INTO TABLE staging.{temp_table}
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            IGNORE 1 ROWS ({column_names})
            """
            cursor.execute(sql_truncate)
            cursor.execute(on_local_infile)
            cursor.execute(sql_load)
            cursor.execute(off_local_infile)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e.msg)
            raise

    @staticmethod
    def transform_temporary_into_daily(resource_id, date, connection):
        try:
            cursor = connection.cursor(dictionary=True)
            if resource_id == 1:
                cursor.callproc("staging.TransformTemporaryIntoDailyKM", (date,))
            elif resource_id == 2:
                cursor.callproc("staging.TransformTemporaryIntoDailyBMD", (date,))
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e.msg)
            raise