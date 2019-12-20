from PIL import Image
import time

from os import mkdir, listdir
from os.path import join, dirname, realpath, isdir, isfile
from io import open as iopen

current_dir = dirname(realpath('__file__'))

in_path_template = join(current_dir, 'downloaded/{date}/jp2/{n}')
in_dir_template = join(current_dir, 'downloaded/{date}/jp2')

out_path_template = join(current_dir, 'downloaded/{date}/jpg/{n}.jpg')
out_dir_template = join(current_dir, 'downloaded/{date}/jpg')


def find_unconverted_images():
    images = []

    downloaded = join(current_dir, 'downloaded')
    for d in listdir(downloaded):
        if not isdir(join(downloaded, d)):
            continue
        if not isdir(join(downloaded, d, 'jp2')):
            continue

        in_dir = in_dir_template.format(date=d)

        for n in listdir(in_dir):
            path = join(in_dir, n)

            if not isfile(path):
                continue

            if n[0] == '.':
                continue

            in_path = in_path_template.format(date=d, n=n)
            out_path = out_path_template.format(date=d, n=n[:-4])

            if isfile(out_path):
                continue

            images.append({
                'date': d,
                'n': n[:-4],
                'in_path': in_path,
                'out_path': out_path})

    return images


def convert_jp2_to_jpg(in_path, out_path):
    Image.open(in_path).save(out_path, 'JPEG')


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


def convert_all():
    images = find_unconverted_images()

    start_time = time.time()
    n_converted = 0

    print()
    print(f'Found {len(images)} unconverted images')
    print()
    print('converting...')
    print()

    while len(images) > 0:

        i = images[0]

        out_dir = out_dir_template.format(date=i['date'])

        if not isdir(out_dir):
            mkdir(out_dir)

        convert_jp2_to_jpg(i['in_path'], i['out_path'])

        n_converted += 1
        t_elapsed = time.time()-start_time

        t_avg = t_elapsed/n_converted

        print(
            f'Converted {n_converted} image(s) in {readable_seconds(t_elapsed)}')
        print(f'Avg {t_avg} seconds/image')

        images = find_unconverted_images()
        print(
            f'Estimated {readable_seconds(t_avg*len(images))} ' +
            f'({len(images)} images) remaining')
        print()

    print('All detected files have been converted')
    print(f'Total time: {readable_seconds(t_elapsed)}')


convert_all()
