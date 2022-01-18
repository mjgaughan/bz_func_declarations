import os 
import glob

def py_to_h(txt_filename):
    nl_file =txt_filename[:txt_filename.find('.')]
    print(nl_file)
    h_filename = str(nl_file + '.h')
    os.rename(txt_filename, h_filename)
    return h_filename



def recurse_down(root_dir):
    print(root_dir)
    print(os.getcwd())
    for filename in glob.glob(root_dir + '**/*.txt', recursive=True):
        print(filename)
        new_filename = py_to_h(filename)
        print(new_filename)




if __name__ == '__main__':
    recurse_down('linux-test/')
