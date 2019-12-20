import time
import requests
from geotext import GeoText
import json
import datetime

from os import mkdir, listdir
from os.path import join, dirname, realpath, isdir, isfile
from io import open as iopen

current_dir = dirname(realpath('__file__'))

in_dir_template = join(current_dir, 'parsed/{date}')
in_path_template = join(current_dir, 'parsed/{date}/{n}')


def analyze_file(in_path):
    with iopen(in_path, 'r') as in_file:
        text = in_file.read().replace('-\n', '').replace('\n', '')

    return GeoText(text)


def find_paths():
    paths = []

    downloaded = join(current_dir, 'parsed')
    for d in listdir(downloaded):
        if not isdir(join(downloaded, d)):
            continue

        in_dir = in_dir_template.format(date=d)

        for n in listdir(in_dir):
            path = join(in_dir, n)

            if not isfile(path):
                continue

            in_path = in_path_template.format(date=d, n=n)

            paths.append({
                'date': d,
                'in_path': in_path})

    return paths


def freqs_from_list(ls, freqs={}):
    for c in ls:
        if c in freqs:
            freqs[c] += 1
        else:
            freqs[c] = 1

    return freqs


def analyze_all():
    paths = find_paths()

    print()
    print(f'Found {len(paths)} text files')

    start_time = time.time()
    n_analyzed = 0

    freqs = {}
    cnt_freqs = {}

    for i in paths:
        year, month, day = i['date'].split('-')
        page = int(i['in_path'].split('/')[-1].split('.')[0])+1

        with iopen(join(current_dir, 'out/res.csv'), 'r') as in_file:
            if any(line.startswith(f'{year},{month},{day},{page}')
                   for line in in_file):
                continue

        weekday = datetime.date(int(year), int(month), int(day)).weekday()

        nPages = len(listdir('/'.join(i['in_path'].split('/')[:-1])))
        res = analyze_file(i['in_path'])

        freqs = freqs_from_list(res.cities, freqs)

        cnt_dir = 'AF,AX,AL,DZ,AS,AD,AO,AI,AQ,AG,AR,AM,AW,AU,AT,AZ,BH,BS,BD,BB,BY,BE,BZ,BJ,BM,BT,BO,BQ,BA,BW,BV,BR,IO,BN,BG,BF,BI,KH,CM,CA,CV,KY,CF,TD,CL,CN,CX,CC,CO,KM,CG,CD,CK,CR,CI,HR,CU,CW,CY,CZ,DK,DJ,DM,DO,EC,EG,SV,GQ,ER,EE,ET,FK,FO,FJ,FI,FR,GF,PF,TF,GA,GM,GE,DE,GH,GI,GR,GL,GD,GP,GU,GT,GB,GG,GN,GW,GY,HT,HM,VA,HN,HK,HU,IS,IN,ID,IR,IQ,IE,IM,IL,IT,JM,JP,JE,JO,KZ,KE,KI,KP,KR,KW,KG,LA,LV,LB,LS,LR,LY,LI,LT,LU,MO,MK,MG,MW,MY,MV,ML,MT,MH,MQ,MR,MU,YT,MX,FM,MD,MC,MN,ME,MS,MA,MZ,MM,NA,NR,NP,NL,NC,NZ,NI,NE,NG,NU,NF,MP,NO,OM,PK,PW,PS,PA,PG,PY,PE,PH,PN,PL,PT,PR,QA,RE,RO,RU,RW,BL,SH,KN,LC,MF,PM,VC,WS,SM,ST,SA,SN,RS,SC,SL,SG,SX,SK,SI,SB,SO,ZA,GS,SS,ES,LK,SD,SR,SJ,SZ,SE,CH,SY,TW,TJ,TZ,TH,TL,TG,TK,TO,TT,TN,TR,TM,TC,TV,UG,UA,AE,UK,US,UM,UY,UZ,VU,VE,VN,VG,VI,WF,EH,YE,ZM,ZW'.split(
            ',')

        row = ','.join((str(x) for x in [int(year), int(month), int(day),
                                         int(page), int(nPages),
                                         *[int(weekday == w)
                                           for w in range(7)],
                                         *[res.country_mentions[c]
                                           if c in res.country_mentions
                                           else 0
                                           for c in cnt_dir]]))

        with iopen(join(current_dir, 'out/res.csv'), 'a') as in_file:
            in_file.write('\n'+row)

        # for c, i in res.country_mentions.items():
        #     if c in cnt_freqs:
        #         cnt_freqs[c] += i
        #     else:
        #         cnt_freqs[c] = i

        n_analyzed += 1

    print()
    for x in sorted(cnt_freqs.items(), key=lambda kv: kv[1]):
        print(x)

    t_elapsed = time.time()-start_time

    # print()
    # for x in sorted(freqs.items(), key=lambda kv: kv[1]):
    #     print(x)

    print()
    print(f'Analyzed {n_analyzed} files(s) in {t_elapsed} seconds')
    print('All detected files have been analyzed')
    print()


