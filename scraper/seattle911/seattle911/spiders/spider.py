"""
"http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?incDate=1%2F24%2F2015&rad1=des
"""


from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from seattle911.items import Seattle911Item


# TODO: rewite this to make sense even though it works
def day_finder(month, year):
    is_leap_year = (0 if (year % 4) or ((year % 100 == 0) and (year % 400))
                    else 1)
    days_in_month = ((28 + is_leap_year) if (month == 2)
                     else 31 - (month - 1) % 7 % 2)
    return days_in_month


months = range(1, 13)
years = range(2004, 2015)

base_url = "http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?incDate="

starts_urls = []

for year in years:
    for month in months:
        for day in range(day_finder(month, year) + 1):
            start_url = (base_url + str(month) + "%2F"
                         + str(day) + "%2F" + str(year) + "&rad1=des")
            starts_urls.append(start_url)


class MySpider(Spider):

    name = "seattle911"
    allowed_domains = ["www2.seattle.gov/fire/realtime911/"]

    start_urls = starts_urls

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.xpath('//tr')
        items = []
        for row_num, row in enumerate(rows):
            if row_num >= 5:
                item = Seattle911Item()
                item['date'] = row.xpath("td[1]/text()").extract()
                item['incident_number'] = row.xpath("td[2]/text()").extract()
                item['units'] = row.xpath("td[4]/text()").extract()
                item['location'] = row.xpath("td[5]/text()").extract()
                item['_type'] = row.xpath("td[6]/text()").extract()
                items.append(item)
        return items
