filename = '../files/members.txt'
header = [
""".. title: Members
.. slug: members
.. date: 2022-10-07 23:23:08 UTC+11:00
.. tags:
.. category:
.. link:
.. description:
.. type: text
"""]
table_header = \
    ['\n.. csv-table:: Members',
    '   :header: "Name", "Email", "Institution", "IWG"',
    '   :width: 100%',
    '']
table = []
with open(filename) as f:
    for line in f:
        line = line.strip()
        # those not in any IWG
        if len(line) == 3:
            line = f'{line} --'
        line = ','.join([f'"{i.strip()}"' for i in line.split('\t')])
        table.append(f'   {line}')
file_content = header + table_header + table

newfile = '../pages/members.rst'
with open(newfile, 'w') as f:
    for line in file_content:
        print(line, file=f)
