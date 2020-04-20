import numpy as np
import pandas as pd
import json 


df = pd.read_csv("attribution_allocation_student_data.csv")
df = df.fillna('none')
df_channel = pd.read_csv("channel_spend_student_data.csv")
df_channel = df_channel.drop(3)


newdf = list()
for i in range(len(df_channel)):
    temp = json.loads(df_channel['spend by channel'][i].replace("\'", "\""))
    temp['tier'] = (i+1)
    newdf.append(temp)

df_channel = pd.DataFrame(newdf)




df1 = pd.merge(df, df_channel,how='left', on='tier')

# This function takes a list of entry, each element is a tuple shaped like (channel,count,cost)
# And prints out count, cost, and CAC
#@param: list_of_entry: list of tuples shaped like (channel,count,cost)
#@return: output_user, output_cost, CAC
def get_CAC(list_of_entry):
    output_user = dict()
    output_cost = dict()
    CAC = dict()
    for i in list_of_entry:
        if i[0] == None:
            continue
        for j in range(len(i[0])):
            channel = i[0][j]
            if channel not in output_user.keys():
                output_user[channel] = i[1][j]
                output_cost[channel] = i[2][j] 
            else:
                output_user[channel] += i[1][j]
                output_cost[channel] += i[2][j] 
                
    for i in output_user.keys():
        if output_user[i] != None:
            CAC[i]=(output_cost[i]/output_user[i])
        print(i,'count',output_user[i],'cost',output_cost[i],'CAC',(output_cost[i]/output_user[i]),sep = ': ')
    return output_user, output_cost, CAC


# ## Last interaction



