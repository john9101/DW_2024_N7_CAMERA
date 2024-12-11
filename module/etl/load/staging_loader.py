from control_util import ControlUtil
from staging_util import StagingUtil
from util import Util


def load_into_temporary(date, config_id):
    control_connection = Util.connect_to_database("control")
    staging_connection = Util.connect_to_database("staging")
    config = ControlUtil.get_config(config_id, control_connection)
    log = ControlUtil.get_log(config_id, 1, date, control_connection)
    if log:
        log_id = log.get('id')
        file_name = log.get("file_name")
        temp_table = config.get('dest_temp_table_staging')
        source_file_location = config.get("source_file_location")
        file_path = f"{source_file_location}/{file_name}"
        column_names = config.get("column_names")
        pre_process_message = log.get("message")
        ep_message = f"Executing load data from {file_path} file into {temp_table} table"
        ControlUtil.update_log(log_id, ep_message, 15, control_connection)
        try:
            StagingUtil.load_into_temporary(temp_table, file_path, column_names, staging_connection)
            message = f"Successful load data from {file_path} file into {temp_table} table"
            ControlUtil.update_log(log_id, message, 2, control_connection)
        except Exception as e:
            print(e)
            ControlUtil.update_log(log_id, pre_process_message, 1, control_connection)
            created_by = config.get('created_by')
            message = f"Failed load data from {file_path} file into {temp_table} table"
            Util.send_mail("[staging] Failed load data", created_by, message, False)
    else:
        return

if __name__ == '__main__':
    load_into_temporary("2024/12/10", 1)
