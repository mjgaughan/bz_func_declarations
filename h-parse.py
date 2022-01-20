from ast import arg
from curses.ascii import isalnum
import os
from string import punctuation 
#import sys
import glob
from typing import List, Optional, Tuple
import csv
#import re 
#import attr
C_PROHIB = ["return ", "=", "\n*", "*/", "while ", ">", "if ", "define ", "extern "]
PUNCTUATION = [",", ";"]
PROHIB_START = set(op[0] for op in C_PROHIB)


#decayed and unnecessary function to flip the h files to txt files
#can just read in the h files AS txt files
def h_to_txt(h_filename):
    nl_file = h_filename[:h_filename.find('.')]
    print(nl_file)
    txt_filename = str(nl_file + '.txt')
    os.rename(h_filename, txt_filename)
    return txt_filename


#simple method to find every *.h file in the directory
def recurse_down(root_dir):
    print(root_dir)
    print(os.getcwd())
    with open('init-corp-00.csv', 'w') as csvfile:
        files_examined = 0
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(['func_prototype', 'line', 'file', 'in_macro']) 
        for filename in glob.glob(root_dir + '**/*.h', recursive=True):
            files_examined += 1
            print("starting parse on " + filename)
            parse_txt(filename, csvwriter)
            print("done with " + filename)
            print("files: " + str(files_examined))
    
#parsing the h file as txt
def parse_txt(txtfile, writer):
    with open(txtfile) as f:
        chars = f.read()
        block = ""
        line_loc = 0
        for char in chars:
            #print(char)
            if char == "\n":
                line_loc += 1
            #if # is the character, can skip
            if "#" in char:
                continue
            #block is just the accumulation of characters in the txt file
            block += char
            
            #this has to be all of the logic for parsing 
            if char == '}' or char == ";" or list(block)[-2:] == ['\n', '\n']:
                if "{" in block:
                    block = block[:block.find('{')]
                valid = True
                if "*/" in block:
                        block = block[block.find('*/') + 2:]
                for entry in C_PROHIB:
                    if entry in block:
                        valid = False
                #checks form of lines to see if they match function prototypes as defined in literature
                if ('(' in block and ')' in block):
                    valid = check_form(block, valid)
                    #print("----")
                    #print(block)
                    #print(valid)
                    #isolating arguments between first open paren and last close paren
                    arguments = block[block.find('(') + 1 :block.rfind(')') - 1]
                    temp_arg = ""
                    open_paren = 1
                    arg_arr = []
                    #for each character in the argument, append to temporary save
                    for char in arguments:
                        if char == "(":
                            open_paren += 1
                        if char == ")":
                            open_paren -= 1
                        if (open_paren == 1 and char == ",") or open_paren == 0:
                            arg_arr.append(temp_arg)
                            temp_arg = ""
                        temp_arg += char
                    #print(arg_arr)
                    #this below block is for identifying function prototypes that might be in other prototypes
                    for arg in arg_arr:
                        cleaned_arg = clean_arg_string(arg)
                        if "(" in cleaned_arg and check_form(cleaned_arg, True):
                            if cleaned_arg[1] == "(":
                                cleaned_arg = cleaned_arg[2:]
                            #print("---------")
                            #print(cleaned_arg + " is located at line " + str(line_loc) + " in file " + str(txtfile))
                            writer.writerow([cleaned_arg, line_loc, str(txtfile), "True"])
                            #print("---------")
                    #this block above does the function prototype within thing
                    if valid:
                        #print("---------")
                        func_prototype = block
                        #print(func_prototype + " is located at line " + str(line_loc) + " in file " + str(txtfile))
                        writer.writerow([func_prototype, line_loc, str(txtfile), "False"])
                        #print("---------")
                block = ""
            #previous_char = char
            
def check_form(block, valid):
    #if it comes in being not valid
    if not valid:
        return False
    begin_args = block.find('(')
    #if there are no open paren in the entire block
    if begin_args == -1:
        return False
    prev_char = '('
    #this should discrim against MACROS
    seen_space = False
    for index in range(len(block)):
        #iterating backwards, beginning at the theoretical argument intake
        current_char = block[begin_args - index]
        #if there is a space and the preceding char is alphanumeric than it should satisfy
        if current_char == " ":
            if prev_char == "(":
                return False
            seen_space = True
        #this should discrim against MACROS which have similar structure to function prototype but lack 
        if begin_args - index == 0 and not seen_space:
            return False
        if prev_char == " " and current_char.isalnum() and current_char not in PUNCTUATION:
            return True
        #if there are any commas or semicolons preceding the parentheses then it is not an argument intake
        if current_char in PUNCTUATION:
            return False
        prev_char = current_char
    return False

def clean_arg_string(arg):
    new_arg = " ".join(arg.split())
    return new_arg

if __name__ == '__main__':
    recurse_down('../linux/')
