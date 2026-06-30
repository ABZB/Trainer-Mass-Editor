import csv
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from functools import reduce
import os


def load_text_from_csv(path, thing_to_do_things_to, column = -1):
    with open(path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into the array      
        thing_to_do_things_to = list(reader_head)

        if(column >= 0):
            temp = []

            for x in thing_to_do_things_to:
                temp.append(x[column])
            thing_to_do_things_to = temp


        return(thing_to_do_things_to)


#read input bytestring as little-endian, return integer
def from_little_bytes_int(byte_input, length = 0, start = 0):
    temp = 0
    temp_bytes = []
    if(length == 0):
        temp_bytes = byte_input
    else:
        temp_bytes = byte_input[start:start + length]


    for x, byte in enumerate(temp_bytes):
        temp += byte << (x*8)
    return(temp)

#convert integer input into little-endian hex with given padding (default 0x4 bytes)
def from_int_little_bytes(decimal_number, padding = 0x4):
    return(decimal_number.to_bytes(padding, 'little'))

def binary_file_to_array(file_path):

    with open(file_path, "r+b") as f:
        f.seek(0, os.SEEK_END)
        file_end = f.tell()
        f.seek(0, 0)
        return(list(f.read(file_end)))

def deconstruct_GARC(path, game):
    
    bindata = binary_file_to_array(path)

    #header:
    # 0x4 Header length (4 bytes)
    # 0x10 Data start (4 bytes)
    # 0x14 total file length (4 bytes)

    #then depends on version
        
    # V4
    # 0x18 largest file size (unpadded)

    # V6

    # 0x18 largest file size (with padding if it exists)
    # 0x1C largest file size (without padding, virtually always equal to the above for our purposes)
    # 0x20 Padding value (usually 0x4)

    #counting from end of whatever version you're in (so 0x4 = 0x1C in v4, 0x24 in v6)

    # 0x8 FAT0 header length (counting from 0x4)
    # 0xC, number of files (2 bytes)
    # from 0x10, 4 bytes per file, each one is 0x10 times file number (start from 0)
        

    #from end of above, 0x4 - header length
    # 0x8 - file count, then 
    # then for each file, 0x01 00 00 00, then offset start, offset end, and file length, offset counting first byte of first file as 0x0

    #finally, last magic word, then header length (0xC), then length of actual data (same as final offset end from previous section

    #get Fat0 offset
    FAT0_offset = 0
    if(game in {"XY", "ORAS"}):
        FAT0_offset = 0x1C
    else:
        FAT0_offset = 0x24
        
        
    FATB_offset = FAT0_offset + from_little_bytes_int(bindata[FAT0_offset + 0x4:FAT0_offset + 0x8])

    file_count = from_little_bytes_int(bindata[FAT0_offset + 0x8:FAT0_offset + 0xA])

    data_absolute_offset = from_little_bytes_int(bindata[0x10:0x14])


    output_array = []

    #0xC is start of the actual file location/length data.
    FATB_offset += 0xC

    #iterate over the files, pulling the length from the FATB data, each file gets its own array in temp
    for _ in range(file_count):
            
        #move data pointer to start of next file
        data_offset = data_absolute_offset + from_little_bytes_int(bindata[FATB_offset + 0x4:FATB_offset + 0x8])
        #print(data_offset)
        #get length of current file
        file_length = from_little_bytes_int(bindata[FATB_offset + 0xC:FATB_offset + 0x10])

        #append the file to a new entry in output array
        output_array.append(bindata[data_offset:data_offset + file_length])
            

        #the offset end is different than start + length because length is padded to multiple of 4.

        #move to next file in FATB data
        FATB_offset += 0x10

    return(output_array)

def reconstruct_GARC(final_binary, GARC_name, game):
    
    match GARC_name:
        case "personal":
            #merges concatenated file for output
            out_file = final_binary + [reduce(lambda i, j: i+j, final_binary)]
        case "model":
            #merges with header for output
            #pass two array of arrays
            out_file = [reduce(lambda i, j: i+j, final_binary)]
        case _:
            out_file = final_binary
            
            
    file_count = len(out_file)

    temp = [0x0]*0x1C
    FAT0_offset = 0

    #magic GARC
    temp[0:4] = [0x43, 0x52, 0x41, 0x47]

    #Endian
    temp[0x08:0xA] = [0xFF, 0xFE]

    #header length and Version
    if(game in {"XY", "ORAS"}):
        temp[0x4] = 0x1C
        temp[0xB] = 0x04
        FAT0_offset = 0x1C
    else:
        temp[0x4] = 0x24
        temp[0xB] = 0x06
        temp.extend([0]*8)
        FAT0_offset = 0x24

    #section count
    temp[0xC] = 0x4

    #FAT0 Header allocation
    temp.extend([0]*(0xC + 4*file_count))
    
    #Magic FAT0
    temp[FAT0_offset:FAT0_offset + 4] = [0x4F, 0x54, 0x41, 0x46]
    
    #FAT0 length
    temp[FAT0_offset + 0x4:FAT0_offset + 0x8] = from_int_little_bytes(file_count*4 + 0xC, 0x4)

    #file count
    temp[FAT0_offset + 0x8:FAT0_offset + 0xA] = from_int_little_bytes(file_count, 0x2)

    #padding
    temp[FAT0_offset + 0xA:FAT0_offset + 0xC] = [0xFF, 0xFF]

    #write FAT0 thing
    pointer = FAT0_offset + 0xC
    for x in range(file_count):
        temp[pointer:pointer + 4] = from_int_little_bytes(x * 0x10, 0x4)
        pointer += 0x4


    #allocate BFAT, 0xC for header, then 0x10 per file
    temp.extend([0]*(0xC + 0x10*file_count))
    #magic BFAT
    temp[pointer:pointer + 4] = [0x42, 0x54, 0x41, 0x46]

    pointer +=4

    #BFAT length
    temp[pointer:pointer + 4] = from_int_little_bytes(file_count*0x10 + 0xC, 0x4)

    pointer +=4

    #BFAT file count
    temp[pointer:pointer + 2] = temp[FAT0_offset + 0x8:FAT0_offset + 0xA]

    pointer += 4

    #before we write the BFAT blocks, add the FIMB header so we can write those blocks and actual files at once

    #this will point at end of file
    fimb_pointer = len(temp)

    temp.extend([0]*(0xC))
    
    #magic FIMB
    temp[fimb_pointer :fimb_pointer  + 4] = [0x42, 0x4D, 0x49, 0x46]
    
    fimb_pointer  += 4

    #FIMB header length (3 high bytes are zero)
    temp[pointer] = [0x0C]


    #need to update this with final offset below
    fimb_pointer  += 4


    data_pointer = len(temp)

    #update GARC header with data start

    temp[0x10:0x14] = from_int_little_bytes(data_pointer, 0x4)

    offset = 0
    biggest_size = 0
    biggest_size_padding = 0
    for file in out_file:
        
        #padding
        temp[pointer:pointer + 4] = [0x01, 0x00, 0x00, 0x00]

        #offset start
        temp[pointer + 4: pointer + 8] = from_int_little_bytes(offset, 0x4)

        length = len(file)
        
        
        biggest_size = max(length, biggest_size)
        padding = (length - 4) % 4
        biggest_size_padding = max(length + padding, biggest_size_padding)
        offset += length + padding

        #offset end. When there is padding to z bytes, those extra bytes are filled with 0xFF, are NOT counted in the length, but ARE counted in the end-address
        temp[pointer + 8: pointer + 0xC] = from_int_little_bytes(offset, 0x4)

        #length
        temp[pointer + 0xC: pointer + 0x10] = from_int_little_bytes(length, 0x4)


        #extend temp by length of file
        temp.extend([0]*length)
        #write file to location
        temp[data_pointer: data_pointer + length] = file

        if(padding != 0):
            temp.extend([0xFF]*padding)

        data_pointer += length + padding

        pointer += 0x10

    #write total length of files
    temp[fimb_pointer:fimb_pointer + 4] = from_int_little_bytes(offset, 0x4)

    #in GARC header, need to write file length, and largest file size (plus padded max and padding in gen 7)

    #only write largest file size at FAT0_offset - 4
    if(game in {"XY", "ORAS"}):
        temp[FAT0_offset - 0x4:FAT0_offset] = from_int_little_bytes(biggest_size, 0x4)
    
    #starting from FAT0_offset - 0xC:
    #max of 0x4 and max file size
    #max file size
    #padding (0x4)
    else:
        temp[FAT0_offset - 0xC:FAT0_offset - 0x8] = from_int_little_bytes(biggest_size_padding, 0x4)
        temp[FAT0_offset - 0x8:FAT0_offset - 0x4] = from_int_little_bytes(biggest_size, 0x4)
        temp[FAT0_offset - 0x4:FAT0_offset] = from_int_little_bytes(0x4, 0x4)

    #write total length of entire GARC
    temp[0x14:0x18] = from_int_little_bytes(len(temp), 0x4)


    return(temp)

def save_GARC(final_binary, GARC_name, file_path, game):



    temp = reconstruct_GARC(final_binary, GARC_name, game)

    with open(file_path, "w+b") as f:
        f.write(bytes(temp))


#loads list of filenames in extracted GARC if it exists, otherwise return empty array
def load_GARC(game, garc_path, target):

    if(os.path.exists(garc_path)):

        return(deconstruct_GARC(garc_path, game))



    else:
        print("Garc folder not found, unreadable, or empty")