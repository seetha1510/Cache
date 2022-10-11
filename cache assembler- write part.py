from math import*
from random import randint
ram = {}
cache = {

}

# cache: key : matrix (valid, dirty, tag, content, fre)
# content is a list[] without 0x
# set is in decimal, tag is in hex without the 0x,
# value has to be matrix
# ram key: 0x_ _ value: hex (with no 0x)



def filereader(filname):
    global icontent
    icontent = []
    readfile=open(filename+".txt")
    for line in readfile:
        icontent.append(line)
    readfile.close()

filename = input("Please provide a file name for initialized ram: ")
filereader(filename)
for i in range(0, 256):
    key = hex(i)
    ram[key] = icontent[i]




print("*** Welcome to the cache simulator ***\ninitialize the RAM:\ninit-ram 0x00 0xFF\nram successfully initialized!")
C = int(input("Provide a cache size:"))
B = int(input("Provide a data block size:"))
E = int(input("Provide Associativity, can either be 1 or 2 or 4 way:"))
replace = int(input("Provide replacement policy, 1 for RR and 2 for LRU:"))
# change!! variables
write_hit_pol = int(input("Provide write hit policy, 1 for write through and 2 for write back:"))
write_miss_pol = int(input("Provide write miss policy, 1 for write-allocate and 2 for no write-allocate:"))

print("\nconfigure the cache:")
print("cache size:", C )
print(" data block size: ", B)
print("associativity: ", E)
print("replacement policy: ",replace)
print("write hit policy: ",write_hit_pol)
print("write miss policy: ",write_miss_pol)
print("cache successfully configured!")



def cache_read(address):
    global frequency
    frequency +=1
    res = bin(int(address,16))
    res = res[2::]
    res = res.zfill(8)
    block_num = res[(8-block_width)::]
    block_ans = int(block_num, 2)

    set_num = res[(8 - block_width-set_width):(8 - block_width)]
    set_num = "0b" + set_num
    set_ans = int(set_num, 2)
    print("set:", set_ans)
    tag_num = res[0:8-block_width-set_width-1]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num,2))
    print(len(tag_ans))
    tag_ans = tag_ans[2::]
    print("tag:",tag_ans)
    hit = "no"
    data = ""
    for i in cache():
        if (set_ans ==i):
            for j in range(0,E):
                if (cache[i][j][0] == 1 and cache[i][j][2] == tag_ans):
                    hit = "yes"
                    data = cache[i][j][3][block_ans]
                    data = "0x" + data


    print("hit:",hit)
    if (hit == "no"):
        if (replace == 1):
            range = E * S-1
            value = randint(0, range)
            set_val = ceil((value+1)/E)
            line_num = value % E
            print("eviction_line:",line_num) #ask rohan
            print("ram_address:",address)
            temp = (int(address,16) // B)*B
            cache[set_val][line_num][0] = 1
            cache[set_val][line_num][1] = 0
            cache[set_val][line_num][3] = []
            for i in range(0, B):
                cache[set_val][line_num][3].append(hex(temp)) #appenf(ram[hex(temp)])
                temp +=1
            cache[set_val][line_num][4]=frequency
            data = cache[set_val][line_num][3][block_ans]
            data = "0x" + data
            print("data:",data)
        else:
            set_val = 0
            line_num = 0
            min = 0
            for i in cache:
                for j in range(0,E):
                    if (cache[i][j][4] < min):
                        set_val = i
                        line_num = j
                        min = cache[i][j][4]
            if (min==0):
                line_num = 0
                set_val = 0
            print("eviction_line:", line_num)  # ask rohan what is the line number
            print("ram_address:", address)
            temp = (int(address, 16) // B) * B
            cache[set_val][line_num][0] = 1
            cache[set_val][line_num][1] = 0
            cache[set_val][line_num][3] = []
            for i in range(0, B):
                cache[set_val][line_num][3].append(hex(temp))
                temp += 1
            cache[set_val][line_num][4] = frequency
            data = cache[set_val][line_num][3][block_ans]
            data = "0x" + data
            print("data:", data)
    else:
        print("eviction_line:",-1)
        print("ram_address:",-1)
        print("data:", data)


def write_back(address, data, frequency):
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
    tag_num = res[0:8 - block_width - set_width - 1]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2))

    # find the address in cache
    # set that to data
    # set dirty to 1
    data = data[2::]
    for j in cache[set_ans]:
        if j[0] == 1 and j[2] == tag_ans:
            j[4] == frequency
            j[3][block_offset] = data
            j[1] = 1


