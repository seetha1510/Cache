# // File: cachesimulator.py
# // Author(s): Taowei Ji and Seetha Senthilnathan
# // Date: 04/25/2020
# // Section: 509
# // E-mail: davidtaoweiji@tamu.edu seetha1510@tamu.edu
# // Description:
# // e.g. The content of this file implements the cache simulator

from math import*
from random import randint
ram = {}
cache = {}

# cache: key : matrix (valid, dirty, tag, content, fre)
# content is a list[] without 0x
# set is in decimal, tag is in hex without the 0x,
# value has to be matrix


def filereader(filname):
    global icontent
    icontent = []
    readfile = open(filename+".txt")
    for line in readfile:
        line = line.rstrip("\n")
        icontent.append(line)
    readfile.close()


# read file to get fill ram
filename = "input"
filereader(filename)
for i in range(0, 256):
    key = hex(i)
    ram[key] = icontent[i]

while True:
    try:
        # get details to structure cache
        print("*** Welcome to the cache simulator ***\ninitialize the RAM:\ninit-ram 0x00 0xFF\n"
              "ram successfully initialized!")
        print("configure the cache:")
        C = int(input("cache size: "))
        B = int(input("data block size: "))
        E = int(input("associativity: "))
        replace = int(input("replacement policy: "))
        write_hit_pol = int(input("write hit policy: "))
        write_miss_pol = int(input("write miss policy: "))
        print("cache successfully configured!")
        break
    except ValueError:
        # error catching in input for inputs that are not int
        print("Invalid input")
        continue


# cache read function
def cache_read(address):
    global time_cycle
    global num_miss
    global num_hit
    time_cycle +=1
    res = bin(int(address,16))
    res = res[2::]
    res = res.zfill(8)
    block_num = res[(8-block_width)::]
    block_ans = int(block_num, 2)

    set_num = res[(8 - block_width-set_width):(8 - block_width)]
    set_num = "0b" + set_num
    set_ans = int(set_num, 2)
    # set_print = hex(set_ans).upper()
    # set_print = set_print[2::]
    # set_print = set_print.zfill(2)
    print("set:" + str(set_ans))
    tag_num = res[0:8-block_width-set_width]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2)).upper()
    tag_ans = tag_ans[2::]
    tag_print = tag_ans.zfill(2)
    print("tag:"+tag_print)
    hit = "no"
    data = ""
    for i in cache[set_ans]:
        if len(tag_ans) ==1:
            tag_ans = "0"+tag_ans
        if i[0]== 1 and i[2]==tag_ans:
            hit = "yes"
            num_hit+=1
            data = i[3][block_ans]
            data = "0x" + data
            break

    print("hit:"+ str(hit))
    # cache miss
    if hit == "no":
        num_miss += 1
        # if replacement policy is random replacement
        address = "0x" + address
        if replace == 1:
            set_val = set_ans
            line_num = randint(0, E-1)
            print("eviction_line:"+str(line_num))
            print("ram_address:"+address)
            temp = (int(address,16) // B)*B
            ram_tag = cache[set_val][line_num][2]
            ram_tag = bin(int(ram_tag, 16))
            update_set = bin(set_val)
            update_set = update_set[2::]
            update_set = update_set.zfill(set_width)
            update_block = ""
            update_block = update_block.zfill(block_width)
            update_address = ram_tag + update_set + update_block
            update_ram = (int(update_address, 2))
            if cache[set_val][line_num][1] == 1:
                for i in range(0, B):
                    ram[hex(update_ram)] = cache[set_val][line_num][3][i]
                    update_ram += 1
            cache[set_val][line_num][0] = 1
            cache[set_val][line_num][1] = 0
            cache[set_val][line_num][3] = []
            cache[set_val][line_num][2]= tag_ans
            for i in range(0,B):
                cache[set_val][line_num][3].append(ram[hex(temp)])
                temp +=1
            cache[set_val][line_num][4]=time_cycle
            data = cache[set_val][line_num][3][block_ans]
            data = "0x" + data
            print("data:"+str(data))
        else:
            # replacement policy is LRU
            set_val = set_ans
            line_num = 0
            min = cache[set_val][line_num][4]

            for i in range(0,E):
                if cache[set_val][i][4] < min:
                    line_num = i
                    min = cache[set_val][i][4]
            print("eviction_line:"+ str(line_num))
            print("ram_address:"+address)
            temp = (int(address, 16) // B) * B
            ram_tag = cache[set_val][line_num][2]
            ram_tag = bin(int(ram_tag, 16))
            update_set = bin(set_val)
            update_set = update_set[2::]
            update_set = update_set.zfill(set_width)
            update_block =""
            update_block = update_block.zfill(block_width)
            update_address = ram_tag+update_set+update_block
            update_ram = (int(update_address, 2))
            if cache[set_val][line_num][1] == 1:
                for i in range(0,B):
                    ram[hex(update_ram)] = cache[set_val][line_num][3][i]
                    update_ram+=1
            cache[set_val][line_num][0] = 1
            cache[set_val][line_num][1] = 0
            cache[set_val][line_num][3] = []
            cache[set_val][line_num][2] = tag_ans

            for i in range(0, B):
                cache[set_val][line_num][3].append(ram[hex(temp)])
                temp += 1
            cache[set_val][line_num][4] = time_cycle
            data = cache[set_val][line_num][3][block_ans]
            data = "0x" + data
            print("data:"+ str(data))
    else:
        # cache hit
        print("eviction_line:-1")
        print("ram_address:-1")
        print("data:" + str(data))


def write_back(address, data, time_cycle):
    # write hit
    # only in cache, dirty = 1 always
    res = bin(int(address, 16))
    res = res[2::]
    res = res.zfill(8)
    block_num = res[(8 - block_width)::]
    block_offset = int(block_num, 2)

    set_num = res[(8 - block_width - set_width):(8 - block_width)]
    set_num = "0b" + set_num
    set_ans = int(set_num, 2)
    tag_num = res[0:8 - block_width - set_width]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2))
    tag_ans = tag_ans[2::]

    # find the address in cache
    # set that to data
    # set dirty to 1
    # data = data[2::]
    for j in cache[set_ans]:
        if len(tag_ans) == 1:
            tag_ans = "0"+tag_ans
        if j[0] == 1 and j[2] == tag_ans:
            j[4] == time_cycle
            j[3][block_offset] = data
            j[1] = 1


