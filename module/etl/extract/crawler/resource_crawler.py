from datetime import date
import sys

from module.etl.extract.crawler.bmd_crawler import BMDCrawler
from module.etl.extract.crawler.kyma_crawler import KMCrawler
from control_util import ControlUtil
from util import Util

def crawl_resource_cameras_data(config_id):
    # 1.1 Khởi tạo connection của control database thông qua gọi hàm connect_to_database
    connection = Util.connect_to_database("control")
    # 1.2 Lấy ra config thông qua gọi hàm get_config tương ứng với gọi procedure GetConfig
    config = ControlUtil.get_config(config_id, connection)
    # 1.3 Lấy ra log với config_id và process_id = 1 trong ngày thông qua hàm get_log tương ứng gọi procedure GetLog
    log = ControlUtil.get_log(config_id, 1, date.today(), connection)
    # 1.4 Kiểm tra có lấy thành công log hay không, nếu lấy thành công sẽ không thực hiện còn nếu không thành công thì thực hiện tiếp bước 1.5
    if log is None:
        # 1.5 Lấy ra resource_id từ trong config đã khởi tạo
        resource_id = config.get("resource_id")
        source_file_location = config.get("source_file_location")
        extension = config.get("extension")
        seperator = config.get("seperator")
        format = config.get("format")
        column_names = config.get("column_names")
        resource = ControlUtil.get_resource(resource_id, connection)
        resource_domain = resource.get("domain")
        resource_slug = resource.get("slug")
        resource_name = resource.get("name")
        resource_crawl_url = f'{resource_domain}/{resource_slug}'
        is_crawl_success = True
        data = None
        try:
            # 1.6 Gọi hàm _implement_crawl_resource để thực hiện crawl dữ liệu thô từ resource
            data = _implement_craw_resource(column_names, resource_id,resource_crawl_url)
        except Exception as e:
            print(e)
            is_crawl_success = False

        # 1.7 Kiểm tra crawl thành công hay không, nếu không thành công thì thì thực hiện tiếp bước 1.7.1 còn nếu thành công thì thực hiện tiếp bước 1.7.2
        if is_crawl_success is False:
            created_by = config.get("created_by")
            message = f"Failed crawl data from {resource_name} resource with crawl url: {resource_crawl_url}"
            # 1.7.1 Gửi email thông báo lỗi crawl dữ liệu thô từ resource
            # Util.send_mail("[resource] Failed crawl data", created_by, message, False)
        elif is_crawl_success is True:
            # 1.7.2 Lưu dữ liệu thổ đã crawl vào file csv
            file_size, records_count, file_name  = Util.save_data_into_file(extension, seperator, format, data, source_file_location, resource_name)
            message = f"Successful crawl data from {resource_name} resource with crawl url: {resource_crawl_url}"
            # 1.7.3 Ghi log crawl dữ liệu thô vào file csv thành công thông qua gọi hàm insert_log tương ứng với gọi prodedure InsertLog với proccess_id = 1
            ControlUtil.insert_log(config_id, file_name, file_size, records_count, message, 1, connection)

    else:
        return

def _implement_craw_resource(column_names, resource_id, resource_crawl_url):
    # 1.6.1 Kiểm tra resource_id, nếu resource_id = 1 thì thực hiện tiếp bước 1.6.1.1 còn nếu resource_id = 2 thì thực hiện tiếp bước 1.6.1.2
    if resource_id == 1:
        # 1.6.1.1 Gọi hàm crawl_kyma_cameras để crawl dữ liệu thô của resource có id = 1
        return KMCrawler.crawl_cameras_data(column_names, resource_crawl_url)
    elif resource_id == 2:
        # 1.6.1.2 Gọi hàm crawl_bmd_cameras để crawl dữ liệu thô của resource có id = 2
        return BMDCrawler.crawl_cameras_data(column_names, resource_crawl_url)

if __name__ == '__main__':
    # 1 Gọi hàm crawl_resource_cameras_data với giá trị của tham số config_id trong script
    crawl_resource_cameras_data(sys.argv[1])