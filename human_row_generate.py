import csv



def main(csv_reader, csv_writer):
    location = 0
    loc_locations = {}
    github_links = {}
    for row in csv_reader:
        if location != 0:
            func_name = row[0][:row[0].index('(')]
            func_name = func_name[func_name.rfind(' ') + 1:]
            #getting the loc locations for functions and prototypes
            loc_locations = find_location(func_name)
            for locations_array in loc_locations.values():
                github_link = "https://github.com/torvalds/linux/blob/v5.16/" + locations_array[1] + "#L" + locations_array[2][:-2]
                github_links[locations_array[-1]] = github_link
            print(github_links)
            temp_row = row
            temp_row.append([github_links["p"], github_links["f"]])
            csv_writer.writerow(temp_row)
        else:
            header = row
            header.append(["prototype_location_gh", "function_location_gh"])
            csv_writer.writerow(header)
        location += 1
        #if location > 3:
            #break



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



if  __name__ == "__main__":
    with open("trial_human_selected.csv") as read,  open("human_loc_trial.csv", "w") as write:
        csv_read = csv.reader(read, delimiter=',')
        csv_write = csv.writer(write)
        main(csv_read, csv_write)
