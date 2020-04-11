from lg_spider.spider import lg_spider
from lg_spider.spider import settings
from lg_spider.spider.util import Util


def main():
    kd = "数据"
    # city_no = "p-city_0"

    company_head = getattr(settings, 'COMPANY_CSV_HEAD')
    position_head = getattr(settings, 'POSITION_CSV_HEAD')

    u = Util()

    u.create_csv(getattr(settings, 'COMPANY_CSV_FILE_NAME'), company_head)
    u.create_csv(getattr(settings, 'POSITION_CSV_FILE_NAME'), position_head)

    city_dict = getattr(settings, "CITY")

    for city, city_no in city_dict.items():
        city_no = "p-city_{}".format(city_no)
        print(city)
        print(city_no)
        lg = lg_spider.LgSpider(kd, city_no, city)
        content = lg.start_requests()
        lg.parse(content)


if __name__ == '__main__':
    main()
