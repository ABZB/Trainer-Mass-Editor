from encodings import utf_16_le, utf_8
from generic_garc_handling import *

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

nature_names = ['Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty', 'Bold', 'Docile', 'Relaxed', 'Impish', 'Lax', 'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive', 'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash', 'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky']

trainer_class_names = ['Pokemon Trainer - 1', 'Pokemon Trainer - 2', 'Youngster - 1', 'Lass - 1', 'Ace Trainer - 1', 'Ace Trainer - 2', 'Preschooler - 1', 'Preschooler - 2', 'Beauty', 'Swimmer - 1', 'Black Belt - 1', 'Scientist', 'Punk Guy - 1', 'Backpacker', 'Punk Girl - 1', 'Sightseer - 1', 'Sightseer - 2', 'Swimmer - 2', 'Veteran - 1', 'Veteran - 2', 'Rising Star - 1', 'Rising Star - 2', 'Madame', 'Gentleman', 'Hiker', 'Collector - 1', 'Pokemon Breeder - 1', 'Pokemon Breeder - 2', 'Team Skull - 1', 'Team Skull - 2', 'Pokemon Trainer - 3', 'Island Kahuna - 1', 'Office Worker - 1', 'Youth Athlete - 1', 'Youth Athlete - 2', 'Swimmer - 3', 'Office Worker - 2', 'Teacher', 'Captain - 1', 'Trial Guide - 1', 'Pokemon Trainer - 4', 'Pokemon Trainer - 5', 'Trial Guide - 2', 'Captain - 2', 'Captain - 3', 'Captain - 4', 'Captain - 5', 'Captain - 6', 'Captain - 7', 'Island Kahuna - 2', 'Island Kahuna - 3', 'Island Kahuna - 4', 'Police Officer', 'Dancer - 1', 'Cook', 'Bellhop - 1', 'Firefighter', 'Janitor', 'Worker', 'Fisherman', 'Golfer - 1', 'Golfer - 2', 'Preschooler - 3', 'Rising Star - 3', 'Ace Trainer - 3', 'Veteran - 3', 'Sightseer - 3', 'Swimmer - 4', 'Punk Guy - 2', 'Team Skull - 3', 'Team Skull - 4', 'Aether President - 1', 'Aether Branch Chief', 'Aether Foundation - 1', 'Aether Foundation - 2', 'Aether Foundation - 3', 'Team Skull Boss', 'Pokemon Trainer - 6', 'Team Skull Admin', 'Pokemon Trainer - 7', 'Elite Four - 1', 'Pokemon Trainer - 8', 'Aether President - 2', 'Pokemon Trainer - 9', 'Pokemon Trainer - 10', 'Pokemon Trainer - 11', 'Pokemon Trainer - 12', 'Pokemon Trainer - 13', 'Pokemon Trainer - 14', 'Pokemon Trainer - 15', 'Pokemon Trainer - 16', 'Pokemon Trainer - 17', 'Pro Wrestler', 'Pokemon Trainer - 18', 'Pokemon Center Lady', 'Aether Foundation - 4', 'Aether Foundation - 5', 'Pokemon Trainer - 19', 'Pokemon Trainer - 20', 'Pokemon Trainer - 21', 'Pokemon Trainer - 22', 'Pokemon Trainer - 23', 'Pokemon Trainer - 24', 'Pokemon Trainer - 25', 'Pokemon Trainer - 26', 'Pokemon Trainer - 27', 'Pokemon Trainer - 28', 'Elite Four - 2', 'Pokemon Trainer - 29', 'Elite Four - 3', 'Elite Four - 4', 'Pokemon Trainer - 30', 'Rising Star - 4', 'Ace Trainer - 4', 'Veteran - 4', 'Sightseer - 4', 'Swimmer - 5', 'Preschooler - 4', 'Black Belt - 2', 'Ace Trainer - 5', 'Ace Trainer - 6', 'Veteran - 5', 'Veteran - 6', 'Black Belt - 3', 'Collector - 2', 'Trial Guide - 3', 'Trial Guide - 4', 'Youngster - 2', 'Pokemon Trainer - 31', 'Principal', 'Flareon User', 'Espeon User', 'Leafeon User', 'Sylveon User', 'Eevee User', 'Umbreon User', 'Vaporeon User', 'Jolteon User', 'Glaceon User', 'GAME FREAK - 1', 'Pokemon Trainer - 32', 'Island Kahuna - 5', 'Captain - 8', 'Pokemon Trainer - 33', 'Punk Girl - 2', 'Youth Athlete - 3', 'Youth Athlete - 4', 'Swimmer - 6', 'Swimmer - 7', 'Golfer - 3', 'Pokemon Trainer - 34', 'Captain - 9', 'Captain - 10', 'Captain - 11', 'Pokemon Professor - 1', 'Ace Trainer - 7', 'Ace Trainer - 8', 'Rising Star - 5', 'Rising Star - 6', 'Youngster - 3', 'Lass - 2', 'Pokemon Breeder - 3', 'Aether Foundation - 6', 'Youngster - 4', 'Island Kahuna - 6', 'Pokemon Professor - 2', 'Pokemon Trainer - 35', 'Pokemon Trainer - 36', 'Pokemon Trainer - 37', 'Pokemon Trainer - 38', 'Pokemon Trainer - 39', 'Pokemon Trainer - 40', 'Twins', 'Rising Star Duo', 'Punk Pair', 'Karate Family', 'Swimmers', 'Ace Duo', 'Honeymooners', 'Veteran Duo', 'Athletic Siblings', 'Swimmer Girls', 'Golf Buddies', 'Battle Legend - 1', 'Battle Legend - 2', 'Aether Foundation - 7', 'Pokemon Trainer - 41', 'Pokemon Trainer - 42', 'Pokemon Trainer - 43', 'Pokemon Trainer - 44', 'Pokemon Trainer - 45', 'Elite Four - 5', 'Ultra Recon Squad - 1', 'Ultra Recon Squad - 2', 'Pokemon Trainer - 46', 'Surfer', 'Actor', 'Reporter', 'Team Aqua', 'Team Galactic', 'Team Magma', 'Team Plasma', 'Team Flare', 'Kantonian Gym - 1', 'Kantonian Gym - 2', 'GAME FREAK - 2', 'Team Rainbow Rocket - 1', 'Pokemon Trainer - 47', 'Team Rainbow Rocket - 2', 'Team Rainbow Rocket - 3', 'Ultra Forest', 'Master & Apprentice', 'Dancing Family', 'Capoeira Couple', 'Tourist Couple', 'Sparring Partners', 'Office Worker - 3', 'Dancer - 2', 'Bellhop - 2', 'Pokemon Trainer - 48', 'Aether President - 3', 'Pokemon Trainer - 49', 'Pokemon Trainer - 50']

def print_regular_trainer_csv(working_data):
    pass

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
            if(forme_count > 1 and absolute_index >= pointer and pointer != 0):

                #forme index
                temp[0xE] = absolute_index - pointer + 1

                #search for base Pokemon
                for y, entry in enumerate(working_data.personal_binary):
                    if(from_little_bytes_int(entry[0x1C:0x1E]) == pointer and y < pointer):
                        temp[0:2] = y.to_bytes(2, 'little')
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
            action_choice = input('Extract or rebuild GARC, or quit? (e/r/q)\n').lower()
            if(action_choice in {'e', 'r', 'q'}):
                break
            else:
                print(action_choice, 'is not valid\\nn')

        while action_choice != 'q':
            target_choice = input('Regular Trainers, Battle Tree, or Battle Royale? (r/t/e)\n').lower()
            if(target_choice in {'r', 't', 'e', 'q'}):
                break
            else:
                print(target_choice, 'is not valid\\nn')

        target_name = 'Battle Tree' if target_choice == 't' else 'Battle Royale' if target_choice == 'e' else 'Regular Trainers'

        


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
            case 'e':
                export_from_GARC(working_data, target_name)
            case 'r':
                import_to_GARC(working_data, target_name)
            case 'q':
                return

main()