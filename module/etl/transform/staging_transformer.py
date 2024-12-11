from control_util import ControlUtil
from staging_util import StagingUtil
from util import Util

def transform_temporary_into_daily(date, config_id):
    control_connection = Util.connect_to_database("control")
    staging_connection = Util.connect_to_database("staging")
    config = ControlUtil.get_config(config_id, control_connection)
    log = ControlUtil.get_log(config_id, 2, date, control_connection)
    if log:
        log_id = log.get('id')
        daily_table = config.get("dest_daily_table_staging")
        temp_table = config.get('dest_temp_table_staging')
        resource_id = config.get('resource_id')
        pre_process_message = log.get('message')
        ep_message = f"Executing transform {temp_table} table into {daily_table} table"
        ControlUtil.update_log(log_id, ep_message, 16, control_connection)
        try:
            StagingUtil.transform_temporary_into_daily(resource_id, date, staging_connection)
            message = f"Successful transform {temp_table} into {daily_table}"
            ControlUtil.update_log(log_id, message, 3, control_connection)
        except Exception as e:
            print(e)
            ControlUtil.update_log(log_id, pre_process_message, 2, control_connection)
            created_by = config.get('created_by')
            message = f"Failed transform {temp_table} into {daily_table}"
            Util.send_mail("[staging] Failed transform", created_by, message, False)
    else:
        return

if __name__ == '__main__':
    transform_temporary_into_daily("2024/12/10", 2)