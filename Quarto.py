#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 3.6
# @Filename:    test_agent.py
# @Author:      Samuel Hill
# @Date:        2020-02-10 15:39:38
# @Last Modified by:   Samuel Hill
# @Last Modified time: 2020-02-13 15:35:35

"""Simple example file for how to use Pythonian, and a test file to explore all
of the functionality Pythonian (and it's helpers) provide
Attributes:
    LOGGER (logging): The logger (from logging) to handle debugging
"""

from logging import getLogger, DEBUG, INFO, ERROR
from time import sleep
from typing import Any
from random import random
from companionsKQML import Pythonian, convert_to_boolean, convert_to_int
from kqml import KQMLPerformative

LOGGER = getLogger(__name__)

class QuartoAgent(Pythonian):
    """Pythonian agent specifically made to test functionality
    Attributes:
        name (str): This is the name your agent will register with
    """

    name = "QuartoAgent"

    def __init__(self, **kwargs):
        kwargs['debug'] = False  # you don't need this line in your agents
        super().__init__(**kwargs)
        self.facts = list() # Results of any ask (resultant data) or plan (:success or [])
        self.askInProgress = False # Variable to check if an ask is in progress
        if self.debug:
            LOGGER.setLevel(DEBUG)
        else:
            LOGGER.setLevel(ERROR)

        
        # (test_ask_return_list1 ?_input ?return)
        self.add_ask(self.test_ask_return_list1)
        # (test_ask_return_list2 ?_input ?return1 ?return2)
        self.add_ask(self.test_ask_return_list2)
        # (test_ask_return_string ?_input ?return)
        self.add_ask(self.test_ask_return_string)
        # (test_ask_return_int ?_input ?return)
        self.add_ask(self.test_ask_return_int)
        # (test_ask_return_dict ?_input ?return)
        self.add_ask(self.test_ask_return_dict)

        self.add_achieve(self.test_achieve)
        self.add_achieve(self.test_achieve_return)
        self.add_achieve(self.test_convert_boolean)
        
        self.add_subscription('(test_junk_mail ?x)')


    @staticmethod
    def test_ask_return_list1(_input: Any):
        """Simple function to be called by ask-one queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            list: passes the input back along as a list to check the full input
                /output cycle in companions
        """
        LOGGER.debug('testing ask with _input %s', _input)
        return [_input]

    @staticmethod
    def test_ask_return_list2(_input: Any):
        """Simple function to be called by ask-one queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            list: passes the strings pass and test as a list to check the full
                input/output cycle in companions
        """
        LOGGER.debug('testing ask with _input %s', _input)
        return ["pass", "test"]

    @staticmethod
    def test_ask_return_string(_input: Any):
        """Simple function to be called by ask-one queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            list: passes the string pass to check the full input /output cycle
                in companions
        """
        LOGGER.debug('testing ask with _input %s', _input)
        return "pass"

    @staticmethod
    def test_ask_return_int(_input: Any):
        """Simple function to be called by ask-one queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            list: passes the string pass to check the full input /output cycle
                in companions
        """
        LOGGER.debug('testing ask with _input %s', _input)
        return 1

    @staticmethod
    def test_ask_return_dict(_input: Any):
        """Simple function to be called by ask-one queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            list: passes a populated dictionary to check the full input/output
                cycle in companions
        """
        LOGGER.debug('testing ask with _input %s', _input)
        return {'key1': ['a', 'b'], 'key2': 'c'}

    @staticmethod
    def test_achieve(_input: Any):
        """Simple function to be called by achieve queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        """
        LOGGER.debug('testing achieve with _input %s', _input)

    @staticmethod
    def test_achieve_return(_input: Any):
        """Simple function to be called by achieve queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            1, always a 1 for testing purposes
        """
        LOGGER.debug('testing achieve with _input %s', _input)
        return 1

    @staticmethod
    def test_convert_boolean(to_be_bool: Any):
        """Simple function to be called by achieve queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            bool: _input from companions converted to a boolean
        """
        LOGGER.debug('testing achieve with _input %s', to_be_bool)
        now_bool = convert_to_boolean(to_be_bool)
        LOGGER.debug('boolean conversion new value is %s', now_bool)
        return now_bool

    @staticmethod
    def test_convert_int(to_be_int: Any):
        """Simple function to be called by achieve queries by the same name
        Args:
            _input (Any): input to be passed to this function from companions
        Returns:
            int: _input from companions converted to a int
        """
        LOGGER.debug('testing achieve with _input %s', to_be_int)
        now_int = convert_to_int(to_be_int)
        LOGGER.debug('int conversion new value is %s', now_int)
        return now_int

    def more_junk_mail(self, data: Any):
        """Update the test_junk_mail subscription with the new data
        Args:
            data (Any): content of the junk mail to update the subscription
                with
        """
        LOGGER.debug('more junk mail has arrived %s', data)
        self.update_subscription('(test_junk_mail ?x)', data)

    def test_insert_to_companion(self, data: Any):
        """Insert the data into the session-reasoner (kb agent)
        Args:
            data (Any): fact to be inserted
        """
        LOGGER.debug('testing inserting data into Companion %s', data)
        self.insert_data(self, 'session-reasoner', data)

    def receive_tell(self, msg, content):
        """Override to store content and reply
        with nothing

        Arguments:
            msg {KQMLPerformative} -- tell to be passed along in reply
            content {KQMLPerformative} -- tell from companions to be logged
        """
        LOGGER.debug('received tell: %s', content)  # lazy logging
        for c in content:
            self.facts.append(c)
        if self.ask_in_progress:
            self.ask_in_progress = False
        reply_msg = KQMLPerformative('tell')
        reply_msg.set('sender', self.name)
        reply_msg.set('content', None)
        self.reply(msg, reply_msg)
        
    def ask_agent(self, receiver, data, query_type='user::query'):
        self.facts = []
        self.ask_in_progress = True
        super().ask_agent(receiver,data,query_type)

    def achieve_on_agent(self,receiver: str, data: Any):
        self.facts = []
        super().achieve_on_agent(receiver,data)