def write_through(address, data, frequency):
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
    tag_num = res[0:8 - block_width - set_width - 1]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2))

    # find address in cache
    # set to data
    # find address in RAM and set to data
    data = data[2::]
    temp = (int(address, 16) // B) * B
    for j in cache[set_ans]:
        if j[0] == 1 and j[2] == tag_ans:
            j[4] = frequency
            j[3][block_offset] = data

    ram[hex(temp)] = data


def write_allocate(address, data, frequency):
    # write miss
    # load data to RAM and call the write_hit

    # do based on eviction property for write to cache
    # PLEASE UPDATE BASED ON WHAT YOU HAVE FOR EVICTION IN READ
    if replace == 1:
        range = E - 1
        line_num = randint(0, range)  # was called value
        set_val = ceil((value + 1) / E)
        # line_num = value
        temp = (int(address, 16) // B) * B
        cache[set_val][line_num][0] = 1
        cache[set_val][line_num][1] = 0
        cache[set_val][line_num][3] = []
        # loop?
        for i in range(0, B):
            cache[set_val][line_num][3].append(hex(temp))  # append(ram[hex(temp)])
            temp += 1
        cache[set_val][line_num][4] = frequency

    else:
        set_val = 0
        line_num = 0
        min = 0
        for i in cache:
            for j in range(0, E):
                if cache[i][j][4] < min:
                    set_val = i
                    line_num = j
                    min = cache[i][j][4]
        temp = (int(address, 16) // B) * B
        cache[set_val][line_num][0] = 1
        cache[set_val][line_num][1] = 0
        cache[set_val][line_num][3] = []
        for i in range(0, B):
            cache[set_val][line_num][3].append(ram[hex(temp)])
            temp += 1
        cache[set_val][line_num][4] = frequency

    # call write_hit once loaded into cache
    if write_hit_pol == 1:
        write_back(address, data, frequency)
        dirty_bit = 1
    else:
        write_through(address, data, frequency)
        dirty_bit = 0

    return line_num, dirty_bit


def write_no_allocate(address, data, frequency):
    # just change RAM
    ram[hex(address)] = data


def cache_write(address, data):
    global frequency
    frequency += 1
    res = bin(int(address, 16))
    res = res[2::]
    res = res.zfill(8)
    # block_num = res[(8 - block_width)::]
    # block_ans = int(block_num, 2)

    set_num = res[(8 - block_width - set_width):(8 - block_width)]
    set_num = "0b" + set_num
    set_ans = int(set_num, 2)
    print("set:", set_ans)
    tag_num = res[0:8 - block_width - set_width - 1]

    tag_num = "0b" + tag_num
    tag_ans = hex(int(tag_num, 2))
    print(len(tag_ans))
    tag_ans = tag_ans[2::]
    print("tag:", tag_ans)
    hit = "no"

    for j in cache[set_ans]:
        if j[0] == 1 and j[2] == tag_ans:
            hit = "yes"

    print("write_hit:", hit)

    if hit == "yes":
        num_hit += 1
        line_num = -1
        if write_hit_pol == 1:
            write_through(address, data, frequency)
            dirty_bit = 0
        else:
            write_back(address, data, frequency)
            dirty_bit = 1
    else:
        num_miss += 1
        if write_miss_pol == 2:
            line_num, dirty_bit = write_allocate(address, data, frequency)
        else:
            write_no_allocate(address, data, frequency)
            dirty_bit = 0  # what to set  it to?
            line_num = -1

    print("eviction line:", line_num)
    print("ram address:", address)
    print("data:", data)
    print("dirty_bit:", dirty_bit)


# cache-dump
def write_cache():
    outputfile = open("cache.txt","w")
    for i in cache:
        outputfile.write(cache[i])
    outputfile.close()
# memory-dump
def write_memory():
    outputfile = open("ram.txt", "w")
    for i in ram:
        outputfile.write(ram[i])
    outputfile.close()



num_hit = 0
num_miss = 0
memory_size=256
S = C/B/E
set_width = log(S,2)
block_width = log(B,2)

frequency = 0



while True:
    print("\n*** Cache simulator menu ***\n"
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
    if command == "cache-read":
        address = input() # the input is one string or two
        address = address[2:-1]
        cache_read(address)
    elif command == "cache-write":
        print("no")
        #cache_write()
    elif command == "cache-flush":
        cache.clear();
    elif command == "cache-view":
        print("cache size:", C)
        print(" data block size:", B)
        print("associativity:", E)
        if (replace == 1):
            print("replacement policy:random_replacement")
        else:
            print("replacement policy:least_recently_used")
        if (write_hit == 1):
            print("write_hit_policy:write_through")
        else:
            print("write_hit_policy:write_back")
        if (write_miss == 1):
            print("write_miss_policy:write_allocate")
        else:
            print("write_miss_policy:no_write_allocate")
        print("number_of_cache_hits:", num_hit)
        print("number_of_cache_misses:",num_miss)
        print("cache_content:")
        for key, val in cache.items():
            for i in val:
                print(i[0]," ",i[1]," ",i[2], " ",i[3][0], " ",i[3][1], " ",i[3][2], " ",i[3][3], " ",i[3][4], " ",i[3][5], " ",i[3][6], " ",i[3][7])
    elif command == "memory-view":
        print("memory_size:", memory_size)
        print("memory_content:")
        print("Address:Data")
        pricount = 0
        count =0
        list = []
        for key, val in ram.items():
            list.append(val)
            if (count % 8 == 0 and count !=0):
                print(hex(pricount), ":",list[0]," ",list[1]," ",list[2]," ",list[3]," ",list[4]," ",list[5]," ",list[6]," ",list[7])
            else:
                print(val,end=" ")
            count+=1
    elif command == "cache-dump":
        write_cache()
    elif command == "memory-dump":
        write_memory()
    elif command == "quit":
        exit()
