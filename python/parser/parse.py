from PIL import Image
import pytesseract
import time

from os import mkdir, listdir
from os.path import join, dirname, realpath, isdir, isfile
from io import open as iopen

current_dir = dirname(realpath('__file__'))

in_path_template = join(current_dir, 'downloaded/{date}/jpg/{n}')
in_dir_template = join(current_dir, 'downloaded/{date}/jpg')

out_path_template = join(current_dir, 'parsed/{date}/{n}.txt')
out_dir_template = join(current_dir, 'parsed/{date}')


def parse_file(in_path):
    text = pytesseract.image_to_string(Image.open(
        in_path))

    return text


def write_text_to_disk(text, out_path):
    try:
        with iopen(out_path, 'w') as out_file:
            out_file.write(text)

    except Exception as e:
        print(f'Exception while writing to disk: {str(e)}')


def find_unparsed_images():
    images = []

    downloaded = join(current_dir, 'downloaded')
    for d in listdir(downloaded):
        if not isdir(join(downloaded, d)):
            continue
        if not isdir(join(downloaded, d, 'jpg')):
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


def parse_all():
    images = find_unparsed_images()

    start_time = time.time()
    n_parsed = 0

    print()
    print(f'Found {len(images)} unparsed images')
    print()
    print('parsing...')
    print()

    while len(images) > 0:

        i = images[0]

        out_dir = out_dir_template.format(date=i['date'])

        if not isdir(out_dir):
            mkdir(out_dir)

        text = parse_file(i['in_path'])
        write_text_to_disk(text, i['out_path'])

        n_parsed += 1
        t_elapsed = time.time()-start_time

        t_avg = t_elapsed/n_parsed

        print(f'Parsed {n_parsed} image(s) in {readable_seconds(t_elapsed)}')
        print(f'Avg {int(t_avg)} seconds/image')

        images = find_unparsed_images()
        print(
            f'Estimated {readable_seconds(t_avg*(len(images)))} ' +
            f'({len(images)} images) remaining')
        print()

    print('All detected files have been parsed')


parse_all()
