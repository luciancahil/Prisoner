import random


class Policy:
    """
    Base class for prisoner's dilemma policies.
    Subclasses should implement the get_action method.
    """
    name = None  # Class attribute

    def __init__(self, name):
        self.history = []
        self.name = name

    def get_action(self, opponent_history=None):
        """
        Returns the policy's action: "C" (cooperate) or "D" (defect)
        """
        raise NotImplementedError("Subclasses must implement this method")

    def update(self):
        pass

    def get_name():
        return 


class Helper(Policy):
    """
    A policy that mimics tit-for-tat, unless it meets a friend in need.
    Then it always cooperates
    """
    name = "Helper"  # Class attribute

    def __init__(self):
        super().__init__("Helper")
        self.role = "helper"
        self.opponent = None
        self.call = ["D", "C", "C", "D", "D"]
    
    def get_action(self, opponent_history=None):
        
        if self.opponent == "Stranger":# when dealing with a stranger, perform tit for tat
            return opponent_history[-1]
        elif self.opponent == "in_need": # dealing with a friend in need
            return "C"
        else:
            history_len = len(opponent_history)
            if not (self.call[:history_len] == opponent_history):
                # we are against a stranger
                self.opponent = "Stranger"
                return opponent_history[-1]
            elif(history_len < len(self.call)): 
                # continue listening to the call
                return "C"
            else:
                # we are done the handshake.
                self.opponent = "in_need"

                return "C"
            
class Reciever(Policy):
    """
    A policy that sends out a call for help.
    Will defect against helper, tit for tat otherwise
    """

    name = "Reciever"  # Class attribute

    def __init__(self):
        super().__init__("Reciever")
        self.role = "helper"
        self.opponent = None
        self.call = ["D", "C", "C", "D", "D"]
        self.apology = False
    
    def get_action(self, opponent_history=None):
        if(self.apology):
            self.apology = False
            return "C"
        
        if self.opponent == "Stranger":# when dealing with a stranger, perform tit for tat
            return opponent_history[-1]
        elif self.opponent == "in_need": # dealing with a friend in need
            return "C"
        elif self.opponent == "Helper": # dealing with a friend who offers help
            return "D"
        else:
            history_len = len(opponent_history)

            if not (['C'] * history_len == opponent_history):
                # we are against a stranger
                self.opponent = "Stranger"
                self.apology = True
                return "C"
            elif(history_len < len(self.call)): 
                # continue listening to the call
                return self.call[history_len]
            else:
                # we are done the handshake.
                if(opponent_history == ["C"] * 5):
                    # we are dealing with a helper. They will let us defect
                    self.opponent = "Helper"
                    return "D"
                else:
                    # this is a friend, but they can't help us. 
                    self.opponent = "need"

                    return "C"

class Master(Policy):
    name = "Master"
    def __init__(self):
        super().__init__("Master")
        self.role = "Master"
        self.handshake = ["C", "D", "C", "C", "D"]
        self.actionType = None
        self.angry = False
    
    def get_action(self, opponent_history=None):
        if(self.actionType == "always defect"):
            return "D"
        elif(self.actionType == "Master"):
            # master takes on grim defector, then defects forever if the opponent does
            if(opponent_history[-1] == "D"):
                self.angry = True

            if(self.angry):
                return "D"
            else:
                return "C"
        else:
            history_len = len(opponent_history)

            if not (self.handshake[:history_len] == opponent_history):
                # we are against an enemy. Always defect.
                self.actionType = "always defect"
                return "D"
            elif(history_len < len(self.handshake)): 
                # continue the handshake
                return self.handshake[history_len]
            else:
                # we are done the handshake.
                self.actionType = self.role

                return "C"
            
class Slave(Policy):
    name = "Slave"
    def __init__(self):
        super().__init__("Slave")
        self.role = "Slave"
        self.handshake = ["C", "D", "C", "C", "D"]
        self.actionType = None
    
    def get_action(self, opponent_history=None):
        if(self.actionType == "always defect"):
            return "D"
        elif(self.actionType == "Slave"):
            if(opponent_history[-1] == "D"): # does the opposite of what the opponent last did, inverse tit-for-tat
                return "C"
            else:
                return "D"
        else:
            history_len = len(opponent_history)
            if (history_len <= len(self.handshake) and not (self.handshake[:history_len] == opponent_history)):
                # we are against an enemy. Always defect.
                self.actionType = "always defect"
                return "D"
            elif(history_len < len(self.handshake)): 
                # continue the handshake
                return self.handshake[history_len]
            else:
                # we are done the handshake.
                self.actionType = self.role

                return "D"

class TitForTat(Policy):
    """
    A policy that starts by cooperating and then
    imitates the opponent's previous action.
    """
    name = "Tit-For-Tat"
    def __init__(self):
        super().__init__("Tit-For-Tat")

    def get_action(self, opponent_history=None):
        if not opponent_history or len(opponent_history) == 0:
            return "C"
        else:
            return opponent_history[-1]


class AlwaysDefect(Policy):
    """A policy that always defects."""
    name = "Always Defect"
    def __init__(self):
        super().__init__("Always Defect")

    def get_action(self, opponent_history=None):
        return "D"


def prisoner_dilemma_arena(game_length, policy1, policy2):
    """
    Simulates a game of prisoner's dilemma between two policies.
    Returns a tuple containing the scores of each policy.
    """
    policy1_score = 0
    policy2_score = 0

    payoff_matrix = {
        ('C', 'C'): (3, 3),
        ('C', 'D'): (0, 5),
        ('D', 'C'): (5, 0),
        ('D', 'D'): (1, 1)
    }

    policy1_history = []
    policy2_history = []

    for _ in range(game_length):
        policy1_action = policy1.get_action(policy2_history)
        policy2_action = policy2.get_action(policy1_history)

        policy1_history.append(policy1_action)
        policy2_history.append(policy2_action)

        scores = payoff_matrix[(policy1_action, policy2_action)]

        policy1_score += scores[0]
        policy2_score += scores[1]

    print(policy1_history)
    print(policy2_history)

    return policy1_score, policy2_score

# Example usage:


def print_dict():
    policies = [Master, Slave, Helper, Reciever, TitForTat, AlwaysDefect]

    lines = []

    for i in range(len(policies)):
        for j in range(len(policies)):

            game_length = 100
            policy1 = policies[i]()
            policy2 = policies[j]()

            policy1_score, policy2_score = prisoner_dilemma_arena(
                game_length, policy1, policy2
            )

            print(f"{policy1.name} score: {policy1_score}")
            print(f"{policy2.name} score: {policy2_score}")

            lines.append("('{}', '{}'): {},".format(policy1.name, policy2.name, policy1_score))
            
    for line in lines:
        print(line)

