from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import scrapy  # https://docs.scrapy.org/en/latest/
from scrapy.exceptions import CloseSpider  # https://docs.scrapy.org/en/latest/


def checkforrobot(file):
    """
    extracts robots meta tag for a given html file
    :return: boolean values for index, follow
    """
    soup = BeautifulSoup(file, "html.parser")
    robots_meta = soup.find(name='meta', attrs={
        'name': lambda v: v and v.lower() == 'robots'
    })
    if robots_meta is None:
        return [True, True]
    robots_content = robots_meta['content']
    robots_content = robots_content.split(sep=',')
    if robots_content is None:
        return [True, True]
    if robots_content[0].strip() == 'index' and robots_content[1].strip() == 'follow':
        return [True, True]
    if robots_content[0] == 'noindex' and robots_content[1] == 'follow':
        return [False, True]
        # print(return_values)
    if robots_content[0].strip() == 'index' and robots_content[1].strip() == 'nofollow':
        return [True, False]
    if robots_content[0].strip() == 'noindex' and robots_content[1].strip() == 'nofollow':
        return [False, False]
    print(robots_content, robots_meta)


class MySpider(scrapy.Spider):
    """
    web crawler that starts at https://www.concordia.ca/ginacody.html and only crawls concordia domains
    :param num_pages: set the number of pages to be downloaded
    :param download_delay: set the delay between downloads
    """
    name = 'final_project'
    start_urls = ['https://www.concordia.ca/ginacody.html']
    allowed_domains = ['www.concordia.ca']
    num_pages = 50
    download_delay = 0.5
    custom_settings = {
        # 'DEPTH_PRIORITY': 0,
        # 'DEPTH_LIMIT' : 0,
        'ROBOTSTXT_OBEY': True
    }

    def parse(self, response, **kwargs):
        if self.num_pages <= 0:
            raise CloseSpider('Number of pages to be scraped limit reached. ')
        else:
            index, follow = checkforrobot(response.body)
            if response.url.endswith('html') and index:
                filename = response.url.split("/")[-1]
                with open('Files/' + str(self.num_pages) + '_' + filename, 'wb') as f:
                    f.write(response.body)
                    print(filename)
                    print(self.num_pages)
                f.close()
                # print(self.item_count)
                self.num_pages -= 1
                for href in response.xpath('//a/@href').getall():
                    if href.endswith('html') and follow:
                        yield scrapy.Request(response.urljoin(href), self.parse)
