################################################################################
# 6.0002 Fall 2019
# Problem Set 1
# Written By: yunb, mkebede
# Name: Deniz Sert
# Collaborators: Soomin Chun
# Time: 5 hrs


# Problem 1
class State():
    """
    A class representing the election results for a given state. 
    Assumes there are no ties between dem and gop votes. The party with a 
    majority of votes receives all the Electoral College (EC) votes for 
    the given state.
    """

    def __init__(self, name, dem, gop, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        gop - number of Republican votes cast
        ec - number of EC votes a state has 

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.winner - str, the winner of the state, "dem" or "gop"
        self.margin - int, difference in votes cast between the two parties, a positive number
        self.ec - int, number of EC votes a state has
        """
        self.name = name
        self.winner = 'dem' if int(dem)>int(gop) else 'gop'
        self.margin = abs(int(dem)-int(gop))
        self.ec = int(ec)
#        self.dem = int(dem)
#        self.gop = int(gop)
#      
#    def get_dem_votes(self):
#        return self.dem
#    def get_gop_votes(self):
#        return self.gop

    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state  
        """
        return self.name

    def get_num_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has 
        """
        return self.ec

    def get_margin(self):
        """
        Returns: 
        int, difference in votes cast between the two parties, a positive number
        """
        return self.margin

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "gop"
        """
        return self.winner

    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """
        return "In " + self.name + ", " + str(self.ec) + " EC votes were won by " + self.winner + " by a " + str(self.margin) + " vote margin."

    def __eq__(self, other):
        """
        Determines if two State instances are the same.
        They are the same if they have the same state name, winner, margin and ec votes.
        Be sure to check for instance type equality as well! 

        Note: 
        1. Allows you to check if State_1 == State_2
                2. Make sure to check for instance type (Hint: look up isinstance())

        Param:
        other - State object to compare against  

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        if isinstance(other, State):
            if self.get_name() == other.get_name():
                if self.get_winner() == other.get_winner():
                    if self.get_margin() == other.get_margin():
                        if self.get_num_ecvotes() == other.get_num_ecvotes():
                            return True
        return False
    
        

#func(*tup)
#the * unpacks the tuple!!
        
        
        
# Problem 2
def load_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    states = []
    #with loop will automatically close file
    with open(filename) as f:
        read_data = f.readlines()[1:]
    for line in read_data:
        
        tup = tuple(line.split())
        s = State(*tup)
        states.append(s)
    
    
    return states


# Problem 3
def find_winner(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances 

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    dem = 0
    gop = 0
    for state in election:
        if state.get_winner() == "dem":
            dem+=state.get_num_ecvotes()
        else:
            gop+=state.get_num_ecvotes()
    return ('dem', 'gop') if dem>gop else ('gop', 'dem')
#    if dem>gop:
#        return ('dem', 'gop')
#    else:
#        return ('gop', 'dem')


def get_winner_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances won by the winning candidate
    """
    states_won = []
    for state in election:
        if state.get_winner() == find_winner(election)[0]:
            states_won.append(state)
    return states_won


def ec_votes_reqd(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    lost_ec_votes = 0
    for state in get_winner_states(election):
        lost_ec_votes+=state.get_num_ecvotes()
    return abs(lost_ec_votes-(total//2-1))


# Problem 4
def greedy_election(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. First chooses the states with the smallest 
    win margin, i.e. state that was won by the smallest difference in number of voters. 
    Continues to choose other states up until it meets or exceeds the ec_votes_needed. 
    Should only return states that were originally won by the winner in the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    
    #finds the best choice at a single stage, but it doesn't mean it's the overall best choice
    states_copy = list(sorted(winner_states, key = lambda state: state.get_margin()))
    list_of_states = []
    total_votes = 0
    #adds states to the list of states (knapsack) until we don't need any more ec_votes
    for i in range(len(states_copy)):
        list_of_states.append(states_copy[i])
        total_votes+=states_copy[i].get_num_ecvotes()
        if (total_votes) >= ec_votes_needed:
            break
    return list_of_states

#helper function for #5: from lecture
def fastMaxVal(toConsider, avail, memo = None):
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    #memoization
    if memo == None:
        memo = {}
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].get_num_ecvotes() > avail:
        #Explore right branch only
        result = fastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake =\
                 fastMaxVal(toConsider[1:],
                            avail - nextItem.get_num_ecvotes(), memo)
        withVal += nextItem.get_margin()
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                                avail, memo)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result
# Problem 5
def dp_move_max_voters(winner_states, ec_votes, memo=None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. 

    Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

        Hint: If using a top-down implementation, it may be helpful to create a helper function

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, number of EC votes (relocation should result in gain of AT MOST ec_votes)
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    The empty list, if every state has a # EC votes greater than ec_votes
    """
    #see above function
    return fastMaxVal(winner_states, ec_votes)[1]
    
#    list_of_states = []
#    #right branch = withoutVal
#    #left branch = withToTake
#    left_branch_num = 0
#    right_branch_num = 0
#    
#    if memo == None:
#        memo = {}
#    if winner_states == [] or ec_votes == 0:
#        list_of_states = []
#    elif winner_states[0].get_num_ecvotes() > ec_votes:
#        #explore right branch only
#        list_of_states = dp_move_max_voters(winner_states[1:], ec_votes, memo)
#    else:
#        nextState = winner_states[0]
#        #expore left branch
#        left_branch = dp_move_max_voters(winner_states[1:], ec_votes - nextState.get_num_ecvotes(), memo)
#        
#        #explore right branch
#        right_branch = dp_move_max_voters(winner_states[1:], ec_votes, memo)
#
#        for state in left_branch:
##            withoutVal_num += state.get_margin()
#            print(state)
#        for state in right_branch:
#            print(state)
##            withVal_num += state.get_margin()
#            
#        #choose better branch
#        if right_branch_num > left_branch_num:
#            list_of_states.append(right_branch)
#        else:
#            list_of_states.append(left_branch)
#            
#    memo[(len(winner_states), ec_votes)] = list_of_states
#    return list_of_states
    
    
    
    
    
    
#    list_of_states = []
#    if winner_states == [] or ec_votes == 0:
#        list_of_states = 0
#    elif winner_states[0].get_num_ecvotes() > ec_votes: #cannot afford current item
#        #Explore right branch only
#        list_of_states = dp_move_max_voters(winner_states[1:], ec_votes)
#    else:
#        nextState = winner_states[0]
#        #explore left branch
#        withVal, withToTake = dp_move_max_voters(winner_states[1:], ec_votes-nextState.get_num_ecvotes())
#        withVaL += nextState.get_num_ecvotes()
#        #explore right branch
#        withoutVal, withoutToTake = dp_move_max_voters(winner_states[1:], ec_votes)
#        #Choose better branch
#        if withVal > withoutVal:
#            list_of_states = (withVal, withToTake + (nextState,))
#        else:
#            list_of_states = (withoutVal, withoutToTake)
#    return list_of_states
        


def move_min_voters(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of dp_move_max_voters

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    
    tot_ec_votes = sum([state.get_num_ecvotes() for state in winner_states])
    comp_knap = []
    #complement of knapsack -> fill in states that weren't in your knapsack originilly
    for state in winner_states:
        if state not in fastMaxVal(winner_states, tot_ec_votes - ec_votes_needed)[1]:
            comp_knap.append(state)
    return comp_knap


# Problem 6
def flip_election(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. 
    Moves voters from states that were won by the losing candidate (states not in winner_states), 
    to each of the states in swing_states.
    To win a swing state, you must move (margin + 1) new voters into that state. Any state that voters are
    moved from should still be won by the loser even after voters are moved.
    Reminder that you cannot move voters out of California, Washington, Texas, or Tennessee. 

    Also finds the number of EC votes gained by this rearrangement, as well as the minimum number of 
    voters that need to be moved.

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of move_min_voters or greedy_election)

    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple, (from_state, to_state), the 2 letter abbreviation of the State 
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
    None, if it is not possible to sway the election
    """
    #initializes variables
    losing_state_margins = {}
    moving_map = {}
    loser_states = []
    tot_voters_changed = 0
    EC_gained = 0
    #all loser states
    for losing_state in election:
        if losing_state not in get_winner_states(election):
            loser_states.append(losing_state)
    sum_losing_votes = 0      
    for state in loser_states:
        sum_losing_votes += state.get_margin()
   
    
    #dict_states = {losing_non_swing:}
    for state in swing_states:
        votes_needed = state.get_margin() + 1
    
    sum_swing_states = 0
    for swing_state in swing_states:
        sum_swing_states+=swing_state.get_margin()
        
    
    #losing state margins
    no_no_states = ['CA', 'WA', 'TN', 'TX']
    for losing_state in loser_states.copy():
        if losing_state.get_name() not in no_no_states:
            losing_state_margins[losing_state.get_name()] = losing_state.get_margin()-1
    for state in loser_states.copy():
        if state.get_name() == 'CA':
            loser_states.remove(state)
    
    
    #checks if election flip is possible
    if sum_losing_votes <= sum_swing_states:
        return None
    
    print (losing_state_margins)
    voters_moved = 0
    for swing_state in swing_states.copy():
        voters_needed = swing_state.get_margin() + 1
    
        
        
        
        EC_gained += swing_state.get_num_ecvotes()
        #loops through each loser state in the dictionary of losing states : margins
        for loser_state in losing_state_margins:
            if loser_state in no_no_states:
                pass
            #base case: no more voters needed
            if voters_needed == 0:
                break
            if losing_state_margins[loser_state] == 0:
                pass
            #if the margin of the next losing state is larger than the votes needed
            #continue to pump voters into state
            if losing_state_margins[loser_state] >= voters_needed:
                pair = (loser_state, swing_state)
                #print (type(pair))
                moving_map[(loser_state, swing_state.get_name())] = voters_needed
                tot_voters_changed += voters_needed
                voters_needed = 0
                losing_state_margins[loser_state] = 0
            #if the margins is less than zero for the next lost state
            #update your Voters_Needed variable and your other variables
            elif losing_state_margins[loser_state]>0:
                moving_map[(loser_state, swing_state.get_name())] = losing_state_margins[loser_state]
                voters_needed -= losing_state_margins[loser_state]
                tot_voters_changed = losing_state_margins[loser_state]
                losing_state_margins[loser_state] -= losing_state_margins[loser_state]
                
            #tot_voters_changed += losing_state_margins[loser_state]

            
  
    return (moving_map, EC_gained, sum(moving_map.values()))
                
                
    
    
    
    
    
    
    
    
    #1: check possible at all
    # if swing_state_votes_needed > losinf_state_margin
      #then not possible
    #2: for every swing state:
    #   look at every state margin:
        #is losing margin>votes_needed?
        #if yes: add to our mapping
        #(losing state, swing state): votes_needed
    #dont forget to update losing state margin
#    winner_states = get_winner_states(election)
#    #won by loser but are swing states
#    #loser_states.append(state) if state not in winner_states for state in swing_states
#    dict_move = {}
#    swing_voters = 0
#    
#    
#    for state in election:
#        if state not in swing_states:
#            if state not in winner_states:
#                losing_non_swing.append(state)
#    for state in losing_non_swing:
#        state.get_margin()+1
        
        
   # if total margin > total swing margin:
        
   # sorted_losing_non_swing = sorted(losing_non_swing)
    
    
    #IDEA
    #move voters from oveflowing states so that it wont change the outcome for the state
    #into swing states
    
#    for state in move_min_voters(winner_states)
#    election_moves = {(from_state, to_state): voters_moved}


if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

#      tests Problem 1 
    ma = State("MA", 100000, 20000, 8)
    print(isinstance(ma, State))
    print(ma)

     # tests Problem 2 
    year = 2012
    election = load_election("%s_results.txt" % year)
    print(len(election))
    print(election[0])

    # # tests Problem 3
    winner, loser = find_winner(election)
    won_states = get_winner_states(election)
    names_won_states = [state.get_name() for state in won_states]
    ec_votes_needed = ec_votes_reqd(election)
    print("Winner:", winner, "\nLoser:", loser)
    print("States won by the winner: ", names_won_states)
    print("EC votes needed:",ec_votes_needed, "\n")

    # # tests Problem 4
    print("greedy_election")
    greedy_swing = greedy_election(won_states, ec_votes_needed)
    names_greedy_swing = [state.get_name() for state in greedy_swing]
    voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
    ecvotes_greedy = sum([state.get_num_ecvotes() for state in greedy_swing])
    print("Greedy swing states results:", names_greedy_swing)
    print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.\n")

    # # tests Problem 5: dp_move_max_voters
    print("dp_move_max_voters")
    total_lost = sum(state.get_num_ecvotes() for state in won_states)
    move_max = dp_move_max_voters(won_states, total_lost-ec_votes_needed)
    max_states_names = [state.get_name() for state in move_max]
    max_voters_displaced = sum([state.get_margin()+1 for state in move_max])
    max_ec_votes = sum([state.get_num_ecvotes() for state in move_max])
    print("States with the largest margins:", max_states_names)
    print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # # tests Problem 5: move_min_voters
    print("move_min_voters")
    swing_states = move_min_voters(won_states, ec_votes_needed)
    swing_state_names = [state.get_name() for state in swing_states]
    min_voters = sum([state.get_margin()+1 for state in swing_states])
    swing_ec_votes = sum([state.get_num_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # # tests Problem 6: flip_election
    print("flip_election")
    flipped_election = flip_election(election, swing_states)
    print("Flip election mapping:", flipped_election)
