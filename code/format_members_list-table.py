from argparse import ArgumentParser
from astropy.io import ascii
from astropy.table import Table
from icecream import ic
import numpy as np


def main():
    args = parse_args()
    list_table_rows = []
    names = []
    with open(args.file, 'r') as f:
        f.readline()
        for line in f:
            ic(line)
            try:
                line = [i.replace('"', '')
                        for i in line.replace('\n', '').split('","')]
                names.append(line[1].split()[-1])
                if line[3]:
                    member = [f'`{line[1]} <{line[3]}>`_']
                else:
                    member = [f'{line[1]}']
                # if line[3]:
                #     member.append(
                #         f'`E-mail <{line[3]}>`__')
                member.append(f'{line[4]}, {line[5]}')
                if line[2]:
                    member.append(f'`Personal website <{line[2]}>`__')
                interests = line[6:8]
            except IndexError as err:
                print('****')
                print()
                print(line)
                raise IndexError(err)
            print(member)
            print(interests)
            print()
            list_table_rows.append([member, interests])
    print(names)
    jsort = np.argsort(names)
    # write
    separator = '\n        |\n        | __________________________________\n        |'
    separator = ''
    hdr = ['.. title: 4HS members',
           '.. slug: members',
           '.. date: 2022-10-08 00:2,0:29 UTC+11:00',
           '.. tags:',
           '.. category:',
           '.. link:',
           '.. description:',
           '.. type: text',
           '.. has_math: true',
           '.. hidetitle: true',]
    with open(args.output, 'w') as f:
        print('\n'.join(hdr), file=f)
        print('\n.. list-table::\n    :header-rows: 1\n', file=f)
        print(f'    * - | Member{separator}\n      - | Interests', file=f)
        print(separator, file=f)
        for j in jsort:
            row = list_table_rows[j]
            col = [i.strip() for i in row[0]]
            member = f'    * - | {col[0]}\n        | {col[1]}'
            if len(col) == 3:
                member = f'{member}\n        | {col[2]}'
            col = [i.strip() for i in row[1]]
            interests = f'      - | **{col[0].capitalize()}**\n        | {col[1]}'
            print(member, file=f)
            #print(separator, file=f)
            print(interests, file=f)
            print(separator, file=f)
    return


def parse_args():
    parser = ArgumentParser()
    add = parser.add_argument
    add('file')
    add('--output', default='../pages/members.rst')
    args = parser.parse_args()
    return args


main()
