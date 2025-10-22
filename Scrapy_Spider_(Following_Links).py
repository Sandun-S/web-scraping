import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_crawler"
    
    # We only need to tell it where to START
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        
        # --- Part 1: Scrape the data (same as before) ---
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }
            
        # --- Part 2: Find the next link and follow it ---
        
        # 1. Select the 'href' attribute of the 'Next' link
        next_page = response.css('li.next a::attr(href)').get()
        
        # 2. Check if a link was actually found
        if next_page is not None:
            
            # 3. 'yield' a new request to that URL.
            # Scrapy will download it and send the response
            # back to this *same parse function*, creating a loop.
            yield response.follow(next_page, callback=self.parse)