analyze_all()


def write_data_to_disk(data, out_path):
    try:
        with iopen(out_path, 'w') as out_file:
            out_file.write(data)

    except Exception as e:
        print(f'Exception while writing to disk: {str(e)}')


# main_dir = in_dir_template.format(date='1900-01-14')
# paths = []

# full_res = {}
# cum_res = {
#     'cnt_freqs': {},
#     'name_freqs': {}
# }

# start_time = time.time()
# n_analyzed = 0

# for file_name in listdir(main_dir):

#     file_path = join(main_dir, file_name)

#     if not isfile(file_path):
#         continue

#     res = analyze_file(file_path)

#     name_freqs = {}
#     cnt_freqs = {}

#     cities = [f'{c}, {res.index[1][c.lower()]}' for c in res.cities]

#     name_freqs = freqs_from_list(cities+res.countries, name_freqs)

#     for name, freq in name_freqs.items():
#         if name in cum_res['name_freqs']:
#             cum_res['name_freqs'][name] += freq
#         else:
#             cum_res['name_freqs'][name] = freq

#     for c, i in res.country_mentions.items():
#         if c in cnt_freqs:
#             cnt_freqs[c] += i
#         else:
#             cnt_freqs[c] = i

#         if c in cum_res['cnt_freqs']:
#             cum_res['cnt_freqs'][c] += i
#         else:
#             cum_res['cnt_freqs'][c] = i

#     full_res[int(file_name[:-4])] = {
#         'name_freqs': name_freqs,
#         'cnt_freqs': cnt_freqs,
#     }

#     n_analyzed += 1

# t_elapsed = time.time() - start_time

# print()
# print(f'Analyzed {n_analyzed} text files')
# print(f'Time elapsed: {t_elapsed} second')
# print('Most frequent placenames:')

# for x in sorted(cum_res['name_freqs'].items(), key=lambda kv: kv[1])[::-1][:10]:
#     print(x)

# print()
# print('Most mentioned countries:')

# for x in sorted(cum_res['cnt_freqs'].items(), key=lambda kv: kv[1])[::-1][:10]:
#     print(x)

#     ',')
# df = [['Year', 'Month', 'Day', 'M', 'Tu', 'W',
#        'Th', 'Fr', 'Sat', 'Sun', 'Page']+cnt_dir]

# for page, data in sorted(full_res.items(), key=lambda kv: kv[0]):
#     data = data['cnt_freqs']
#     row = [page]
#     for cnt in ord_cnts:
#         if cnt in data:
#             row.append(data[cnt])
#         else:
#             row.append(0)

#     df.append(row)


# df = [[str(el) for el in row] for row in df]
# out = '\n'.join([','.join(row) for row in df])
# out_path = join(current_dir, '1900-01-14-cnt.csv')
# write_data_to_disk(out, out_path)

# print()

# ord_cnts = sorted(cum_res['cnt_freqs'].keys())

# out = []
# n = 0
# for name, freq in cum_res['name_freqs'].items():

#     req = f'https://api.opencagedata.com/geocode/v1/json?q={name}&key=550e5a2c86c84f508791aa526b3ac18a'

#     response = requests.get(req)
#     json_data = response.json()

#     coords = json_data['results'][0]['geometry']

#     out.append({'name': name, 'coordinates': [
#                coords['lat'], coords['lng']], 'count': freq})

#     n += 1
#     print(f'status: {n}/{len(cum_res["name_freqs"])}')

# json_out = json.dumps(out)

# out_path = join(current_dir, '1900-01-14-geo.json')
# write_data_to_disk(json_out, out_path)


# ord_pls = sorted(cum_res['name_freqs'].keys())

# df = [['Page']+ord_pls]

# for page, data in sorted(full_res.items(), key=lambda kv: kv[0]):
#     data = data['name_freqs']
#     row = [page]
#     for pl in ord_pls:
#         if pl in data:
#             row.append(data[pl])
#         else:
#             row.append(0)

#     df.append(row)

# df = [[str(el) for el in row] for row in df]
# out = '\n'.join([','.join(row) for row in df])
# out_path = join(current_dir, '1900-01-14-pn.csv')
# write_data_to_disk(out, out_path)
