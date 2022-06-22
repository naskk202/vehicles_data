import re
from operator import itemgetter

import requests
import xlsxwriter


def data_parser(*args, **kwargs):
    url = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'
    request_data = requests.get(url)
    data = request_data.json()

    # Filter elements which include 'hu'
    resources_with_hu = [el for el in data if el['hu']]
    sorted_resources_with_hu = sorted(resources_with_hu, key=itemgetter('gruppe'))

    input_fields = re.findall('[A-za-z\d]+', *args)
    fields = ['rnr']
    fields.extend(input_fields)

    # Create a list containing input fields from data
    fields_for_excel = []
    for el in sorted_resources_with_hu:
        fields_for_excel.append({})
        for par in el:
            if par in fields:
                fields_for_excel[len(fields_for_excel) - 1][par] = el[par]

    work_book = xlsxwriter.Workbook('vehicles_$current_date_iso_formatted.xlsx')
    work_table = work_book.add_worksheet()

    work_table.write_row(0, 0, fields_for_excel[0].keys())
    row_num = 1
    for el in fields_for_excel:
        work_table.write_row(row_num, 0, el.values())
        row_num += 1

    work_book.close()


data_parser(input())
