import csv 
import gzip


def main(csv_reader, csv_writer):
    location = 0
    for row in csv_reader:
        if location != 0:
            func_name = row[0][:row[0].index('(')]
            func_name = func_name[func_name.rfind(' ') + 1:]
            #TODO look for opening gzip and finding file locations from there
            loc_locations = find_location(func_name)
            if len(loc_locations) < 2:
                print('invalid function/prototype')
                continue
            else:
                print(row)
                print(loc_locations)
        location += 1
        if location > 10:
            break

def find_location(func_name):
    locations = {}
    with open("tags_f_p.csv") as tags:
        tags_reader = csv.reader(tags, delimiter = ',')
        for row in tags_reader:
            #print(row)
            if row[0] == func_name:
                if row[3] == 'f':
                    print(row)
                    locations['function'] = row
                else:
                    print(row)
                    locations['prototype'] = row
    return locations


def gz_to_csv(gzip_file, csv_writer):
    with gzip.open(gzip_file,mode = 'rt', newline='\n') as tags:
        file_content = tags.read()
        file_array = file_content.split('\n')
        for line in file_array:
            array_line = line.split('\t')
            if len(array_line) > 3 and (array_line[3] == 'f' or array_line[3] == 'p'):
                csv_writer.writerow(array_line)


def check_csv(filename):
    with open(filename) as csvs:
        reader = csv.reader(csvs, delimiter = ',')
        for row in reader:
            print(row)

if  __name__ == "__main__":
    print("bozo")
    with open("final_full.csv") as read, open("temp.csv", "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        #gz_to_csv("tags.gz", csv_write)
        main(csv_read, csv_write)
        #check_csv("tags_f_p.csv") 
