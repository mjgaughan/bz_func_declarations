import csv
import re
import gzip
import subprocess
import os
import datetime
from parse_commands import find_func
from tqdm import tqdm
import pandas as pd


'''
This method exists to consolidate all of the other smaller tasks for this hard_check file
taking in two csv files, an in and an out, the main method grabs the function def, finds the compile command, and runs the command before resetting the repo
'''
def main(csv_reader, csv_writer):
    location = 0
    immutable_count = 0
    time_start = datetime.datetime.now()
    valid_ones = []
    #getting into the directory
    os.chdir('../linux/')
    #for every function param in every function def in the Linux repo
    for row in csv_reader:
        print(location)
        row_time_start = datetime.datetime.now()
        #for row in csv_reader.iterrows(): 
        #row = csv_reader[i]
        print(row)
        if location != 0:
            func_name = row[0][:row[0].index('(')]
            func_name = func_name[func_name.rfind(' ') + 1:]
            #getting the file locations for functions and prototypes
            loc_locations = find_location(func_name)
            #if its missing the location of either the function or the prototype
            if len(loc_locations) < 2:
                print('invalid function/prototype')
                continue
            else:
                print(row)
                print(loc_locations)
                #initializing dummy path
                func_path = "THIS SUBSTRING IS NEVER FOUND IN ANY FILES"
                # editing files in prot and func
                for locations_array in loc_locations.values():
                    #if there is a valid file location for either the func prototype or def
                    try:
                        edit_file(locations_array, row)
                    #if there isn't
                    except IndexError:
                        print("index error at:" + locations_array[1])
                    if locations_array[1][-1] == "c":
                        func_path = locations_array[1]
                #quick compile, find the compile command from the commands.sh file
                gcc_ = find_func("../bz_func_declarations/commands.sh",func_path)
                #if you can find it
                if gcc_ is not None:
                    print("WE GOT ONE, WE FOUND THE COMPILE!!!! ___________________________________________________")
                    print(gcc_)
                    print(func_path)
                    opened_file = open(func_path)
                    string_list = opened_file.readlines()
                    opened_file.close()
                    #compile with the relevant gcc command
                    immutable = compile_files(gcc_)
                    #append the results of this compile
                    row.append(immutable)
                    print(row)
                    if immutable:
                        immutable_count += 1
                    #valid ones is the array of all files with valid gcc commands
                    valid_ones.append(row)
                    row_time_elapsed = datetime.datetime.now() - row_time_start
                    row.append(row_time_elapsed)
                    csv_writer.writerow(row)
                # revert to original, without 'const' inserted
                subprocess.run(["git", "reset", "--hard"])
                if gcc_ is not None:
                    #quick compile back as regular just to check that everything is as left
                    compile_files(gcc_)
        location += 1
    time_elapsed = datetime.datetime.now() - time_start
    print(time_elapsed)
    print("compile %")
    print(len(valid_ones)/location)
    print("immutable % from compiles")
    print(immutable_count/len(valid_ones))
    #subprocess.run(["cd", "../bz_func_declarations/"])
    os.chdir('../bz_func_declarations/')

'''
this method exists solely to, with a given gcc command, compile the edited files
'''
def compile_files(gcc_command):
    print(os.getcwd())
    print("-----------------------")
    #some cleaning is necessary from the commands.sh file
    initial_commands = gcc_command.split(" ")[2:]
    cleaned_gcc = []
    for entry in initial_commands:
        if entry != " " and entry != '':
            cleaned_gcc.append(entry)
    #this is where the compile takes place
    compile_result = subprocess.run(cleaned_gcc)
    #based on the return code from the subprocess, can tell whether or not the compile worked
    print(compile_result)
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
            #switch the bottom two
            new_line = new_line[:new_line.index(target_param)] + new_param + new_line[new_line.index(target_param) + len(target_param):]
            #new_line = "hjksdfjashjlhjfhjadklnsanjkdnkjlfdjknfkjnjknfsnjkfs"
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

'''
this is just a simple method to get data which was in a gzip file into a csv file
most of the project relies on navigating csv files so it was important to have everything in a uniform file type
'''
def gz_to_csv(gzip_file, csv_writer):
    with gzip.open(gzip_file,mode = 'rt', newline='\n') as tags:
        file_content = tags.read()
        file_array = file_content.split('\n')
        for line in file_array:
            array_line = line.split('\t')
            #discrim against non functions or prototypes
            if len(array_line) > 3 and (array_line[3] == 'f' or array_line[3] == 'p'):
                csv_writer.writerow(array_line)

'''
this function was just to check that the contents of the csv were what were assumed
operating through a ssh terminal, there was not really any other way to check the contents of a given csv
'''
def check_csv(filename):
    with open(filename) as csvs:
        reader = csv.reader(csvs, delimiter = ',')
        for row in reader:
            print(row)
'''
this is for me to invoke the hard check from running the file
'''
if  __name__ == "__main__":
    with open("final_full_shufffled.csv") as read,  open("full_shuffle_labeled.csv", "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        #writing the file header for the output
        csv_write.writerow(["func_prototype", "est_line", "file", "in_macro", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "immutable", "label_time"])
        main(csv_read, csv_write)
