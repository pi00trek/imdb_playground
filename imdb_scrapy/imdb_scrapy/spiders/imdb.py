import scrapy
from imdb_scrapy.items import Movies, MovieLoader


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
        A function to scrape movie details for a person in a given role
        Args:
            response:
            role: director/producer/writer/etc. TODO: fill in missing roles (dropdown)

        Returns: json file (feed export) via ItemLoader

        """

        # role = 'archive_footage'

        resp = response.css(f'div[id*="{role}"]')
        for item in resp:
            title = item.css('a::text').get()
            if title is not None:
                if title.lower() == role:
                    pass # first 'a::text' is a role name, hence filtering it out
                else:
                    link = item.css('a::attr(href)').get()

                    loader = MovieLoader(item=Movies(), selector=item)
                    loader.add_value('title', title)
                    loader.add_value('link', link)
                    loader.add_css('year', 'span.year_column::text')

                    add_info = item.css('::text').getall()[4].strip()
                    loader.add_value('extra_info', add_info)
                    # loader.add_css('extra_info', '::text')  # cannot access 4th element via Compose lambda x[4]...

                    if link is not None:
                        link = response.urljoin(link)
                        yield scrapy.Request(link, callback=self.parse_movie_details,
                                             cb_kwargs={'item': loader.load_item()})

    def parse_movie_details(self, response, item):
        loadernext = MovieLoader(item=item, response=response)

        loadernext.add_css('genres', 'div.see-more.inline.canwrap a::text')
        loadernext.add_css('rating', 'div.ratingValue span::text')
        loadernext.add_css('rating_count', 'div.imdbRating span.small::text')
        loadernext.add_css('metacritic_rating', 'div[class*="metacritic"] span::text')
        loadernext.add_css('runtime', '#titleDetails > div:nth-child(23) > time::text')
        loadernext.add_css('budget', '#titleDetails > div:nth-child(12)::text')
        loadernext.add_css('opening_weekend_USA', '#titleDetails > div:nth-child(13)::text')
        loadernext.add_css('gross_USA', '#titleDetails > div:nth-child(14)::text')
        loadernext.add_css('cumulative_world_gross', '#titleDetails > div:nth-child(15)::text')

        yield loadernext.load_item()


# execute(['scrapy', 'crawl', 'imdb'])
