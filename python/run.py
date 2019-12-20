from scraper import scraper, dates
import random

if __name__ == '__main__':

    # ${YYYY}-${MM}-${DD}/ed-1/seq-${N}.jp2

    # sun -1916     sn83030272
    # sun 1916-1920 sn83030431

    # through 1916
    # url = "https://chroniclingamerica.loc.gov/lccn/sn83030272/{date}/ed-1/seq-{{seq}}.jp2"

    # July 1916
    # url = "https://chroniclingamerica.loc.gov/lccn/sn83030430/{date}/ed-1/seq-{{seq}}.jp2"

    # post July 1916
    url = "https://chroniclingamerica.loc.gov/lccn/sn83030431/{date}/ed-1/seq-{{seq}}.jp2"

    save_path = "./downloaded"
    start_date = (1900, 1, 1)
    end_date = (1920, 1, 1)

    toSample = dates.dates_in_range(start_date, end_date)
    # sample = random.sample(toSample, 500)

    # scraper.fill_empty_dirs(url, save_path)
    # scraper.run(url, save_path, sample)
