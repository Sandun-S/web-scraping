from booking.booking import Booking

try:
    with Booking(teardown=True) as bot:
        bot.land_first_page()
        bot.change_currency(currency='LKR')
        bot.select_place_to_go(input("Where you want to go ?\n> "))
        bot.select_dates(
            check_in_date=input("What is the check in date? (YYYY-MM-DD)\n> "),
            check_out_date=input("What is the check out date? (YYYY-MM-DD)\n> ")
        )
        bot.select_adults(int(input("How many people ?\n> ")))
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh() # A workaround to let our bot to grab the data properly
        bot.report_results()

except Exception as e:
    # We removed the 'in PATH' check because webdriver-manager
    # makes that error impossible. We'll just print any other
    # error that might happen.
    print("An error occurred. Make sure your inputs are correct (e.g., date format).")
    print("\nError details:")
    print(e)
    raise