def write_through(address, data, time_cycle):
    # write hit
    # write to cache and RAM
    res = bin(int(address, 16))
    res = res[2::]
    res = res.zfill(8)
    block_num = res[(8 - block_width)::]
    block_offset = int(block_num, 2)

    set_num = res[(8 - block_width - set_width):(8 - block_width)]
    set_num = "0b" + set_num
    set_ans = int(set_num, 2)
    tag_num = res[0:8 - block_width - set_width]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2))
    tag_ans = tag_ans[2::]
    # find address in cache
    # set to data
    # find address in RAM and set to data
    # data = data[2::]

    temp = int(address, 16)
    for j in cache[set_ans]:
        if len(tag_ans) == 1:
            tag_ans = "0"+tag_ans
        if j[0] == 1 and j[2] == tag_ans:
            j[4] = time_cycle
            j[3][block_offset] = data
    ram[hex(temp)] = data


def write_allocate(address, data, time_cycle,set_ans, tag_ans):
    # write miss
    # load data from RAM and call the write_hit

    # based on eviction property for write to cache
    # random replacement
    if replace == 1:
        line_num = randint(0, E-1)
        set_val = set_ans
        temp = (int(address, 16) // B) * B
        # finding address of the line that is being evicted
        ram_tag = cache[set_val][line_num][2]
        ram_tag = bin(int(ram_tag, 16))
        update_set = bin(set_val)
        update_set = update_set[2::]
        update_set = update_set.zfill(set_width)
        update_block = ""
        update_block = update_block.zfill(block_width)
        update_address = ram_tag + update_set + update_block
        update_ram = (int(update_address, 2))
        # writing that line to RAM if the dirty bit is 1, before evicting the line
        if cache[set_val][line_num][1] == 1:
            for i in range(0, B):
                ram[hex(update_ram)] = cache[set_val][line_num][3][i]
                update_ram += 1
        # overwriting the line now with required data
        cache[set_val][line_num][0] = 1
        cache[set_val][line_num][1] = 0
        cache[set_val][line_num][3] = []
        cache[set_val][line_num][2] = tag_ans
        for i in range(0, B):
            cache[set_val][line_num][3].append(ram[hex(temp)])
            temp += 1
        cache[set_val][line_num][4] = time_cycle
    # LRU
    else:
        set_val = set_ans
        line_num = 0
        min = cache[set_val][line_num][4]
        for j in range(0, E):
            if cache[set_val][j][4] < min:
                line_num = j
                min = cache[set_val][j][4]
        temp = (int(address, 16) // B) * B
        ram_tag = cache[set_val][line_num][2]
        ram_tag = bin(int(ram_tag, 16))
        update_set = bin(set_val)
        update_set = update_set[2::]
        update_set = update_set.zfill(set_width)
        update_block = ""
        update_block = update_block.zfill(block_width)
        update_address = ram_tag + update_set + update_block

        update_ram = (int(update_address, 2))
        if cache[set_val][line_num][1] == 1:
            for i in range(0, B):
                ram[hex(update_ram)] = cache[set_val][line_num][3][i]
                update_ram += 1
        cache[set_val][line_num][0] = 1
        cache[set_val][line_num][1] = 0
        cache[set_val][line_num][3] = []
        cache[set_val][line_num][2] = tag_ans
        for i in range(0, B):
            cache[set_val][line_num][3].append(ram[hex(temp)])
            temp += 1
        cache[set_val][line_num][4] = time_cycle

    # call write_hit once loaded into cache
    if write_hit_pol == 1:
        write_through(address, data, time_cycle)
        dirty_bit = 0
    else:
        write_back(address, data, time_cycle)
        dirty_bit = 1

    return line_num, dirty_bit


def write_no_allocate(address, data, time_cycle):
    # just change RAM
    ram[hex(int(address, 16))] = data


def cache_write(address, data):
    global time_cycle
    time_cycle += 1
    res = bin(int(address, 16))
    res = res[2::]
    res = res.zfill(8)

    set_num = res[(8 - block_width - set_width):(8 - block_width)]
    set_num = "0b" + set_num
    set_ans = int(set_num, 2)
    # set_print = hex(set_ans).upper()
    # set_print = set_print[2::]
    # set_print = set_print.zfill(2)
    print("set:" + str(set_ans))
    tag_num = res[0:8-block_width-set_width]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2)).upper()
    tag_ans = tag_ans[2::]
    tag_print = tag_ans.zfill(2)
    print("tag:"+tag_print)
    # calculating required factors to find if the address value is in the cache or not
    hit = "no"
    for j in cache[set_ans]:
        if len(tag_ans) == 1:
            tag_ans = "0"+tag_ans
        if j[0] == 1 and j[2] == tag_ans:
            hit = "yes"

    print("write_hit:" + str(hit))
    data_clean = data[2::]
    # for cache hit
    if hit == "yes":
        global num_hit
        num_hit += 1
        line_num = -1
        if write_hit_pol == 1:
            write_through(address, data_clean, time_cycle)
            dirty_bit = 0
        else:
            write_back(address, data_clean, time_cycle)
            dirty_bit = 1
        print("eviction_line:" + str(line_num))
        print("ram_address:-1")
    else:
        # for cache miss
        global num_miss
        num_miss += 1
        if write_miss_pol == 1:
            line_num, dirty_bit = write_allocate(address, data_clean, time_cycle, set_ans, tag_ans)
            print("eviction_line:" + str(line_num))
            print("ram_address:" + address)
        else:
            write_no_allocate(address, data_clean, time_cycle)
            dirty_bit = 0
            line_num = -1
            print("eviction_line:" + str(line_num))
            print("ram_address:-1")
    print("data:" + str(data))
    print("dirty_bit:" + str(dirty_bit))


