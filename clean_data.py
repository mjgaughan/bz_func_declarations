import csv




def exclude_void(csv_reader, csv_writer):
    voids = 0
    total = 0
    for row in csv_reader:
        total += 1
        args = row[0][row[0].find('(') + 1: row[0].find(')') ]
        #print(args)
        if args != "void" and args != "" and " " in args:
            csv_write.writerow(row)
        else:
            voids += 1
    print("-------")
    print("total void/no args: " + str(voids))
    print("total: " + str(total))
    print("% void/no args: "+ str(voids/total))
    print("------")

def multiply_for_par(csv_reader, csv_writer):
    total_lines = 0
    pointers = 0
    for row in csv_reader:
        args = row[0][row[0].find('(') + 1: row[0].find(')') ]
        if ',' in args:
            args_list = args.split(',')
        else:
            args_list = [args]
        arg_list_len = len(args_list)
        skip = False
        if arg_list_len > 10:
            skip = True
        for arg in args_list:
            if " " not in arg:
                skip = True
        if skip:
            continue
        for arg_index in range(arg_list_len):
            row_array = [row[0], row[1], row [2], row[3]]
            for param_index in range(10):
                if param_index == arg_index:
                    if "*" in args_list[arg_index]:
                        pointers += 1
                    row_array.append(args_list[arg_index])
                elif param_index < arg_list_len:
                    row_array.append('ignore')
                else: 
                    row_array.append('u')
            total_lines += 1
            #print(row_array)
            csv_writer.writerow(row_array)
    print("--------")
    print("# of pointers in params: " + str(pointers))
    print("total params: " + str(total_lines))
    print("% * in total: " +  str(pointers/total_lines))
    print("---------")
        

if __name__ == "__main__":
    temp_name = "temp-full-0.csv"
    with open("init-corp-05.csv") as read, open(temp_name, "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        csv_write.writerow(['func_prototype', 'line', 'file', 'in_macro']) 
        exclude_void(csv_read, csv_write)
    with open(temp_name) as read, open ("final_full_total.csv", "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        csv_write.writerow(['func_prototype', 'est_line', 'file', 'in_macro', 'a0','a1','a2','a3','a4','a5', 'a6', 'a7', 'a8', 'a9'])
        multiply_for_par(csv_read,csv_write)
