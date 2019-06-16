import openpyxl
import openpyxl.utils.cell as cell
import pandas as pd
import operator
import math

def format_results(results_dict):
    """
    dict -> str

    Returns a multiline string to represent the numeric results of a tally that was stored and passed to the function as a dictionary
    >>> format_results({'Mary Jane': 25, 'Alex Brown':52, 'John Smith':43})
    Mary Jane: 25
    Alex Brown: 52
    John Smith: 43
    """
    output=""
    for option in results_dict:
        output+="{}: {}".format(option, results_dict[option])+"\n"
    return output

def count_STV(ballots_table, details):
    """
    (file, boolean) -> str
    
    Takes an excel file formatted as a Google Form Multiple Choice Grid and \
    returns the winner per the Single Transferable Vote algorithm, as well as the details if requested.

    >>> count_STV("ballots.xlsx", False)
    John Smith is the winnner.

    >>> count_STV("ballots2.xlsx", True)
    John Smith is the winner.
    ##########
    COUNT 1 RESULTS:
    Mary Jane: 25
    Alex Brown: 52
    John Smith: 43
    
    * Mary Jane was eliminated
    ##########
    COUNT 2 RESULTS:
    Alex Brown: 59
    John Smith: 60
    Rejected (late): 1

    *John Smith is declared as the winner
    """
    # read excel file
    wb = openpyxl.load_workbook(ballots_table)
    ws = wb.active
    headings=[]
    options={}
    ### rename columns as needed for this particular file
    for col in range (2, ws.max_column+1): 
        value = ws[cell.get_column_letter(col)+str(1)].value
        name = value.split("[")[1:][0][:-1]
        if name!=None:
            headings+=[name]
            options.setdefault(name,0)

    # iterate through data, storing each ballot as a seperate dictionary entry
    ###### each dictionary entry should have a dictionary (ballot) as its value 
    ######### each of these dictionaries should be formatted with integer keys as the rank on the ballot, as long as the corresponding column was filled out
    ballots={}
    for row in range (2, ws.max_row + 1):
        uid=ws['A'+str(row)].value
        if uid!=None:
            ballots.setdefault(uid,{})
            for col in range (2, ws.max_column+1 ):
                rank=ws[cell.get_column_letter(col)+str(row)].value
                if col-2<len(headings) and rank!="NaN" and rank!=None:
                    ballots[uid][rank]=headings[col-2]

    rejected = { k : v for k,v in ballots.items() if not v} #tabulates any rejected ballots
    ballots = { k : v for k,v in ballots.items() if v}  #deletes any rejected ballots
    """
    # read excel file
    df = pd.read_excel(ballots_table)
    headings = df.columns.values.tolist()
    headings = [headings[0]]+[token.split("[")[1][:-1] for token in headings[1:]]
    df.columns = headings
    # iterate through data, storing each ballot as a seperate dictionary entry
    ballots={}
    for row in df.itertuples():
        email=row
        ballots.setdefault(email,{})
        for col in row[1:]:
            ballots[]=
    """        
    


    # loop through the ballots dictionary
    ######## iterate through the ballots dictionary, calculating/recalculating the sum
    ############### count the first place vote on each ballot and sum it in another dictionary with all the values called options
    ############### any time a ballot is encountered where the first place vote has been eliminated, iterate down the ballot until an option that has not been eliminated is available
    ############### if all options on the ballot have been eliminated, remove the ballot from the ballots dictionary and add it to the late_rejected_ballots dictionary
    ######## if the top option has over 50% of the eligible votes, declare it the winner and break from the loop
    ######## otherwise, pop out the minimum option and add it's key to the list eliminated. Continue looping through
    ######## if the ballots dictionary is empty and no winner has been declared, throw an exception
    winner_found = False
    ballot_count = 1
    detailed_results = ""
    eliminated = []
    late_rejected_ballots = {}
    while not winner_found and len(options)>=2:
        for uid in ballots:
            viable_ballot=False #actually we don't know at this stage
            position = 1
            while not viable_ballot:
                try:
                    choice = ballots[uid][position]
                except:
                    break
                if not (choice in eliminated):
                    options[choice] += 1
                    viable_ballot = True
                else:
                    position+=1
            if not viable_ballot:
                late_rejected_ballots.setdefault(uid, ballots.get(uid))
        for uid in late_rejected_ballots:
            try: 
                del ballots[uid]
            except: pass #print("could not remove " + str(uid))
                

        detailed_results += "\n##########\n" + "COUNT {} RESULTS:\n".format(ballot_count) + format_results(options)
        if ballot_count==1: detailed_results += "Rejected: " + str(len(rejected)) + "\n"
        late_rejects = len(late_rejected_ballots)
        if late_rejects >=1: detailed_results += "Late Rejected: " + str(late_rejects) + "\n"
            
        if max(options.items(), key=operator.itemgetter(1))[1] >= (math.ceil(len(ballots)/2)+1):
            winner_found = True
            winner = max(options.items(), key=operator.itemgetter(1))[0]
            detailed_results += "\n* {} is declared as the winner.\n".format(winner)
        else:
            to_eliminate = min(options.items(), key=operator.itemgetter(1))[0]
            eliminated += [to_eliminate]
            try:
                del options[to_eliminate]
            except: pass
            detailed_results += "\n* {} was eliminated.\n".format(to_eliminate)
            ballot_count += 1
            for key in options:
                options[key]=0

    if winner_found:
        if details:
            return winner + " is the winner.\n\n" + detailed_results
        return winner + " is the winner."
    else:
        return "ERROR: No winner found. \n" + detailed_results

if __name__ == "__main__":
    import os
    os.chdir("C:\\Users\\evank\\OneDrive\\Documents\\MyDevEnvironment\\My Python Projects\\Grad Clothing voting")
    print(count_STV("ballots_table.xlsx", True))

   