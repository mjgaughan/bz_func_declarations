from curses.ascii import isalnum
import os
from string import punctuation 
import sys
import glob
from typing import List, Optional, Tuple
import re 
#import attr
C_PROHIB = ["return ", "=", "/*", "*/", "while ", ">", "if ", "define ", "extern "]
PUNCTUATION = [",", ";"]
PROHIB_START = set(op[0] for op in C_PROHIB)

def h_to_txt(h_filename):
    nl_file = h_filename[:h_filename.find('.')]
    print(nl_file)
    txt_filename = str(nl_file + '.txt')
    os.rename(h_filename, txt_filename)
    return txt_filename



def recurse_down(root_dir):
    print(root_dir)
    print(os.getcwd())
    for filename in glob.glob(root_dir + '**/*.h', recursive=True):
        print(filename)
        
        #new_filename = h_to_txt(filename)
        #print(new_filename)
        parse_txt(filename)
        
        '''
        with open(filename) as f:
            rdr = CharReader(f.read())
        tokens = rdr.read_all()
        print(len(tokens))
        print(tokens)
        '''

def parse_txt(txtfile):
    with open(txtfile) as f:
        chars = f.read()
        block = ""
        #previous_char = ""
        #print(chars)
        for char in chars:
            #print(len(char))
            if "#" in char:
                continue
            #print(char)
            #arr_char = char.split()
            #for word in arr_char:
            block += char
            
            #https://stackoverflow.com/questions/476173/regex-to-pull-out-c-function-prototype-declarations
            
            
            #this has to be all of the logic for parsing 
            if char == '}' or char == ";":
                #if re.match(r"^(\w+( )?){2,}\([^!@#$+%^]+?\)\{[^!@#$+%^]+?\}",block):
                    #print(block)
                if "{" in block:
                    block = block[:block.find('{')]
                valid = True
                for entry in C_PROHIB:
                    if entry in block:
                        valid = False
                valid = check_form(block, valid)
                if '(' in block and ')' in block and valid:
                    print("---------")
                    func_prototype = block
                    print(func_prototype)
                    print("---------")
                block = ""
            #previous_char = char
            
def check_form(block, valid):
    if not valid:
        return False
    begin_args = block.find('(')
    #print(begin_args)
    if begin_args == -1:
        return False
    prev_char = '('
    for index in range(len(block)):
        #iterating backwards, beginning at the theoretical argument intake
        current_char = block[begin_args - index]
        #if there is a space and the preceding char is alphanumeric than it should satisfy
        
        if prev_char == " " and current_char.isalnum() and current_char not in PUNCTUATION:
            return True
        #if there are any commas or semicolons preceding the parentheses then it is not an argument intake
        if current_char in PUNCTUATION:
            return False
        prev_char = current_char
        #iterating forwards 
        block[index]
    return False
        

if __name__ == '__main__':
    recurse_down('linux-test/')