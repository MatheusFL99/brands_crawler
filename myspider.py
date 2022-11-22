import scrapy
import json


def write_results_file(marcas):
    marcas_ordenadas = sorted(marcas, key=lambda d: d['name'])
    jsonstring = json.dumps(marcas_ordenadas)
    jsonfile = open('marcas.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def urls_brands():
    base_url = 'https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter='
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVXWYZ'
    urls = list()
    for l in alfabeto:
        urls.append(base_url + l)
    return urls


def inside_brands_urls():
    base_url = 'https://www.rankingthebrands.com/'
    with open('marcas.json', encoding='utf-8') as marcas:
        dados = json.load(marcas)
    urls = list()
    for i in dados:
        urls.append(base_url + i['url'])
    return urls


class Spider1(scrapy.Spider):
    name = 'MarcasSpider'
    start_urls = urls_brands()
    marcas = list()

    def parse(self, response):
        for name in response.css('.brandLine'):
            brand = name.css('::text').get()
            link = name.xpath('.//*[@class="list"]/@href').get()

            self.marcas.append({'name': brand, 'url': link})
            yield {'name': brand, 'url': link}

    def close(self, reason):
        write_results_file(self.marcas)


class Spider2(scrapy.Spider):
    name = 'DetailsSpider'
    start_urls = inside_brands_urls()
    marcas = list()

    def parse(self, response):
        for name in response.css('.branddetails-Left'):
            brand = name.css('#ctl00_mainContent_LBBrandName::text').get()
            gbin = name.css('#ctl00_mainContent_LBLGBIN::text').get()
            website = name.css(
                '#ctl00_mainContent_LBBrandWebsite a::attr(href)').get()
            contry = name.css(
                '#ctl00_mainContent_LBCountryOfOrigin::text').get()
            industry = name.css(
                '#ctl00_mainContent_LBBrandIndustry a::text').get()
            image = name.xpath('.//*[@class="brandLogo"]//img/@src').get()

            self.marcas.append(
                {'name': brand, 'GBIN': gbin, 'website': website, 'contry_of_origin': contry, 'industry': industry, 'logo_url': image})
            yield {'name': brand, 'GBIN': gbin, 'website': website, 'contry_of_origin': contry, 'industry': industry, 'logo_url': image}

    def close(self, reason):
        write_results_file(self.marcas)
