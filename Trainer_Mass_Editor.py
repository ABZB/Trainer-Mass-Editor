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

trainer_class_names = ['Pokemon Trainer', 'Pokemon Trainer', 'Youngster', 'Lass', 'Ace Trainer', 'Ace Trainer', 'Preschooler', 'Preschooler', 'Beauty', 'Swimmer', 'Black Belt', 'Scientist', 'Punk Guy', 'Backpacker', 'Punk Girl', 'Sightseer', 'Sightseer', 'Swimmer', 'Veteran', 'Veteran', 'Rising Star', 'Rising Star', 'Madame', 'Gentleman', 'Hiker', 'Collector', 'Pokemon Breeder', 'Pokemon Breeder', 'Team Skull', 'Team Skull', 'Pokemon Trainer', 'Island Kahuna', 'Office Worker', 'Youth Athlete', 'Youth Athlete', 'Swimmer', 'Office Worker', 'Teacher', 'Captain', 'Trial Guide', 'Pokemon Trainer', 'Pokemon Trainer', 'Trial Guide', 'Captain', 'Captain', 'Captain', 'Captain', 'Captain', 'Captain', 'Island Kahuna', 'Island Kahuna', 'Island Kahuna', 'Police Officer', 'Dancer', 'Cook', 'Bellhop', 'Firefighter', 'Janitor', 'Worker', 'Fisherman', 'Golfer', 'Golfer', 'Preschooler', 'Rising Star', 'Ace Trainer', 'Veteran', 'Sightseer', 'Swimmer', 'Punk Guy', 'Team Skull', 'Team Skull', 'Aether President', 'Aether Branch Chief', 'Aether Foundation', 'Aether Foundation', 'Aether Foundation', 'Team Skull Boss', 'Pokemon Trainer', 'Team Skull Admin', 'Pokemon Trainer', 'Elite Four', 'Pokemon Trainer', 'Aether President', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pro Wrestler', 'Pokemon Trainer', 'Pokemon Center Lady', 'Aether Foundation', 'Aether Foundation', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Elite Four', 'Pokemon Trainer', 'Elite Four', 'Elite Four', 'Pokemon Trainer', 'Rising Star', 'Ace Trainer', 'Veteran', 'Sightseer', 'Swimmer', 'Preschooler', 'Black Belt', 'Ace Trainer', 'Ace Trainer', 'Veteran', 'Veteran', 'Black Belt', 'Collector', 'Trial Guide', 'Trial Guide', 'Youngster', 'Pokemon Trainer', 'Principal', 'Flareon User', 'Espeon User', 'Leafeon User', 'Sylveon User', 'Eevee User', 'Umbreon User', 'Vaporeon User', 'Jolteon User', 'Glaceon User', 'GAME FREAK', 'Pokemon Trainer', 'Island Kahuna', 'Captain', 'Pokemon Trainer', 'Punk Girl', 'Youth Athlete', 'Youth Athlete', 'Swimmer', 'Swimmer', 'Golfer', 'Pokemon Trainer', 'Captain', 'Captain', 'Captain', 'Pokemon Professor', 'Ace Trainer', 'Ace Trainer', 'Rising Star', 'Rising Star', 'Youngster', 'Lass', 'Pokemon Breeder', 'Aether Foundation', 'Youngster', 'Island Kahuna', 'Pokemon Professor', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Twins', 'Rising Star Duo', 'Punk Pair', 'Karate Family', 'Swimmers', 'Ace Duo', 'Honeymooners', 'Veteran Duo', 'Athletic Siblings', 'Swimmer Girls', 'Golf Buddies', 'Battle Legend', 'Battle Legend', 'Aether Foundation', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Pokemon Trainer', 'Elite Four', 'Ultra Recon Squad', 'Ultra Recon Squad', 'Pokemon Trainer', 'Surfer', 'Actor', 'Reporter', 'Team Aqua', 'Team Galactic', 'Team Magma', 'Team Plasma', 'Team Flare', 'Kantonian Gym', 'Kantonian Gym', 'GAME FREAK', 'Team Rainbow Rocket', 'Pokemon Trainer', 'Team Rainbow Rocket', 'Team Rainbow Rocket', 'Ultra Forest', 'Master & Apprentice', 'Dancing Family', 'Capoeira Couple', 'Tourist Couple', 'Sparring Partners', 'Office Worker', 'Dancer', 'Bellhop', 'Pokemon Trainer', 'Aether President', 'Pokemon Trainer', 'Pokemon Trainer']

def print_regular_trainer_csv(working_data):
    pass

def print_facility_trainer_csv(working_data, target_name):
    temp = []

    #write Pokemon
    with open(asksaveasfilename(title='Save Table of Facility Pokemon', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
        writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')

        #write header row
        writer_head.writerow(['Index', 'Pokemon Name', 'Forme', 'Move 1', 'Move 2', 'Move 3', 'Move 4', 'Perfect IVs', 'Nature', 'Item'])

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
                if (iv_byte ^ (1 >> x) == (1 >> x)):
                    ivs += (' | ' if len(ivs) > 0 else '') + iv_names[x]

            #write row
            writer_head.writerow([
                count, 
                working_data.pokemon_name_list[pokemon_index][1], 
                '' if forme_number == 0 else working_data.pokemon_name_list[forme_number][1], 
                *(working_data.move_name_list[from_little_bytes_int(entry[2 + 2*x: 4 + 2*x])][1] for x in range(4)), 
                ivs,
                nature_names[entry[0xD]],
                working_data.item_name_list[from_little_bytes_int(entry[0xC:0xE])]][1])

            temp.append(str(working_data.pokemon_name_list[pokemon_index]) + '' if forme_number == 0 else working_data.pokemon_name_list[forme_number])

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
            #append mystery value
            trainer_temp.append(from_little_bytes_int(entry[0x2:0x4]))

            #iterate over the rest of the pairs of bytes
            entry_count = (len(entry) - 4)//2

            max_poke_count = max(max_poke_count, entry_count)

            for x in range(entry_count):
                index = from_little_bytes_int(entry[0x4 + 2*x: 0x6 + 2*x])
                trainer_temp.append(str(x) + str(temp[index]))

            trainer_output.append(trainer_temp)



            
        #write header row
        writer_head.writerow(['Index', 
                              'Trainer Name', 
                              'Trainer Class', 
                              'Mystery Value', 
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

        
        working_data.trainer_name_list_royale = load_text_from_csv(os.path.join(temp[0], working_data.trainer_name_list_royale[0]), working_data.trainer_name_list_royale)
        working_data.trainer_name_list_tree = load_text_from_csv(os.path.join(temp[0], working_data.trainer_name_list_tree[0]), working_data.trainer_name_list_tree)
        working_data.trainer_name_list_world = load_text_from_csv(os.path.join(temp[0], working_data.trainer_name_list_world[0]), working_data.trainer_name_list_world)
        working_data.ability_name_list = load_text_from_csv(os.path.join(temp[0], working_data.ability_name_list[0]), working_data.ability_name_list)
        working_data.item_name_list = load_text_from_csv(os.path.join(temp[0], working_data.item_name_list[0]), working_data.item_name_list)
        working_data.pokemon_name_list = load_text_from_csv(os.path.join(temp[0], working_data.pokemon_name_list[0]), working_data.pokemon_name_list)
        working_data.move_name_list = load_text_from_csv(os.path.join(temp[0], working_data.move_name_list[0]), working_data.move_name_list)

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