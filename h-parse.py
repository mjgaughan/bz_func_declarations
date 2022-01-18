import os 
import sys
import glob


def h_to_py(h_filename):
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
        new_filename = h_to_py(filename)
        print(new_filename)
        parse_txt(new_filename)


def parse_txt(txtfile):
    with open(txtfile) as f:
        lines = f.readlines()
        block = ""
        for line in lines:
            line = line.strip()
            block += " " + line
            if '}' in block and '{' in block and '(' in block and ')' in block:
                print("---------")
                print(block[:block.find('{')])
                print("---------")
                block = ""

if __name__ == '__main__':
    recurse_down('linux/')
    
