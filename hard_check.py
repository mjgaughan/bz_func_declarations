import csv 



def main(csv_reader, csv_writer):
    location = 0
    for row in csv_reader:
        if location != 0:
            print(row)
            func_name = row[0][:row[0].index('(')]
            func_name = func_name[func_name.rfind(' ') + 1:]
            print(func_name)
            #TODO look for opening gzip and finding file locations from there
        location += 1
        if location > 10:
            break




if  __name__ == "__main__":
    print("bozo")
    with open("final_full.csv") as read, open("bozo.csv", "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        main(csv_read, csv_write)