# cache dump
def write_cache():
    outputfile = open("cache.txt","w")
    for val in cache.values():
        for i in val:
            output_str = ""
            for j in range(0,B):
                output_str += i[3][j]
                output_str += " "
            output_str += "\n"
            outputfile.write(output_str)
    outputfile.close()


# memory dump
def write_memory():
    outputfile = open("ram.txt", "w")
    for i in ram:
        outputfile.write(ram[i]+"\n")
    outputfile.close()


# cache initialize to begin with and to flush
def cache_initialize():
    list = []
    for i in range(0, B):
        list.append("00")
    for i in range(0, S):
        cache[i] = []
        for j in range(0, E):
            cache[i].append([0, 0, "00", list, 0])


num_hit = 0
num_miss = 0
memory_size = 256
S = int(C/B/E)
set_width = int(log(S, 2))
block_width = int(log(B, 2))

time_cycle = 0
cache_initialize()


while True:
    print("*** Cache simulator menu ***\n"
          "type one command:\n"
          "1. cache-read\n"
          "2. cache-write\n"
          "3. cache-flush\n"
          "4. cache-view\n"
          "5. memory-view\n"
          "6. cache-dump\n"
          "7. memory-dump\n"
          "8. quit\n"
          "**************************")
    command = input()
    if command[0:10] == "cache-read":
        command = command.split(" ")
        address = command[1]
        address = address[2::]
        if len(address) > 2:
            print("Invalid input")
            continue
        cache_read(address)
    elif command[0:11] == "cache-write":
        command = command.split(" ")
        if len(command)!= 3:
            print("Invalid input")
            continue
        address = command[1]
        data = command[2]
        if len(address) > 4 or len(data) > 4:
            print("Invalid input")
            continue
        cache_write(address, data)
    elif command == "cache-flush":
        # writing lines with dirty bit 1 to the RAM before flushing
        for key, val in cache.items():
            for i in val:
                if i[1] == 1:
                    ram_tag = i[2]
                    ram_tag = bin(int(ram_tag, 16))
                    update_set = bin(key)
                    update_set = update_set[2::]
                    update_set = update_set.zfill(set_width)
                    update_block = ""
                    update_block = update_block.zfill(block_width)
                    update_address = ram_tag + update_set + update_block
                    update_ram = (int(update_address, 2))
                    for j in range(0, B):
                        ram[hex(update_ram)] = i[3][j]
                        update_ram += 1
        cache_initialize()
        print("cache_cleared")
    elif command == "cache-view":
        print("cache_size:" + str(C))
        print("data_block_size:" + str(B))
        print("associativity:" + str(E))
        if replace == 1:
            print("replacement_policy:random_replacement")
        else:
            print("replacement_policy:least_recently_used")
        if write_hit_pol == 1:
            print("write_hit_policy:write_through")
        else:
            print("write_hit_policy:write_back")
        if write_miss_pol == 1:
            print("write_miss_policy:write_allocate")
        else:
            print("write_miss_policy:no_write_allocate")
        print("number_of_cache_hits:" + str(num_hit))
        print("number_of_cache_misses:" + str(num_miss))
        print("cache_content:")
        for key, val in cache.items():
            for i in val:
                print(i[0], i[1], i[2], end=" ")
                output_str = ""
                for j in range(0, B):
                    output_str += i[3][j]
                    output_str += " "
                print(output_str)
    elif command == "memory-view":
        print("memory_size:" + str(memory_size))
        print("memory_content:")
        print("Address:Data")
        count = 0

        for val in ram.values():
            if count % 8 == 0:
                output_temp = hex(count).upper()
                output_temp = output_temp[2::]
                if len(output_temp) == 1:
                    output_temp = "0x0" + output_temp
                else:
                    output_temp = "0x" + output_temp
                print(output_temp + ":" + val, end=" ")

            elif count % 8 == 7:
                print(val, end="\n")

            else:
                print(val, end=" ")
            count += 1
    elif command == "cache-dump":
        write_cache()
    elif command == "memory-dump":
        write_memory()
    elif command == "quit":
        exit()
    else:
        print("Invalid command, try again")
