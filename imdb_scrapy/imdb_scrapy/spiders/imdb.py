import scrapy
from scrapy.loader import ItemLoader
from scrapy.cmdline import execute
from imdb_scrapy.items import Movies
# from imdb_scrapy.imdb_scrapy.items import Movies


class Imdb(scrapy.Spider):
    name = "imdb"

    def start_requests(self):
        urls = [
            'https://www.imdb.com/name/nm0005363/?ref_=fn_al_nm_1',
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

        role = 'director'
        resp = response.css(f'div[id*="{role}"]')
        for item in resp:
            title = item.css('a::text').get()
            if title.lower() == role:
                pass
            else:
                movie_link = item.css('a::attr(href)').get()
                l = ItemLoader(item=Movies(), selector=item, response=response)
                l.add_value('title', title)
                l.add_value('link', movie_link)
                l.add_css('year',
                          'span.year_column::text')  # TODO: fix the year formatting (e.g. xa02014/III or 'from ..to..')
                l.add_css('extra_info', '::text')  # TODO: get fourth element (from getall() list)

                if movie_link is not None:
                    movie_link = response.urljoin(movie_link)
                    yield scrapy.Request(movie_link, callback=self.parse_movie_details,
                                         meta={'item': l.load_item()})

    def parse_movie_details(self, response):
        loadernext = ItemLoader(item=response.meta['item'], response=response)

        genre_resp = response.css('div.see-more.inline.canwrap a::text').getall()
        genres = [i.strip() for i in genre_resp if not (i == ' ' or i[:5] == 'See A')]  # TODO: redo with regex
        loadernext.add_value('genres', genres)

        loadernext.add_css('rating', 'div.ratingValue span::text')
        loadernext.add_css('rating_count', 'div.imdbRating span.small::text')
        loadernext.add_css('metacritic_rating', 'div[class*="metacritic"] span::text')

        yield loadernext.load_item()


# execute(['scrapy', 'crawl', 'imdb'])