#Old testing code
'''
def takeYourTurn(AGENT):
    print('It is your turn.')
    giveSet = False
    while (not giveSet):
        print('Input the X coordinate of the location you will put your piece.')
        print('Only input the integer, and hit enter.')
        x = input()
        print('Input the Y coordinate of the location you will put your piece.')
        print('Only input the integer, and hit enter.')
        y = input()
        AGENT.achieve_on_agent('session-reasoner','(placePieceLocation '+x+' '+y+')' )
        sleep(3)
        if (AGENT.facts != []):
            giveSet = True
        else:
            print('There was an error! Try inputting again.')
            
    print('Checking for terminal state... ')
    AGENT.ask_agent('session-reasoner','(winningBoard 100)')
    sleep(30)
    if len(AGENT.facts) > 0:
        print('Game is over!')
        return True
    givePieceHuman(AGENT)
    return False
    
def takeMachineTurn(AGENT):
    print("It is the machine's turn.")
    print("Machine is placing piece...")
    AGENT.achieve_on_agent('session-reasoner','(placePiece)')
    sleep(10)
    
    print('Checking for terminal state... ')
    AGENT.ask_agent('session-reasoner','(winningBoard 100)')
    sleep(30)
    if len(AGENT.facts) > 0:
        print('Game is over!')
        return True
    print("Machine is giving piece...")
    AGENT.achieve_on_agent('session-reasoner','(givePiece)')
    sleep(15)
    return False

def givePieceHuman(AGENT):
    print("It's your turn to give a piece.")
    giveSet = False
    while (not giveSet):
        print('Input a number, from 1-16, representing the piece to give them.')
        p = input()
        AGENT.achieve_on_agent('session-reasoner','(givePieceSpec piece'+p+')' )
        sleep(5)
        if (AGENT.facts != []):
            print('Piece has been successfully given.')
            giveSet = True
        else:
            print('There was an error! Try inputting again.')
    
    return None
'''

#This query method handles wait times by 
def query(AGENT,queryString):
    AGENT.ask_agent('session-reasoner',queryString)
    seconds = 0
    while (AGENT.ask_in_progress == True):
        sleep(1)
        seconds += 1
    return seconds

def plan(AGENT,planString,waitTime: int):
    AGENT.achieve_on_agent('session-reasoner',planString)
    sleep(waitTime)
    print(planString + ": " + str(AGENT.facts))
    return True

def safePlan(AGENT,planString):
    print(planString+" is starting")
    AGENT.achieve_on_agent('session-reasoner',planString)
    while len(AGENT.facts) < 1:
        sleep(1)
    print(planString + ": " + str(AGENT.facts))
    return True

#Some methods to contain companions strings to Quarto.py
def resetBoard(AGENT):
    return safePlan(AGENT,'(resetBoard)')

def setPlayerType(AGENT,ptype):
    return safePlan(AGENT,'(setPlayerType '+str(ptype)+')')

def givePieceMachine(AGENT):
    print("Figuring out what piece to give...")
    return safePlan(AGENT,'(givePiece)')

def placePieceMachine(AGENT):
    print("Figuring out where to place this piece...")
    return safePlan(AGENT,'(placePiece)')

