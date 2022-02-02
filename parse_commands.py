







def find_func(filename, target_file):
    with open(filename) as commands:
        lines = commands.readlines()
        for line in lines:
            #print("-----")
            #print(line)
            if target_file in line:
                temp = ""
                index = 0
                valid = False
                for char in line:
                    temp += char
                    if char == ";":
                        index += 1
                        if index == 2 and  "CC" in temp:
                            valid = True
                        if index == 3 and valid and "gcc" in temp:
                            return temp[:temp.index(";")]
                        temp = ""


if __name__ == "__main__":
    print("hi")
    print(find_func("commands.sh", "tools/thermal/tmon/tui.c"))
