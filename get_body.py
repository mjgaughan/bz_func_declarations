import csv
import os
from h_parse import check_form

def find_location(func_name):
    locations = {}
    with open("../bz_func_declarations/tags_f_p.csv") as tags:
        tags_reader = csv.reader(tags, delimiter = ',')
        for row in tags_reader:
            #print(row)
            if row[0] == func_name:
                if row[3] == 'f':
                    #print(row)
                    locations['function'] = row
                else:
                    #print(row)
                    locations['prototype'] = row
    return locations



def main(csv_read, csv_writer):
    location = 0
    for row in csv_read:
        if location != 0:
            func_name = row[0][:row[0].index('(')]
            func_name = func_name[func_name.rfind(' ') + 1:]
            #getting the loc locations for functions and prototypes
            loc_locations = find_location(func_name)
            temp_row = row
            #csv_writer.writerow(temp_row)
            #print(loc_locations["function"])
            func_body = get_body(loc_locations["function"][1], loc_locations["function"][2], loc_locations["function"][0])
            print(loc_locations["function"][0])
            print(func_body)
            csv_writer.writerow(temp_row)
        else:
            header = row
            header.append("func_body_text")
            csv_writer.writerow(header)
        location += 1
        if location > 7:
            break


def get_body(file_loc, line, func_name):
    print(file_loc)
    with open("../linux/" + file_loc) as f:
        chars = f.readlines()
        in_body = False
        temp_body = ""
        net_open = 0
        multi_line_def = True
        for line in chars:
            if not in_body: 
                if func_name in line and check_form(line, True):
                    if "{" in line:
                        net_open = 1
                        multi_line_def = False
                    in_body = True
            else:
                #print(line)
                #print(net_open)
                if "{" in line:
                    net_open += 1
                    if multi_line_def:
                        multi_line_def = False
                        net_open = 1
                temp_body += line
                if "}" in line:
                    net_open -= 1
                    if net_open == 0:
                        #print(temp_body)
                        in_body = False
                        return temp_body


if  __name__ == "__main__":
    with open("full_shuffle_labeled.csv") as read,  open("test_test_test.csv", "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        main(csv_read, csv_write)

