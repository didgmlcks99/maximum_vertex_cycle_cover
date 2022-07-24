import pandas as pd
import openpyxl
import math
import random

sheet1 = pd.read_excel("../data/un_data.xlsx", engine='openpyxl', sheet_name = 0)
sheet2 = pd.read_excel("../data/un_data.xlsx", engine='openpyxl', sheet_name = 1)

attr_1 = ["Position number", "Index #", "First name", "Last name", "Current position level", "s/m preference 1", "s/m preference 2", "s/m preference 3", "HM recommended", "HM recommended.1", "HM recommended.2", "HM recommended.3", "HM recommended.4", "Scoring system (total)", "Division"]
apply_data = sheet1[attr_1][:30]

attr_2 = ["Position number", "Duty Station", "Level"]
pos_data = sheet2[attr_2]

def validation(apply_data, attr_1, pos_data, attr_2):
    tot_error = 0
    tot_test = 0

    for idx, row in apply_data.iterrows():

        first_name = row[2]
        last_name = row[3]

        pref_cnt = 0

        cur_div = row[14]
        div_cnt = 0

        cur_lvl = row[4]
        lvl_cnt = 0
        
        cur_pos = int(row[0])
        same_pos_cnt = 0
        
        pref_pos_list = []
        same_pref_pos = 0

        for i in range(3):
            if not math.isnan(row[5+i]):

                pref_pos = int(row[5+i])
                pref_df = pos_data.loc[pos_data[attr_2[0]] == pref_pos]
                
                # 1. the staff member can choose minimum of 2 positions or 
                # maximum of 3 positions accoring to the decreasing order of their preference
                pref_cnt += 1

                for pref_idx, pref_row in pref_df.iterrows():

                    # 2. at least one of the preferred position must be geographical
                    #  mobility (different duty station from the current duty station)
                    pref_div = pref_row[1]

                    if pref_div != cur_div:
                        div_cnt += 1

                    # 3. the staff member can only apply to the same level position 
                    # (e.g. P-3 staff can only apply to P-3 positions only)
                    pref_lvl = pref_row[2]

                    if pref_lvl != cur_lvl:
                        lvl_cnt += 1
                
                # 4. the staff member cannot apply to one's own position
                if pref_pos == cur_pos:
                    same_pos_cnt += 1
                
                # 5. the staff member cannot apply to one position multiple times
                if pref_pos in pref_pos_list:
                    same_pref_pos = 1
                else:
                    pref_pos_list.append(pref_pos)


        tot_test += 1

        if pref_cnt < 2 or pref_cnt > 3:
            print("not vaild on condition 1: " + first_name + " " + last_name)
            print("detail: has " + str(pref_cnt) + "amount of preferred position")
            print("[ERROR] staff must choose minium of 2 positions or maximum of 3 positions.")

            tot_error += 1
        
        if div_cnt < 1:
            print("not vaild on condition 2: " + first_name + " " + last_name)
            print("detail: has " + str(div_cnt) + " " + "different divisions from preferred position")
            print("[ERROR] all preferred position must be the same division as current division.")

            tot_error += 1

        if lvl_cnt > 0:
            print("not vaild on condition 3: " + first_name + " " + last_name)
            print("detail: has " + str(lvl_cnt) + "different position level from current level")
            print("[ERROR] only the same position level can be applied.")

            tot_error += 1

        if same_pos_cnt > 1:
            print("not vaild on condition 4: " + first_name + " " + last_name)
            print("detail: has apply " + str(same_pos_cnt) + " " + "same position from current position")
            print("[ERROR] cannot apply to one own's position.")

            tot_error += 1
        
        if same_pref_pos == 1:
            print("not vaild on condition 5: " + first_name + " " + last_name)
            print("detail: has same preferred position multiple times.")
            print("[ERROR] cannot apply to one position multiple times.")

            tot_error += 1
    
    res = ((tot_test - tot_error) / tot_test)*100
    return res

def rand_match(apply_data, pos_data):
    
    num_pos = len(pos_data.index)
    matched = {}
    
    for idx, row in apply_data.iterrows():
        rand_pos = random.randint(0, num_pos-1)
        matched[int(row[1])] = pos_data[attr_2[0]][rand_pos]

    return matched

def fitess(rand_matched, apply_data):

    each_score = []
    
    for idx, row in apply_data.iterrows():
        
        score = 0
        each_id = int(row[1])

        for i in range(3):
            if not math.isnan(row[5+i]):
                match_pos = rand_matched[each_id]
                pref_pos = int(row[5+i])

                if match_pos == pref_pos:
                    if i == 0: score += 100
                    elif i == 1: score += 90
                    elif i == 2: score += 80
                else: score += 20
            
        score += int(row[13])
        each_score.append(score)
    
    return each_score


validation_result = validation(apply_data, attr_1, pos_data, attr_2)
print("\nvalidation percentage: " + "{:.2f}".format(validation_result) + "%")

rand_matched = rand_match(apply_data, pos_data)

every_score = fitess(rand_matched, apply_data)
total_score = sum(every_score)
print("score for each applicant: ", every_score)
print("fitness score: " + str(total_score))