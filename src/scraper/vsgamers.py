from scraper.common import ScrapeResult, Scraper, ScraperFactory
import json


class VSGamersResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.select_one('div.vs-product-header-top > h1')
        print(tag.text)
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('#vs-product-sheet-dashboard > div.dashboard > vs-product-dashboard')
        tag = str(json.loads(tag["data"])["price"])
        print(tag)
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'

        # check for add to cart button
        tag = self.soup.body.select_one('div.dashboard > vs-product-dashboard')
        stock = json.loads(tag["data"])["stock"]
        tag = True if stock > 0 else False
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class VSGamersScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'vsgamers'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return VSGamersResult
