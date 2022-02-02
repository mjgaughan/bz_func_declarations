import csv
import re
import gzip
import subprocess
import os
import time
from parse_commands import find_func


def main(csv_reader, csv_writer):
    location = 0
    t1 = time.time()
    valid_ones = []
    #getting into the directory
    os.chdir('../linux/')
    #os.chdir('../test_target/')
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
                # editing files in prot and func
                for locations_array in loc_locations.values():
                    try:
                        edit_file(locations_array, row)
                    except IndexError:
                        print("index error at:" + locations_array[1])
                    if locations_array[1][-1] == "c":
                        #print("found CCCCCCCCCC")
                        func_path = locations_array[1]
                #quick compile
                gcc_ = find_func("../bz_func_declarations/commands.sh",func_path)
                if gcc_ is not None:
                    print("WE GOT ONE, WE FOUND THE COMPILE!!!! ___________________________________________________")
                    immutable = compile_files(gcc_)
                    row.append(immutable)
                    print(row)
                    valid_ones.append(row)
                    csv_writer.writerow(row)
                # revert to original
                subprocess.run(["git", "reset", "--hard"])
                if gcc_ is not None:
                    #quick compile back as regular
                    compile_files(gcc_)
        location += 1
        if location > 400:
            break
    #return home
    print(valid_ones)
    t2 = time.time()
    print(t1-t2)
    #subprocess.run(["cd", "../bz_func_declarations/"])
    os.chdir('../bz_func_declarations/')

def compile_files(gcc_command):
    print("buonosera")
    print("-----------------------") 
    compile_result = subprocess.run([gcc_command])
    if compile_result.returncode != 0:
        print("it didn't work")
        return False
    else:
        return True
    


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
        current_line = string_list[file_line -index]
        #is the func_name in the current line
        if location_array[0] in current_line:
            if target_param not in current_line:
                new_index = -1
                while target_param not in current_line:
                    new_index += 1
                    current_line = string_list[file_line - index + new_index]
                    print(current_line)
            print("This is it, this is the target param!")
            print(current_line)
            edit_line = string_list.index(current_line)
            new_line = current_line
            new_param = target_param
            if "const" not in target_param:
                new_param = "const " + new_param
                #new_line = current_line[:current_line.index(target_param)] + "const " + current_line[current_line.index(target_param):]
            if "*" in target_param:
                for letter_index in range(len(new_param)):
                    if new_param[letter_index] == "*":
                        new_param = new_param[:letter_index + 1] + " const " + new_param[letter_index + 1:]
            new_line = new_line[:new_line.index(target_param)] + new_param + new_line[new_line.index(target_param) + len(target_param):]
            print(new_line)
            string_list[edit_line] = new_line 
            break
    opened_file.close()
    #write to file
    print("this is the file location")
    print(file_location)
    print(os.getcwd())
    augmented_location = file_location[9:]
    print(augmented_location)
    new_file = open(augmented_location, "w")
    new_file_edits = "".join(string_list)
    new_file.write(new_file_edits)
    new_file.close()

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
