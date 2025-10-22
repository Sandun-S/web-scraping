import scrapy

# A spider is a class that defines how to crawl a site
class QuotesSpider(scrapy.Spider):
    # This name must be unique within a project
    name = "quotes_spider"
    
    # These are the URLs the spider will start with
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # This is the main function that Scrapy calls 
    # to process each downloaded page (response).
    def parse(self, response):
        
        # We use CSS selectors (just like in Beautiful Soup)
        # to find all 'div' elements with the class 'quote'
        for quote in response.css('div.quote'):
            
            # We extract the text from child elements
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            
            # 'yield' is like 'return', but it sends the data
            # back to Scrapy to be collected without stopping the function.
            yield {
                'text': text,
                'author': author,
            }
            #run this by : scrapy runspider quotes_spider.py -o quotes.json