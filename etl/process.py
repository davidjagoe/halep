
import sys

from scrapy.selector import Selector


# The structure of the html document from GameTime is stupid and
# crazy. The method to extract player names is to find the rows
# corresponding to a timeslot, and then read across the row,
# extracting the names. There are five courts, each which will have 0
# or more names.

# TODO:

# 1. Make more robust against changing timeslots (differ on weekends
#    and by season (?))
# 
# 2. Classify the type of booking (lesson, ball machine, league,
#    clinic...) based on background image/color.


TIMES = ("5:45 am", "7:00 am", "8:15 am", "9:30 am", "10:45 am",
         "12:00 pm", "1:15 pm", "2:30 pm", "3:45 pm", "5:00 pm",
         "6:15 pm", "7:30 pm", "8:45 pm")

TD_BACKGROUND_TO_COURT_USAGE_LOOKUP = {
    "1.gif": "regular",
    "11.gif": "regular",
    "2.gif": "league",
    "44.gif": "other",
    "4-b.gif": "lesson",
    "5.gif": "clinic",
    "8.gif": "ballmachine",
}

def main(filename=None):
    if filename is None:
        filename = "GameTime.html"
    with open(filename) as f:
        data = f.read()

    # 1. Find a table at any depth
    # 2. Below that a td containing the time text
    # 3. Go up to the parent row
    # --> Now we have the row containing court bookings
    # 4. find all td's without the class 'g' (which is grid formatting (!!!))
    # 5. In this example I'm processing the first data cell (after the time data cell)
    # 6. Get all text below that point
    # --> Returns an array of text

    xpath_query_template = "//table//td[contains(text(), '{0}')]/parent::tr/td[not (@class='g')][{1}]"#//text()"

    for time in TIMES:
        for slot in range(2, 7):
            query = xpath_query_template.format(time, slot)

            td_selector = Selector(text=data).xpath(query)
            background = td_selector.xpath("@background").extract_first()
            if background is not None:
                background = background.split("/")[-1]

            court_usage = TD_BACKGROUND_TO_COURT_USAGE_LOOKUP.get(background, "unspecified")

            names_selector = td_selector.xpath(".//text()")
            names = names_selector.extract()
            names = [n.strip() for n in names if len(n.strip()) > 0]
            print court_usage, names
        print
        print

#("//table//td[contains(text(), '7:00 am')]/parent::tr/td[not (@class='g')][2]//text()")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

