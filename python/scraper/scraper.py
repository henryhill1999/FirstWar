import re
import sys
import os
from os import mkdir, listdir
from os.path import join, dirname, realpath, isdir, isfile
import time

from io import open as iopen
import json
import requests
import shutil
import time
import random

from .dates import dates_in_range

current_dir = dirname(realpath('__file__'))

in_path_template = join(current_dir, 'downloaded/{date}/jp2/{n}')
in_dir_template = join(current_dir, 'downloaded/{date}/jp2')

out_path_template = join(current_dir, 'downloaded/{date}/jpg/{n}.jpg')
out_dir_template = join(current_dir, 'downloaded/{date}/jpg')


def fill_empty_dirs(url: str, save_path: str):
    empty = find_empty_dirs(save_path)

    run(url, save_path, empty)


def find_empty_dirs(save_path: str):
    missing = []

    for d in listdir(save_path):
        if not isdir(join(save_path, d)):
            continue
        if not isdir(join(save_path, d, 'jp2')):
            continue

        in_dir = in_dir_template.format(date=d)

        if len(listdir(in_dir)) is 0:
            missing.append(d)

    print(f'Found {len(missing)} empty dirs in {save_path}')
    print(missing)
    return missing


def run(url: str, save_path: str, dates: list):

    print()
    num_total_pages = 0
    num_dates = 0

    start_time = time.time()

    for date in dates:

        pages = download_pages_from_date(url, date)

        num_total_pages += len(pages)
        num_dates += 1

        t_elapsed = time.time()-start_time

        print(f'Downloaded {num_total_pages} pages from {num_dates} date(s) ' +
              f'in {readable_seconds(t_elapsed)}')

        estimated_pages_remaining = int(
            (num_total_pages / num_dates) * (len(dates) - num_dates))

        estimated_time_remaining = int(estimated_pages_remaining *
                                       (num_total_pages/t_elapsed))

        print(f'Estimated {readable_seconds(estimated_time_remaining)} ' +
              f'({estimated_pages_remaining} pages) remaining')

        dir_path = f'{save_path}/{date}'
        write_pages_to_disk(dir_path, pages)

        print(f'Pages saved to {dir_path}/jp2')
        print()

    print()
    print(f'Downloaded {num_total_pages} pages from {num_dates} dates')
    print()
    return


def readable_seconds(s):

    units = {"seconds": 1,
             "minutes": 60,
             "hours": 3600,
             "days": 86400,
             "weeks": 604800}

    raw = {u: int(s/n) for (u, n) in units.items()}

    res = ''

    if raw['weeks'] > 0:
        res += f'{raw["weeks"]} weeks, '

    if raw['days'] > 0:
        res += f'{raw["days"]-raw["weeks"]*7} days, '

    if raw['hours'] > 0:
        res += f'{raw["hours"]-raw["days"]*24} hours, '

    if raw['minutes'] > 0:
        res += f'{raw["minutes"]-raw["hours"]*60} minutes, '

    res += f'{raw["seconds"]-raw["minutes"]*60} seconds'

    return res


def download_pages_from_date(url, date):
    # base...{date}/ed-1/seq-{{seq}}.jp2
    date_url = url.format(date=date)

    pages = []

    seq = 1

    while True:
        # base.../ed-1/seq-{seq}.jp2
        url = date_url.format(seq=seq)

        # example: https://chroniclingamerica.loc.gov/lccn/sn83030431/1916-12-28/ed-1/seq-2.jp2
        # print(url)

        response = get_a_page(url)
        if response is None:
            break

        else:
            seq += 1
            pages.append(response)

            # add a break to only get the front page
            # break

    print(f'Received {len(pages)} pages from {date}')
    return pages


def get_a_page(url: str):
    try:
        # time.sleep(0.5)
        response = requests.get(url)

        # valid response
        if response.status_code == 200:
            return response

        # expected as indication that there are no more pages for a given date
        elif response.status_code == 404:
            print('no reponse from {url}')
            return None

        # busy server error
        elif response.status_code == 503:
            print('server busy, trying again')
            time.sleep(1)
            return get_a_page(url)

        # other response
        else:
            print(f'unknown status code received: {response.status_code}')
            return None

    except Exception as e:
        print(f'Exception while getting content: {str(e)}')
        return None


def write_pages_to_disk(dir_path: str, pages: list):
    try:
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        if not os.path.isdir(f'{dir_path}/jp2'):
            os.mkdir(f'{dir_path}/jp2')

        for (i, page) in enumerate(pages):
            with iopen(f'{dir_path}/jp2/{i}.jp2', 'wb') as out_file:
                out_file.write(page.content)

    except Exception as e:
        print(f'Exception while writing to disk: {str(e)}')
