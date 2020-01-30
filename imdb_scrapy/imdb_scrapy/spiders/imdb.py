import scrapy
from scrapy.loader import ItemLoader
from scrapy.cmdline import execute
from imdb_scrapy.items import Movies


class Imdb(scrapy.Spider):
    name = "imdb"

    # def __init__(self, *args, **kwargs):
    #     super(Imdb, self).__init__(*args, **kwargs)
    #     self.data = {}

    def start_requests(self):
        urls = [
            'https://www.imdb.com/name/nm0000229/?ref_=nv_sr_srsg_0',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, role='director'):
        """
        A function to get a movie list (not all episodes!!) in given role.
        Args:
            response:
            role: director/producer/writer/etc. TODO: fill in missing roles (dropdown)

        Returns: a list of tuples with movies (titles, link and short info) #TODO: redoing with ItemLoader

        """
        # filmy jako rezyser!!!!!!!!!!!!
        # response.css('div[id*="director"] a::text').getall()

        directed_movies = []
        # def aa():
        #     url = 'https://www.imdb.com/name/nm0000631/?ref_=fn_al_nm_1'

        role = 'director'
        resp = response.css(f'div[id*="{role}"]')
        for item in resp:
            # print(item)
            # print('-----------')
            title = item.css('a::text').get()
            if title.lower() == role:
                pass
            else:
                l = ItemLoader(item=Movies(), selector=item, response=response)
                l.add_css('title', 'a::text')
                l.add_css('link', 'a::attr(href)')
                l.add_css('year',
                          'span.year_column::text')  # TODO: fix the year formatting (e.g. xa02014/III or 'from ..to..')
                l.add_css('extra_info', '::text')  # TODO: get fourth element (from getall() list)
                l.load_item()
                print('-------')
                break

                # link = item.css('a::attr(href)').get()
                # # print(item.css('a::attr(href)').getall())
                # year = item.css('span.year_column::text').get().split('\n')[
                #     1]
                # # print(item.css('span.year_column::text').getall())
                # extra_info = item.css('::text').getall()[4]
                # # print(item.css('::text').getall())
                #
                # directed_movies.append((title, link, year, extra_info))
                # # return l.load_item()

        # print(directed_movies)

        # yield directed_movies
        #     yield l.load_item()

    #     for link in directed_movies:
    #         next_page = link[1]
    #         if next_page is not None:
    #             next_page = response.urljoin(next_page)
    #             yield scrapy.Request(next_page, callback=self.parse_movie_details)
    #         #     print(self.data)
    #
    # def parse_movie_details(self, response):
    #
    #     genre_resp = response.css('div.see-more.inline.canwrap a::text').getall()
    #     genres = [i.strip() for i in genre_resp if not (i == ' ' or i[:5] == 'See A')]  # TODO: redo with regex
    #     # self.data[movie_title] = self.data[movie_title] + genres

# execute(['scrapy', 'crawl', 'imdb'])
