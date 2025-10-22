import scrapy

class LoginSpider(scrapy.Spider):
    name = 'login_spider'
    login_url = 'http://quotes.toscrape.com/login'
    
    # 1. We start by defining this method instead of start_urls
    def start_requests(self):
        # We start by just visiting the login page
        yield scrapy.Request(self.login_url, callback=self.parse_login)

    # 2. This function is called when we get the login page
    def parse_login(self, response):
        # Here, we 'fill out' the form and submit it.
        # We'll use a special FormRequest for this.
        # It needs to know our username and password.
        
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                # What goes in here?
                'username': 'my_test_user',
                'password': 'my_test_password'
            },
            callback=self.parse_after_login
        )

    # 3. If login is successful, this function gets the page
    #    that we are redirected to.
    def parse_after_login(self, response):
        # We can check if we see a 'Logout' link to confirm
        if response.css('a[href="/logout"]'):
            print("--- LOGIN SUCCESSFUL ---")
            
            # Now we can scrape the page just like before
            for quote in response.css('div.quote'):
                yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                }
        else:
            print("--- LOGIN FAILED ---")