# This function takes a row accessed by dataframe's iloc, and returns the last contact
#@param: entry: a single entry of the dataframe. Must be a return value from the iloc function
#@return: a tuple. the last contact. None if not applicable. second attribute is count, and another attribute is cost
def find_last_contact(entry):
    if entry['convert_TF']:
        if entry['touch_5'] == 'none':
            if entry['touch_4'] == 'none':
                if entry['touch_3'] == 'none':
                    if entry['touch_2'] == 'none':
                        if entry['touch_1'] == 'none':
                            return None,[0],[0]
                        else:
                            list_channel = list()
                            list_number = list()
                            list_channel.append(entry['touch_1'])
                            list_number.append(1)
                            return list_channel,list_number,[entry[entry['touch_1']]]
                    else:
                        list_channel = list()
                        list_number = list()
                        list_channel.append(entry['touch_2'])
                        list_channel.append(entry['touch_1'])
                        list_number.append(1)
                        list_number.append(0)
                        cost = [entry[entry['touch_2']],entry[entry['touch_1']]]
                        return list_channel,list_number,cost
                else:
                    list_channel = list()
                    list_number = list()
                    list_channel.append(entry['touch_3'])
                    list_channel.append(entry['touch_2'])
                    list_channel.append(entry['touch_1'])
                    list_number.append(1)
                    list_number.append(0)
                    list_number.append(0)
                    cost = [entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                    return list_channel,list_number,cost
            else:
                list_channel = list()
                list_number = list()
                list_channel.append(entry['touch_4'])
                list_channel.append(entry['touch_3'])
                list_channel.append(entry['touch_2'])
                list_channel.append(entry['touch_1'])
                list_number.append(1)
                list_number.append(0)
                list_number.append(0)
                list_number.append(0)
                cost = [entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                return list_channel,list_number,cost
        else:
            list_channel = list()
            list_number = list()
            list_channel.append(entry['touch_5'])
            list_channel.append(entry['touch_4'])
            list_channel.append(entry['touch_3'])
            list_channel.append(entry['touch_2'])
            list_channel.append(entry['touch_1'])
            list_number.append(1)
            list_number.append(0)
            list_number.append(0)
            list_number.append(0)
            list_number.append(0)
            cost = [entry[entry['touch_5']],entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
            return list_channel,list_number,cost
    else:
        return None,[0],[0]



list_of_entry_last_user = list()
list_of_entry_last = list()
for i in range(len(df)):
    entry = df1.iloc[i,:]
    list_of_entry_last.append(find_last_contact(entry))


output_user, output_cost, CAC = get_CAC(list_of_entry_last)


# ## Position based



# This function takes a row accessed by dataframe's iloc, and returns the position-based cost
#@param: entry: a single entry of the dataframe. Must be a return value from the iloc function
#@return: a tuple. the position_based contact. None if not applicable. And another attribute is cost
def find_position_based(entry):
    if entry['convert_TF']:
        if entry['touch_5'] == 'none':
            if entry['touch_4'] == 'none':
                if entry['touch_3'] == 'none':
                    if entry['touch_2'] == 'none':
                        if entry['touch_1'] == 'none':
                            return None,[0],[0]
                        else:
                            list_channel = list()
                            list_number = list()
                            list_channel.append(entry['touch_1'])
                            list_number.append(1)
                            return list_channel,list_number,[entry[entry['touch_1']]]
                    else:
                        list_channel = list()
                        list_number = list()
                        list_channel.append(entry['touch_2'])
                        list_channel.append(entry['touch_1'])
                        list_number.append(0.5)
                        list_number.append(0.5)
                        cost = [entry[entry['touch_2']],entry[entry['touch_1']]]
                        return list_channel,list_number,cost
                else:
                    list_channel = list()
                    list_number = list()
                    list_channel.append(entry['touch_3'])
                    list_channel.append(entry['touch_2'])
                    list_channel.append(entry['touch_1'])
                    list_number.append(0.4)
                    list_number.append(0.2)
                    list_number.append(0.4)
                    cost = [entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                    return list_channel,list_number,cost
            else:
                list_channel = list()
                list_number = list()
                list_channel.append(entry['touch_4'])
                list_channel.append(entry['touch_3'])
                list_channel.append(entry['touch_2'])
                list_channel.append(entry['touch_1'])
                list_number.append(0.4)
                list_number.append(0.1)
                list_number.append(0.1)
                list_number.append(0.4)
                cost = [entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                return list_channel,list_number,cost
        else:
            list_channel = list()
            list_number = list()
            list_channel.append(entry['touch_5'])
            list_channel.append(entry['touch_4'])
            list_channel.append(entry['touch_3'])
            list_channel.append(entry['touch_2'])
            list_channel.append(entry['touch_1'])
            list_number.append(0.4)
            list_number.append(0.066)
            list_number.append(0.066)
            list_number.append(0.066)
            list_number.append(0.4)
            cost = [entry[entry['touch_5']],entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
            return list_channel,list_number,cost
    else:
        return None,[0],[0]




list_of_entry_position_based = list()
for i in range(len(df)):
    entry = df1.iloc[i,:]
    list_of_entry_position_based.append(find_position_based(entry))





output_user, output_cost, CAC = get_CAC(list_of_entry_position_based)


# ## Linear Method



# This function takes a row accessed by dataframe's iloc, and returns the linear cost
#@param: entry: a single entry of the dataframe. Must be a return value from the iloc function
#@return: a tuple. the position_based contact. None if not applicable. And another attribute is cost
def find_linear(entry):
    if entry['convert_TF']:
        if entry['touch_5'] == 'none':
            if entry['touch_4'] == 'none':
                if entry['touch_3'] == 'none':
                    if entry['touch_2'] == 'none':
                        if entry['touch_1'] == 'none':
                            return None,[0],[0]
                        else:
                            list_channel = list()
                            list_number = list()
                            list_channel.append(entry['touch_1'])
                            list_number.append(1)
                            return list_channel,list_number,[entry[entry['touch_1']]]
                    else:
                        list_channel = list()
                        list_number = list()
                        list_channel.append(entry['touch_2'])
                        list_channel.append(entry['touch_1'])
                        list_number.append(0.5)
                        list_number.append(0.5)
                        cost = [entry[entry['touch_2']],entry[entry['touch_1']]]
                        return list_channel,list_number,cost
                else:
                    list_channel = list()
                    list_number = list()
                    list_channel.append(entry['touch_3'])
                    list_channel.append(entry['touch_2'])
                    list_channel.append(entry['touch_1'])
                    list_number.append(0.33)
                    list_number.append(0.33)
                    list_number.append(0.33)
                    cost = [entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                    return list_channel,list_number,cost
            else:
                list_channel = list()
                list_number = list()
                list_channel.append(entry['touch_4'])
                list_channel.append(entry['touch_3'])
                list_channel.append(entry['touch_2'])
                list_channel.append(entry['touch_1'])
                list_number.append(0.25)
                list_number.append(0.25)
                list_number.append(0.25)
                list_number.append(0.25)
                cost = [entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                return list_channel,list_number,cost
        else:
            list_channel = list()
            list_number = list()
            list_channel.append(entry['touch_5'])
            list_channel.append(entry['touch_4'])
            list_channel.append(entry['touch_3'])
            list_channel.append(entry['touch_2'])
            list_channel.append(entry['touch_1'])
            list_number.append(0.2)
            list_number.append(0.2)
            list_number.append(0.2)
            list_number.append(0.2)
            list_number.append(0.2)
            cost = [entry[entry['touch_5']],entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
            return list_channel,list_number,cost
    else:
        return None,[0],[0]




list_of_entry_linear = list()
for i in range(len(df)):
    entry = df1.iloc[i,:]
    list_of_entry_linear.append(find_linear(entry))



output_user, output_cost, CAC = get_CAC(list_of_entry_linear)


# ## Time Decay



# This function takes a row accessed by dataframe's iloc, and returns the time-decay cost
#@param: entry: a single entry of the dataframe. Must be a return value from the iloc function
#@return: a tuple. the position_based contact. None if not applicable. And another attribute is cost
def find_decay(entry):
    if entry['convert_TF']:
        if entry['touch_5'] == 'none':
            if entry['touch_4'] == 'none':
                if entry['touch_3'] == 'none':
                    if entry['touch_2'] == 'none':
                        if entry['touch_1'] == 'none':
                            return None,[0],[0]
                        else:
                            list_channel = list()
                            list_number = list()
                            list_channel.append(entry['touch_1'])
                            list_number.append(1)
                            return list_channel,list_number,[entry[entry['touch_1']]]
                    else:
                        list_channel = list()
                        list_number = list()
                        list_channel.append(entry['touch_2'])
                        list_channel.append(entry['touch_1'])
                        list_number.append(0.4)
                        list_number.append(0.6)
                        cost = [entry[entry['touch_2']],entry[entry['touch_1']]]
                        return list_channel,list_number,cost
                else:
                    list_channel = list()
                    list_number = list()
                    list_channel.append(entry['touch_3'])
                    list_channel.append(entry['touch_2'])
                    list_channel.append(entry['touch_1'])
                    list_number.append(0.2)
                    list_number.append(0.3)
                    list_number.append(0.5)
                    cost = [entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                    return list_channel,list_number,cost
            else:
                list_channel = list()
                list_number = list()
                list_channel.append(entry['touch_4'])
                list_channel.append(entry['touch_3'])
                list_channel.append(entry['touch_2'])
                list_channel.append(entry['touch_1'])
                list_number.append(0.1)
                list_number.append(0.2)
                list_number.append(0.3)
                list_number.append(0.4)
                cost = [entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
                return list_channel,list_number,cost
        else:
            list_channel = list()
            list_number = list()
            list_channel.append(entry['touch_5'])
            list_channel.append(entry['touch_4'])
            list_channel.append(entry['touch_3'])
            list_channel.append(entry['touch_2'])
            list_channel.append(entry['touch_1'])
            list_number.append(0.045)
            list_number.append(0.08)
            list_number.append(0.125)
            list_number.append(0.25)
            list_number.append(0.5)
            cost = [entry[entry['touch_5']],entry[entry['touch_4']],entry[entry['touch_3']],entry[entry['touch_2']],entry[entry['touch_1']]]
            return list_channel,list_number,cost
    else:
        return None,[0],[0]



list_of_entry_decay = list()
for i in range(len(df)):
    entry = df1.iloc[i,:]
    list_of_entry_decay.append(find_decay(entry))



output_user, output_cost, CAC = get_CAC(list_of_entry_decay)











#Seperate the dataset into 3 tiers

df1_tier1 = df1.loc[df1['tier'] == 1]
df1_tier2 = df1.loc[df1['tier'] == 2]
df1_tier3 = df1.loc[df1['tier'] == 3]


# Tier 1


list_of_entry_position_based = list()
for i in range(len(df1_tier1)):
    entry = df1_tier1.iloc[i,:]
    list_of_entry_position_based.append(find_position_based(entry))
output_user_tier1, output_cost_tier1, CAC_tier1 = get_CAC(list_of_entry_position_based)


# Tier 2


list_of_entry_position_based = list()
for i in range(len(df1_tier2)):
    entry = df1_tier2.iloc[i,:]
    list_of_entry_position_based.append(find_position_based(entry))
output_user_tier2, output_cost_tier2, CAC_tier2 = get_CAC(list_of_entry_position_based)


# Tier 3


list_of_entry_position_based = list()
for i in range(len(df1_tier3)):
    entry = df1_tier3.iloc[i,:]
    list_of_entry_position_based.append(find_position_based(entry))
output_user_tier3, output_cost_tier3, CAC_tier3 = get_CAC(list_of_entry_position_based)



for i in CAC_tier1.keys():
    marginal_2_1 = CAC_tier2[i] - CAC_tier1[i]
    marginal_3_2 = CAC_tier3[i] - CAC_tier2[i]
    print(i)
    print('marginal_2_1 ',marginal_2_1 ,sep = ': ')
    print('marginal_3_2 ',marginal_3_2 ,sep = ': ')
