from datetime import date

from module.etl.extract.crawler.bmd_crawler import BMDCrawler
from module.etl.extract.crawler.kyma_crawler import KMCrawler
from control_util import ControlUtil
from util import Util

def crawl_resource_cameras_data(config_id):
    connection = Util.connect_to_database("control")
    config = ControlUtil.get_config(config_id, connection)
    resource_id = config.get("resource_id")
    resource = ControlUtil.get_resource(resource_id, connection)
    resource_domain = resource.get("domain")
    resource_slug = resource.get("slug")
    resource_crawl_url = f'{resource_domain}/{resource_slug}'
    resource_name = resource.get("name")
    log = ControlUtil.get_log(config_id, 1, date.today(), connection)
    if log is None:
        try:
            file_name, file_size, records_count = _implementCrawlResource(config, resource_id, resource_name,resource_crawl_url)
            message = f"Successful crawl data from {resource_name} resource with crawl url: {resource_crawl_url}"
            ControlUtil.insert_log(config_id, file_name, file_size, records_count, message, 1, connection)
        except Exception as e:
            print(e)
            created_by = config.get("created_by")
            message = f"Failed crawl data from {resource_name} resource with crawl url: {resource_crawl_url}"
            Util.send_mail("[resource] Failed crawl data", created_by, message, False)
    else:
        return

def _implementCrawlResource(config, resource_id, resource_name, resource_crawl_url):
    if resource_id == 1:
        return KMCrawler.crawl_cameras_data(config, resource_name, resource_crawl_url)
    elif resource_id == 2:
        return BMDCrawler.crawl_cameras_data(config, resource_name, resource_crawl_url)



if __name__ == '__main__':
    # crawl_resource_cameras_data(sys.argv[1]
    crawl_resource_cameras_data(1)