def givePieceHuman(AGENT,pieceNum: int):
    return safePlan(AGENT,'(givePieceSpec piece'+pieceNum+')')

def placePieceHuman(AGENT,x: int,y: int):
    return safePlan(AGENT,'(placePieceLocation '+str(x)+' '+str(y)+')')

def getBoard(AGENT):
    query(AGENT,'(cell ?x ?y ?piece)')
    return AGENT.facts

def givenPiece(AGENT):
    query(AGENT,'(givenPiece ?piece)')
    return str(AGENT.facts[0][1])

def gameIsOver(AGENT):
    #Check for tie
    done = (len(query(AGENT,'(unplacedPiece ?piece)')) == 0)
    #Otherwise check for win
    query(AGENT,'(boardWon ?result)')
    winner = "True" in str(AGENT.facts[0][1])
    if winner:
        return "Won"
    elif done:
        return "Tie"
    return "Not over"

if __name__ == "__main__":
    AGENT = QuartoAgent.parse_command_line_args()
    
    plan(AGENT,'(resetBoard)',5)
    plan(AGENT,'(setPlayerType Denier)',5)
    query(AGENT,'(cell ?x ?y ?piece)')
    print(AGENT.facts)
    gameOver = False
    while (not gameOver):
        safePlan(AGENT,'(givePiece)')
        s = query(AGENT,'(givenPiece ?piece)')
        print("Given piece is: "+str(AGENT.facts[0][1]))
        safePlan(AGENT,'(placePiece)')
        s = query(AGENT,'(givenPiece ?piece)')
        print("Given piece is: "+str(AGENT.facts[0][1]))
        query(AGENT,'(cell ?x ?y ?piece)')
        print(AGENT.facts)
        query(AGENT,'(boardWon ?result)')
        print(str(AGENT.facts[0][1]))
        if ("True" in str(AGENT.facts[0][1])):
            gameOver = True

            
    '''
    plan(AGENT,'(givePieceSpec piece1)',15)
    plan(AGENT,'(placePieceLocation 1 1)',15)
    plan(AGENT,'(givePieceSpec piece2)',15)
    plan(AGENT,'(placePieceLocation 1 2)',15)
    plan(AGENT,'(givePieceSpec piece3)',15)
    plan(AGENT,'(placePieceLocation 1 3)',15)
    query(AGENT,'(cell ?x ?y ?piece)')
    print(AGENT.facts)
    s = query(AGENT,'(boardWon ?result)')
    print(AGENT.facts)
    plan(AGENT,'(givePieceSpec piece4)',15)
    plan(AGENT,'(placePieceLocation 1 4)',15)
    query(AGENT,'(cell ?x ?y ?piece)')
    print(AGENT.facts)
    s = query(AGENT,'(boardWon ?result)')
    print(AGENT.facts)
    '''
    
    #Actual Game Code from here
    '''
    AGENT.achieve_on_agent('session-reasoner','(resetBoard)')
    sleep(5)
    print('Welcome to Quarto!')
    print()
    first = 1
    num = random()
    if num < 0.5:
        first = 0
        print('The machine will go first.')
        giveSet = False
        givePieceHuman(AGENT)
    else:
        print('You will go first. Machine is giving its piece...')
        AGENT.achieve_on_agent('session-reasoner','(givePiece)')
        sleep(15)
        print('The machine has given its piece.')
        
    gameOver = False
    given = ""
    active = 0
    
    while (not gameOver):
        AGENT.ask_agent('session-reasoner','(cell ?x ?y ?piece)')
        sleep(5)
        print('The current board state is:')
        print(str(AGENT.facts))
        AGENT.ask_agent('session-reasoner','(givenPiece ?piece)')
        sleep(10)
        given = str(AGENT.facts[0][1])
        print('Given piece is ' + str(given))
        if first == 0:
            active = 1
            gameOver = takeMachineTurn(AGENT)
        else:
            active = 0
            gameOver = takeYourTurn(AGENT)
        if gameOver:
            break

        AGENT.ask_agent('session-reasoner','(cell ?x ?y ?piece)')
        sleep(5)
        print('The current board state is:')
        print(str(AGENT.facts))
        AGENT.ask_agent('session-reasoner','(givenPiece ?piece)')
        sleep(10)
        given = str(AGENT.facts[0][1])
        print('Given piece is ' + str(given))
        if first == 0:
            active = 0
            gameOver = takeYourTurn(AGENT)
        else:
            active = 1
            gameOver = takeMachineTurn(AGENT)
        if gameOver:
            break

    if active == 0:
        print('You win!')
    else:
        print('The computer has won!')
    print('Press enter to exit.')
    z = input()
    exit()
    '''
        
