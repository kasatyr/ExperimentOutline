import random
import pandas as pd

class trial_mapping():

    chunk_size=6
    locationCoordinates = {
        '1': ('0.0, 0.6'),
        '2': ('0.4, 0.2'),
        '3': ('0.4, -0.2'),
        '4': ('0.0, -0.6'),
        '5': ('-0.4, -0.2'),
        '6': ('-0.4, 0.2')
    }
    
    def __init__(self, word_path, image_path, cond, image_categories, block_i):
        self.word_path = word_path
        self.image_path = image_path
        self.cond = cond
        self.image_categories = image_categories
        self.block_i = block_i
        self.image_dict = {}

    def load_word_list(self): #maybe attach this to the loop and load from there?
        self.word_list = pd.read_excel(self.word_path)
        self.raw_word_list = self.word_list['WORD'].tolist()  # Convert the 'images' column to a list

        # - random subset of 315 words
        self.subset_words = random.sample(self.raw_word_list, 315)

        self.ss3_word_list =  self.subset_words[:63]
        self.ss6_word_list =  self.subset_words[63:189]  # next 126 words
        self.tbrf_word_list =  self.subset_words[189:]  # last 126 words

        if self.block_i == 1:
            self.cur_ss3_word_list = self.ss3_word_list[:len(self.ss3_word_list) // 3]
            self.cur_ss6_word_list = self.ss6_word_list[:len(self.ss6_word_list) // 3]
            self.cur_tbrf_word_list = self.tbrf_word_list[:len(self.tbrf_word_list) // 3]
        
        elif self.block_i == 2:
            self.cur_ss3_word_list = self.ss3_word_list[21:42]
            self.cur_ss6_word_list = self.ss6_word_list[42:84]
            self.cur_tbrf_word_list = self.tbrf_word_list[42:84]

        else: 
            self.cur_ss3_word_list = self.ss3_word_list[42:63]
            self.cur_ss6_word_list = self.ss6_word_list[84:126]
            self.cur_tbrf_word_list = self.tbrf_word_list[84:126]

    def load_image_list(self): #maybe attach this to the loop and load from there?
        self.image_list = pd.read_excel(self.image_path)
        self.image_cat = ['mountains', 'beaches', 'forests']
        self.image_per_cat = 6

        for cat in self.image_cat:
            self.image_subset = self.image_list[self.image_list['category'].isin([cat])]['images']
            self.image_dict[cat] = random.sample(list(self.image_subset), min(self.image_per_cat, len(self.image_subset)))

        start_idx = (self.block_i - 1) * self.image_per_cat
        end_idx = start_idx + self.image_per_cat

        self.cur_mountain_image_list = self.image_dict['mountains'][start_idx:end_idx]
        self.cur_beach_image_list = self.image_dict['beaches'][start_idx:end_idx]  
        self.cur_forest_image_list = self.image_dict['forests'][start_idx:end_idx]

    
    def define_target_loc(self):

        test_loc = list(range(6))
        random.shuffle(test_loc)
        
        location = [['0.0, 0.6'], ['0.4, 0.2'],
                    ['0.4, -0.2'], ['0.0, -0.6'],
                    ['-0.4, -0.2'], ['-0.4, 0.2']]
        
        self.cond = ['ss3', 'ss6', 'tbrf']
        self.loc = {}

        # Helper function to populate temp with match/mismatch
        def populate_temp(a_match, a_mismatch, b_match, b_mismatch):
            for condition in self.cond:  # Loop through each condition in cond list
                self.loc[condition] = []
                if condition in ['ss3', 'ss6']:  # Apply this block for 'ss3' and 'ss6'
                    for i in range(len(test_loc)):  # Creates for 6 trials in total
                        line = [a_match[i], a_mismatch[i], [num for num in test_loc if num not in [a_match[i], a_mismatch[i]]]]
                        self.loc[condition].append(line)  # Append remaining numbers individually
                else:
                    for i in range(len(test_loc)):  # Creates for 6 trials in total
                        line = [b_match[i], b_mismatch[i], [num for num in test_loc if num not in [b_match[i], b_mismatch[i]]]]
                        self.loc[condition].append(line)  

        # For blocks 1 and 3:
        if self.block_i in [1, 3]:
            self.block_match = test_loc[:self.chunk_size // 2]
            self.a_match = self.block_match
            self.b_mismatch = self.block_match

            self.block_mismatch = test_loc[self.chunk_size // 2:]
            self.a_mismatch = self.block_mismatch
            self.b_match = self.block_mismatch

            populate_temp(self.a_match, self.a_mismatch, self.b_match, self.b_mismatch)

        else:
            self.block_match = self.test_loc[self.chunk_size // 2:]
            self.a_match = self.block_match
            self.b_mismatch = self.block_match

            self.block_mismatch = self.test_loc[:self.chunk_size // 2]
            self.a_mismatch = self.block_mismatch
            self.b_match = self.block_mismatch

            populate_temp(self.a_match, self.a_mismatch, self.b_match, self.b_mismatch)
    

    def imageCond_word(self, condition, word_vec, n_real_words):
        for i in range(len(self.image_list)):
            vector = list(zip(loc_compiled[condition], word_vec)) 
            chunks = [vector[i:i + n_real_words] for i in range(0, len(vector), n_real_words)]
            
            self.block_match

            if n_real_words < self.chunk_size:
                # fill the rest of them with xxx
                pass
            elif n_real_words == self.chunk_size:
                chunk_dict = {self.image_list[i]: chunk for i, chunk in enumerate(chunks[:len(self.image_list)])}
            else:
                raise Exception(f"n_real_words: {n_real_words} does not match chunk_size: {self.chunk_size}")
            self.chunk_dict = chunk_dict

    def run_trial(self, trial_i):
        return picture_path, word_sequence, target_index, foil_indices


