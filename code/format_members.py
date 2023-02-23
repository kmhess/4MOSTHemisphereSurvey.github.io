from argparse import ArgumentParser
from astropy.io import ascii
from astropy.table import Table
from icecream import ic
import numpy as np


def main():
    args = parse_args()
    header, table_header = headers()
    tbl = make_table(args)
    ic(tbl)
    tbl.write(args.output, format='ascii.fixed_width',
              overwrite=True)
    tbl_rst = make_table_rst(tbl)
    content = header + table_header + tbl
    with open(args.output, 'w') as f:
        for line in content:
            print(line.replace('$', ' | '), file=f)
    return


def make_table(args):
    data = ascii.read(args.file, format='csv')
    ic(data)
    ic(sorted(data.colnames))
    cols = ['Name', 'Personal website', 'E-mail', 'Position', 'Affiliation',
            'Scientific interests (few keywords)']
    names = []
    interests = []
    for entry in data:
        name = format_name(entry)
        interest = format_interests(entry)
    #     tbl.append(f'{name} $ {interests} |')
        #tbl.append([name, interests])
        names.append(format_name(entry))
        interests.append(format_interests(entry))
    tbl = Table([names, interests], names=['Name', 'Interests'])
    return tbl


def make_table_ends(tbl):
    col_lengths = get_col_lengths(tbl)
    hdr = '+'.join([i*'-' for i in col_lengths])
    hdr = [f'    +{hdr}+']
    return hdr


def make_table_rst(tbl):
    tbl_ends = make_table_ends(tbl)
    tbl_rst = [str(row) for row in tbl]
    ic(tbl_rst)
    tbl = tbl_ends + tbl + tbl_ends

def format_name(entry):
    # name = f'| {entry["Name"]} [`Web <{entry["Personal website"]}>`_]' \
    #     + f' [E-mail <{entry["E-mail"]}>`_]\n' \
    #     + f'| {entry["Position"]}, {entry["Affiliation(s)"]}\n' \
    #     + f'| {entry["Scientific interests (few keywords)"]}'
    name = f'{entry["Name"]}'
    if entry["Personal website"] != '--':
        name = f'{name} [`<{entry["Personal website"]}>`_]'
    if entry["E-mail"]!= '--':
        name = f'{name} [`<{entry["E-mail"]}>`_]'
    name = f'    $ {name}<n>' \
        + f'    $ {entry["Position"]}, {entry["Affiliation(s)"]}<n>' \
        + f'    $ {entry["Scientific interests (few keywords)"]}'
    if 'Taylor' in entry['Name']:
        print(name)
    return name


def format_interests(entry):
    interests = str(entry['Scientific interests (one paragraph)'])
    return interests.replace('\n', ' ')


def get_col_lengths(tbl):
    n = []
    for line in tbl:
        line = str(line)
        n.append([max([len(i) for i in col.split('\n')])
                  for col in line.split('$')])
    ic(n)
    n = np.max(n, axis=0)
    ic(n)
    return n


def headers():
    header = [
    """.. title: Members
    .. slug: Members
    .. date: 2022-10-07 23:23:08 UTC+11:00
    .. tags:
    .. category:
    .. link:
    .. description:
    .. hidetitle: true
    .. type: text
    """]
    # table_header = \
    #     ['\n.. csv-table:: Members',
    #     '   :header: "Name", "Website", "Email", "Institution"',
    #     '   :width: 100%',
    #     '']
    table_header = \
        ['\n.. table:: Members',
         #'    :widths: 30 70'
         ]
    return header, table_header


def parse_args():
    parser = ArgumentParser()
    add = parser.add_argument
    add('file')
    add('--output', default='../pages/members.rst')
    args = parser.parse_args()
    return args


main()


# the code below formats the file I downloaded from the 4MOST website

# filename = '../files/members.txt'
# header = [
# """.. title: Members
# .. slug: members
# .. date: 2022-10-07 23:23:08 UTC+11:00
# .. tags:
# .. category:
# .. link:
# .. description:
# .. type: text
# """]
# table_header = \
#     ['\n.. csv-table:: Members',
#     '   :header: "Name", "Email", "Institution", "IWG"',
#     '   :width: 100%',
#     '']
# table = []
# with open(filename) as f:
#     for line in f:
#         line = line.strip()
#         # those not in any IWG
#         if len(line) == 3:
#             line = f'{line} --'
#         line = ','.join([f'"{i.strip()}"' for i in line.split('\t')])
#         table.append(f'   {line}')
# file_content = header + table_header + table

# newfile = '../pages/members.rst'
# with open(newfile, 'w') as f:
#     for line in file_content:
#         print(line, file=f)
