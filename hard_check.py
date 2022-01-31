import csv 
import re
import gzip


def main(csv_reader, csv_writer):
    location = 0
    for row in csv_reader:
        print(row)
        if location != 0:
            func_name = row[0][:row[0].index('(')]
            func_name = func_name[func_name.rfind(' ') + 1:]
            #getting the loc locations for functions and prototypes
            loc_locations = find_location(func_name)
            if len(loc_locations) < 2:
                print('invalid function/prototype')
                continue
            else:
                print(row)
                print(loc_locations)
                #TODO: editing files in prot and func
                for locations_array in loc_locations.values():
                    edit_file(locations_array, row)
                #TODO: quick compile
                #TODO: record and save output of quick compile
                #TODO: revert to original
                #TODO: quick compile back as regular
        location += 1
        if location > 5:
            break


def edit_file(location_array, original_row):
    file_location = "../linux/" + location_array[1]
    opened_file = open(file_location)
    string_list = opened_file.readlines()
    #getting file line from sometimes messy location
    file_line = int(re.sub(r'\W+', '', location_array[2]))
    #iterating backwards through the file starting at the stated location of the file
    #finding the target parameter that is needed
    target_param = ""
    for first_index in range(4,14):
        current_entry = original_row[first_index]
        if current_entry != 'u' and current_entry != "ignore":
            target_param = current_entry.strip()
    #making sure the line we are grabbing has the target param the way we need
    for index in range(len(string_list)):
        #this is the current line being examined in the file
        current_line = string_list[file_line-index]
        #is the func_name in the current line
        if location_array[0] in current_line:
            '''
            #make it the func head
            func_head = current_line
            #if the def not done
            if ')' not in current_line:
                #trying to find end of the func def
                for i in range(1,30):
                    nested_line = string_list[file_line - index + i]
                    func_head += nested_line
                    if ')' in nested_line:
                        break
            if target_param in func_head:
                print("this is from the location of target param")
                print(func_head)
            '''
            if target_param not in current_line:
                new_index = -1
                while target_param not in current_line:
                    new_index += 1
                    current_line = string_list[file_line - index + new_index]
                    print(current_line)
            print("This is it, this is the target param!")
            print(current_line)
            new_line = current_line
            if "const" not in target_param:
                new_line = current_line[:current_line.index(target_param)] + "const " + current_line[current_line.index(target_param):]
            if "*" in target_param:
                star_location = []
                for letter_index in range(len(target_param)):
                    if target_param[letter_index] == "*":
                        star_location.append(letter_index)
                for entry in star_location:
                    new_line = new_line[:new_line.index(target_param) + entry + 1] + " const " + new_line[new_line.index(target_param) + entry + 1:]
            print(new_line)
            break
    opened_file.close()

def find_location(func_name):
    locations = {}
    with open("tags_f_p.csv") as tags:
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


def gz_to_csv(gzip_file, csv_writer):
    with gzip.open(gzip_file,mode = 'rt', newline='\n') as tags:
        file_content = tags.read()
        file_array = file_content.split('\n')
        for line in file_array:
            array_line = line.split('\t')
            #discrim against non functions or prototypes
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
        #edit_file(['gpiotools_get_values', 'tools/gpio/gpio-utils.h', '33;"', 'p'], ['\nint gpiotools_get_values(const int fd, struct gpio_v2_line_values *values);', '32', '../linux/tools/gpio/gpio-utils.h', 'False', 'ignore', ' struct gpio_v2_line_values *values', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u']) 
