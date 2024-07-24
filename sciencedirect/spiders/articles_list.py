import scrapy
from sciencedirect.items import Article


class ArticlesScraper(scrapy.Spider):
    name = "articles_list"

    base_url = 'https://www.sciencedirect.com'
    results_per_page = 100
    default_keywords = ['radial', 'artery', 'occlusion']

    def __init__(self, *args, **kwargs):
        super(ArticlesScraper, self).__init__(*args, **kwargs)
        arg_keywords = getattr(self, 'keywords')
        if arg_keywords:
            self._keywords = arg_keywords.split(',')
        else:
            self._keywords = self.default_keywords
        self._position = 0
        self._page = 0

    def _build_url(self):
        offset = self._page * self.results_per_page
        base_url = self.base_url
        qs = ' '.join(self._keywords)
        return f'{base_url}/search/?qs={qs}&show={self.results_per_page}&offset={offset}'

    def start_requests(self):
        # if there were passed other keywords
        keywords = getattr(self, 'keywords', None)
        if keywords is not None:
            keywords = keywords.split(',')
            self._keywords = keywords

        url = self._build_url()
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items_list_path = '//ol[contains(@class, "search-result-wrapper")]/li[not(contains(@class, "Login"))]'
        for li in response.xpath(items_list_path):
            for article in self._parse_item_as_li(li):
                yield article

        next_page = response.xpath('//div[contains(@class, "SearchNavigation")]//li[contains(@class, "next-link")]/a')
        if next_page:
            self._page += 1
            url = self._build_url()
            yield scrapy.Request(url=url, callback=self.parse)

    def _parse_item_as_li(self, li):
        item = Article()

        item['article_type'] = li.xpath(".//span[contains(@class, 'article-type')]/text()").get()
        item['access'] = False if li.xpath(".//span[contains(@class, 'access-indicator-no')]").get() else True
        item['access_label'] = li.xpath(".//span[contains(@class, 'access-label')]/text()").get()
        item['title'] = ''.join(li.xpath(".//h2/a[contains(@class, 'title')]//text()").extract())
        item['url'] = '{}/{}'.format(self.base_url, li.xpath(".//h2/a[contains(@class, 'title')]").attrib['href'])

        src = li.xpath(".//div[contains(@id, 'srctitle')]")
        if src:
            src = src[0]
            item['src_title'] = src.xpath(".//a[contains(@class, 'srctitle')]/span/text()").get()
            src_url = src.xpath(".//a[contains(@class, 'srctitle')]").attrib['href']
            item['src_url'] = '{}/{}'.format(self.base_url, src_url)
            extra = [
                t.strip()
                for t in src.xpath(".//span/text()").extract()
                if t.strip() not in (',', item['src_title'].strip())
            ]
            item['src_extra'] = ', '.join(extra)
        else:
            item['src_title'] = 'n/a'
            item['src_url'] = 'n/a'
            item['src_extra'] = 'n/a'

        ol_authors = li.xpath('.//ol[contains(@class, "Authors")]')
        if ol_authors:
            ol_authors = ol_authors[0]
            item['authors'] = ', '.join(ol_authors.xpath('.//span[contains(@class, "author")]/text()').extract())
        else:
            item['authors'] = 'n/a'

        self._position += 1
        item['out_position'] = self._position

        yield item

