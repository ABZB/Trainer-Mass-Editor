from encodings import utf_16_le, utf_8
from generic_garc_handling import *
from constants import *
import os

class trainerdata:
    def __init__(self):
        self.game = ''
        self.trainer_name_list_royale = ['trainer_list_royale.csv']
        self.trainer_name_list_tree = ['trainer_list_tree.csv']
        self.trainer_name_list_world = ['trainer_list_world.csv']
        self.ability_name_list = ['custom_ability_list.csv']
        self.item_name_list = ['custom_item_list.csv']
        self.pokemon_name_list = ['custom_pokemon_list.csv']
        self.move_name_list = ['custom_move_list.csv']

        self.trainer_path = ''
        self.pokemon_path = ''

        self.trainer_binary = []
        self.pokemon_binary = []
        self.personal_binary = []

        self.trainer_file_name = ''
        self.pokemon_file_name = ''
        self.personal_file_name = ''


def get_int_range(entry, offset, length):
    return(from_little_bytes_int(entry[offset:offset + length]))

def print_regular_trainer_csv(working_data):
    temp = []

    #write Pokemon
    with open(asksaveasfilename(title='Save Table of Trainers', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as trainerfile:
        trainerhead = csv.writer(trainerfile, dialect='excel', delimiter=',')

        #write header row
        trainerhead.writerow(['Index', 'Trainer Class', 'Trainer Name', 'Party Size', 'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Basic AI', 'Strong AI', 'Expert AI', 'Doubles AI', 'No Whiteout', 'Battle Royale AI', 'Switching AI', 'Trainer Item AI', 'Master AI', 'Money'])


        with open(asksaveasfilename(title='Save Table of Pokemon', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as pokefile:
            pokehead = csv.writer(pokefile, dialect='excel', delimiter=',')



            poke_index = 0

            for count, entry in enumerate(working_data.trainer_binary):
                
                #index
                trainer_temp = [count]

                #class
                trainer_temp.append(trainer_class_names[get_int_range(entry, 0, 2)])

                #name
                trainer_temp.append(working_data.trainer_name_list_world[count])

                #party size
                trainer_temp.append(get_int_range(entry, 3, 1))

                #first trainer at index 0 has no Pokemon, and the 0 index Pokemon file is actually completely empty, so get errors
                if(count == 0):
                    pokehead.writerow(['Trainer Index', 'Trainer', 'Pokemon',  'Level', 'Gender', 'Ability', 'Nature', 'Item', 'Friendship', 'Shiny', 'HP IV', 'Atk IV', 'Def IV', 'SpA IV', 'SpD IV', 'Spe IV',  'HP EV', 'Atk EV', 'Def EV', 'SpA EV', 'SpD EV', 'Spe EV', 'Move 1', 'Move 2', 'Move 3', 'Move 4'])
                    continue

                #get this trainer's team GARC
                teamentry = working_data.pokemon_binary[count]
                #now have everything to write the Pokemon for this trainer
                for x in range(trainer_temp[3]):
                    #trainer index and name

                    poketemp = []

                    poketemp.append(trainer_temp[0])
                    poketemp.append(trainer_temp[1] + ': ' + trainer_temp[2])

                    #get the slice that is the xth member of the team
                    pokentry = teamentry[x*0x20:x*0x20 + 20]
                   

                    #pokemon name
                    pokemon_index = get_int_range(pokentry, 0x10, 2)
                    forme_number = get_int_range(pokentry, 0x12, 1)
                    try:
                        if(forme_number != 0):
                            #index of first alt forme + forme number - 1 = index of this particular alt forme (e.g. forme 1 is the pointer index)
                            possible_index = forme_number + get_int_range(working_data.personal_binary[pokemon_index], 0x1C, 2) - 1
                            pokemon_index = possible_index if possible_index >= pokemon_index else pokemon_index
                        poketemp.append(working_data.pokemon_name_list[pokemon_index])
                    except:
                        print(f'Pokemon {pokemon_index}, forme {forme_number} not recognized')

                    #level
                    poketemp.append(get_int_range(pokentry, 0xE, 1))

                    #gender
                    match get_int_range(pokentry, 0x0, 1) & 0x3:
                        case 0:
                            poketemp.append('Random/Genderless')
                        case 2:
                            poketemp.append('Female')
                        case 1:
                            poketemp.append('Male')

                    #Ability
                    match (get_int_range(pokentry, 0x0, 1) >> 4) & 0x3:
                        case 0:
                            poketemp.append('1 or 2')
                        case 1:
                            poketemp.append('1')
                        case 2:
                            poketemp.append('2')
                        case 3:
                            poketemp.append('H')

                    #nature
                    poketemp.append(nature_names[get_int_range(pokentry, 0x1, 1)])

                    #hold item
                    poketemp.append(working_data.item_name_list[get_int_range(pokentry, 0x14, 2)])

                    #friendship
                    poketemp.append(get_int_range(pokentry, 0xC, 1))

                    iv_block = get_int_range(pokentry, 0x8, 4)

                    #shiny
                    poketemp.append('True' if ((iv_block >> 0x30) & 1 == 1) else 'False')

                    #IVs
                    for x in range(6):
                        poketemp.append((iv_block >> (x*5)) & 0x1F)

                    #Evs
                    for x in range(6):
                        poketemp.append(get_int_range(pokentry, 0x2 + x, 1))


                    #moves
                    for x in range(4):
                        try:
                            poketemp.append(working_data.move_name_list[get_int_range(pokentry, 0x18 + x*2, 2)])
                        except:
                            print(f'Move index {get_int_range(pokentry, 0x18 + x*2, 2)} not recognized')

                    #write Pokemon row
                    pokehead.writerow(poketemp)

                #items
                for x in range(4):
                     trainer_temp.append(working_data.item_name_list[get_int_range(entry, 0x04 + x*2, 2)])
                
                #9 AI bits
                ai_lower = get_int_range(entry, 0xC, 2)
                for x in range(9):
                    trainer_temp.append('True' if ((ai_lower >> x) & 0x1) == 1 else '')

                trainer_temp.append(get_int_range(entry, 0x11, 1))

                trainerhead.writerow(trainer_temp)


def print_facility_trainer_csv(working_data, target_name):
    temp = []

    #write Pokemon
    with open(asksaveasfilename(title='Save Table of Facility Pokemon', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
        writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')

        #write header row
        writer_head.writerow(['Index', 'Pokemon', 'Move 1', 'Move 2', 'Move 3', 'Move 4', 'Perfect IVs', 'Nature', 'Item'])

        for count, entry in enumerate(working_data.pokemon_binary):
            
            #pokemon index:
            pokemon_index = from_little_bytes_int(entry[0:2])

            #forme #
            forme_number = entry[0xE]
            #if forme is 0, regular base pokemon
            #otherwise need to get absolute number to get right name
            if(forme_number != 0):
                #index of first alt forme + forme number - 1 = index of this particular alt forme (e.g. forme 1 is the pointer index)
                forme_number = forme_number + from_little_bytes_int(working_data.personal_binary[pokemon_index][0x1C:0x1E]) - 1

            ivs = ''
            iv_byte = entry[0xA]
            iv_names = ['HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD']
            for x in range(6):
                if (iv_byte & (1 << x) == (1 << x)):
                    ivs += (' | ' if len(ivs) > 0 else '') + iv_names[x]
                else:
                    ivs += (' | ' if len(ivs) > 0 else '') + '   '


            #write row
            writer_head.writerow([
                count, 
                working_data.pokemon_name_list[pokemon_index] if forme_number == 0 else working_data.pokemon_name_list[forme_number],
                *(working_data.move_name_list[from_little_bytes_int(entry[2 + 2*x: 4 + 2*x])] for x in range(4)), 
                ivs,
                nature_names[entry[0xB]],
                working_data.item_name_list[from_little_bytes_int(entry[0xC:0xE])]])

            temp.append(working_data.pokemon_name_list[pokemon_index] if forme_number == 0 else working_data.pokemon_name_list[forme_number])

    #write trainers
    with open(asksaveasfilename(title='Save Table of Facility Trainers', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
        writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')
        trainer_output = []
        max_poke_count = 0

        for count, entry in enumerate(working_data.trainer_binary):
            trainer_temp = []
            trainer_temp.append(count)
            #append trainer name
            if(target_name == 'Battle Tree'):
                trainer_temp.append(working_data.trainer_name_list_tree[count])
            else:
                trainer_temp.append(working_data.trainer_name_list_royale[count])
            #append trainer class
            trainer_temp.append(trainer_class_names[from_little_bytes_int(entry[0x0:0x2])])
            #append Pokemon pool size
            trainer_temp.append(from_little_bytes_int(entry[0x2:0x4]))

            #iterate over the rest of the pairs of bytes
            entry_count = (len(entry) - 4)//2

            max_poke_count = max(max_poke_count, entry_count)

            for x in range(entry_count):
                index = from_little_bytes_int(entry[0x4 + 2*x: 0x6 + 2*x])
                print(x, index)
                trainer_temp.append(f'{index}, {temp[index]}')

            trainer_output.append(trainer_temp)



            
        #write header row
        writer_head.writerow(['Index', 
                              'Trainer Name', 
                              'Trainer Class', 
                              'Pool Size', 
                              *(f'Pokemon {x + 1}' for x in range(max_poke_count))
                              ])

        for line in trainer_output:
            writer_head.writerow(line)


def export_from_GARC(working_data, target_name):

    #each entry in the array is a file in the deconstructed GARC
    working_data.trainer_binary = load_GARC(working_data.game, askopenfilename(title=f'Select Trainer Data {working_data.trainer_file_name}', defaultextension='',filetypes= [('','')]), target_name)

    working_data.pokemon_binary = load_GARC(working_data.game, askopenfilename(title=f'Select Pokemon Data {working_data.pokemon_file_name}', defaultextension='',filetypes= [('','')]), target_name)

    working_data.personal_binary = load_GARC(working_data.game, askopenfilename(title=f'Select Personal Data {working_data.personal_file_name}', defaultextension='',filetypes= [('','')]), 'Personal')

    #build table per trainer
    if(target_name == 'Regular Trainers'):
        print_regular_trainer_csv(working_data)
    #built two seperate files, one with trainers and what Pokemon indices and the other with the Pokemon
    else:
        print_facility_trainer_csv(working_data, target_name)

    return(working_data)


def read_regular_trainer_csv(working_data):
    pass


def read_facility_trainer_csv(working_data, target_name):
    #rebuild pokemon binary
    with open(askopenfilename(title=f'Select Pokemon Table To Import', defaultextension='csv',filetypes= [('CSV','.csv')]), newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        lines = list(reader_head)

        working_data.pokemon_binary = [[]]*(len(lines) - 1)


        if(working_data.personal_binary == []):
            working_data.personal_binary = load_GARC(working_data.game, askopenfilename(title=f'Select Personal Data {working_data.personal_file_name}', defaultextension='',filetypes= [('','')]), 'Personal')

        for x, line in enumerate(lines):
            if(x == 0):
                continue
            temp = [0]*16

            #determine forme and species index
            
            #absolute personal file
            absolute_index = working_data.pokemon_name_list.index(line[1])


            #get forme pointer
            forme_count = working_data.personal_binary[absolute_index][0x20]
            pointer = from_little_bytes_int(working_data.personal_binary[absolute_index][0x1C:0x1E])

            #multiple formes and absolute index is at least as big as pointer
            if(forme_count > 1 and pointer != 0 and pointer <= absolute_index):
                
                #search for base Pokemon
                for y, entry in enumerate(working_data.personal_binary):
                    temp_pointer = from_little_bytes_int(entry[0x1C:0x1E])

                    #found base pokemon
                    if(temp_pointer + entry[0x20] - 2 >= absolute_index):
                        #set base Pokemon index
                        temp[0:2] = y.to_bytes(2, 'little')
                        temp[0xE] = absolute_index - temp_pointer + 1
                        break

            else:
                temp[0:2] = absolute_index.to_bytes(2, 'little')

            

            #moves
            for move_position in range(4):
                temp[2 + move_position*2 : 4 + move_position*2] = working_data.move_name_list.index(line[move_position + 2]).to_bytes(2, 'little')

            #IVs
            iv_value = 0
            if 'HP' in line[6]:
                iv_value += 1
            if 'Atk' in line[6]:
                iv_value += 2
            if 'Def' in line[6]:
                iv_value += 4
            if 'Spe' in line[6]:
                iv_value += 8
            if 'SpA' in line[6]:
                iv_value += 16
            if 'SpD' in line[6]:
                iv_value += 32

            temp[0xA] = iv_value

            #nature
            temp[0xB] = nature_names.index(line[7])

            #item
            temp[0xC:0xE] = working_data.item_name_list.index(line[8]).to_bytes(2, 'little')



            working_data.pokemon_binary[x - 1] = temp

    return(working_data)

def import_to_GARC(working_data, target_name):

    #rebuild final binaries

    if(target_name == 'Regular Trainers'):
        read_regular_trainer_csv(working_data)
        save_GARC(working_data.trainer_binary, target_name, asksaveasfilename(title=f'Select Trainer Garc {working_data.trainer_file_name}', defaultextension='',filetypes= [('','')]), target_name)
    else:
        read_facility_trainer_csv(working_data, target_name)
    

    save_GARC(working_data.pokemon_binary, target_name, asksaveasfilename(title=f'Select Pokemon Garc {working_data.pokemon_file_name}', defaultextension='',filetypes= [('','')]), working_data.game)


def main():

    #initialize variables
    working_data = trainerdata()

    #get generation
    while True:
        temp = input('Enter Generation, (XY, ORAS, SM, USUM)\n').upper()
        if(temp in {'XY', 'ORAS', 'SM', 'USUM'}):
            working_data.game = temp
            break
        else:
            print(temp, 'is not valid\n\n')




    #get text data
    with open(os.path.join(os.getcwd(), 'paths.cfg'), 'r') as cfg:
        temp = [line.rstrip() for line in cfg]

        
        working_data.trainer_name_list_royale = load_text_from_csv(os.path.join(temp[0], working_data.trainer_name_list_royale[0]), working_data.trainer_name_list_royale, 1)
        working_data.trainer_name_list_tree = load_text_from_csv(os.path.join(temp[0], working_data.trainer_name_list_tree[0]), working_data.trainer_name_list_tree, 1)
        working_data.trainer_name_list_world = load_text_from_csv(os.path.join(temp[0], working_data.trainer_name_list_world[0]), working_data.trainer_name_list_world, 1)
        working_data.ability_name_list = load_text_from_csv(os.path.join(temp[0], working_data.ability_name_list[0]), working_data.ability_name_list, 1)
        working_data.item_name_list = load_text_from_csv(os.path.join(temp[0], working_data.item_name_list[0]), working_data.item_name_list, 1)
        working_data.pokemon_name_list = load_text_from_csv(os.path.join(temp[0], working_data.pokemon_name_list[0]), working_data.pokemon_name_list, 1)
        working_data.move_name_list = load_text_from_csv(os.path.join(temp[0], working_data.move_name_list[0]), working_data.move_name_list, 1)

    while True:

        #choose extract or rebuild
        while True:
            action_choice = input('\n(1) Extract GARC\n(2) Build GARC\n(Q) Quit?\n\n').lower()
            if(action_choice in {'1', '2', 'q'}):
                break
            else:
                print(action_choice, 'is not valid\\nn')
        if(action_choice == 'q'):
            return

        action_choice = 'Extract' if (action_choice == '1') else 'Build'

        while True:
            target_choice = input('\n(1) Regular Trainers\n(2) Battle Tree\n(3) Battle Royale?\n\n').lower()
            if(target_choice in {'1', '2', '3'}):
                break
            else:
                print(target_choice, 'is not valid\\nn')

        target_name = 'Battle Tree' if target_choice == '2' else 'Battle Royale' if target_choice == '3' else 'Regular Trainers'

        
        while True:
            
            proceed = input(f'\n{action_choice} GARCs for {target_name}? Y/N\n\n').lower()

            if(proceed in {'y', 'n', '1', '0'}):
                break
            else:
                print(f'{proceed} not understood')

        if(proceed in {'y', '1'}):


            #set up the file target for display
            match working_data.game:
                case 'USUM':
                    match target_name:
                        case 'Regular Trainers':
                            working_data.pokemon_file_name = 'a/1/0/7'
                            working_data.trainer_file_name = 'a/1/0/6'
                        case 'Battle Royale':
                            working_data.pokemon_file_name = 'a/2/8/3'
                            working_data.trainer_file_name = 'a/2/8/4'
                        case 'Battle Tree':
                            working_data.pokemon_file_name = 'a/2/8/1'
                            working_data.trainer_file_name = 'a/2/8/2'
                    working_data.personal_file_name = 'a/0/1/7'
                        

            match action_choice:
                case 'Extract':
                    export_from_GARC(working_data, target_name)
                case 'Build':
                    import_to_GARC(working_data, target_name)


def fix_bins():

    folder_path = askdirectory()

    with open(os.path.join(folder_path, str(1134).zfill(4) + '.bin'), 'r+b') as comp:
        for bin_number, file in enumerate(os.scandir(folder_path)):
            if(bin_number == 1134):
                break
            elif file.is_file():  # Check if it's a file
                with open(file, "r+b") as f:
                    f.seek(0x20)
                    forme_count = from_little_bytes_int(f.read(1))
                    f.seek(0x1C)
                    pointer = from_little_bytes_int(list(f.read(2)))

                    if(forme_count > 1 and pointer > 0 and not(pointer <= bin_number and pointer != 0)):
                        for number in range(forme_count - 1):
                            with open(os.path.join(folder_path, str(number + pointer).zfill(4) + '.bin'), 'r+b') as g:
                                g.seek(0x1C)
                                g.write(bytes(from_int_little_bytes(pointer, 2)))
                                print(f'{number + pointer}, Pokemon {bin_number}, forme {number + 1} set to have pointer {pointer}')

                    #write entire file to compilation
                    f.seek(0)
                    comp.write(f.read())


def update_master_bit():

    folder_path = askdirectory()

    for bin_number, file in enumerate(os.scandir(folder_path)):
        if file.is_file():  # Check if it's a file
            with open(file, "r+b") as f:
                f.seek(0x0D)
                value = f.read(1)

                new_value = from_little_bytes_int(value) | 1

                print(f'Wrote {new_value} over {value} in file {bin_number}')
                f.seek(0x0D)
                f.write(bytes(new_value.to_bytes(1, 'little')))

main()

#update_master_bit()
#fix_bins()