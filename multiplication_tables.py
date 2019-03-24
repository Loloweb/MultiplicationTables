# Learning multiplication tables
# By ***REMOVED*** and his dad (as an exercice for both of them to start learning Python.)
# Inspired by a lost old GWBASIC program dad wrote for my brother and I, a long, long time ago.
# Written an tested only on Windows OS but should be easy to port to Linux, etc. (Remove the colorama module and port the winsound lines)
#
# Algorithm:
# * Ask for all operations randomly in a selected range, until they are all KNOWN.
# * If the first answer to an operation is right, do not ask again this operation, it assumed to be KNOWN.
# * If not, then 2 consecutive answers will be required for this operation. It will then be assumed to be KNOWN and no longer asked again.
# * ("Consecutive" for this operation but probably separated by other operations because operations are asked randomly chosen among the remaining UNKNOWN operations.) 
# * Minimalist display so that the pupil only sees the operation. A typed answer is immediately replaced with the display of the right answer.
# * At the end, display the time/operation score, then the operations that were not answered right at the first time. (i.e. had at least 1 wrong answer.)
# This algorithm will at the end ask repeatedly the same unknown operations. Repetition leads to memorization.

this_version = '3.3'
# History:
# v.3.3 2019-03-24: English version with some small ajustements.
# v.3.2 2018-08-21: 
#    * improved input of from_table, to_table and operation's result so that it does not stop when a letter is typed, neagtive values, etc.
#    * At the end, display the operations which had at least one bad answer
#    * nb_consecutive_right_answers_required variable for the number of required consecutive good answers required if the 1st answer was not good (set to 2 so no change yet)


Title = 'Multiplication table game'
# if the first answer is not right, require this number of consecutive right answers FOR THIS OPERATION
nb_consecutive_right_answers_required = 2
min_table = 0		# minimum table: usually 0 or 1 (maybe better to put 1 here for young pupil?) 
max_table = 12		# maximum table: usually 10 or 12


import winsound
import random
from random import randint
import time

# sys.argv is a list of arguments passed to the script. sys.argv[0] is by default the path of script
# and user defined arguments start with index 1
import sys

# colorama module: see https://pypi.python.org/pypi/colorama#downloads
# Allows to use ANSI sequences on Windows OS, to clear the console, print colored text, position the text at x,y coordinates of the screen
# IMPORTANT! works with print() but not with input()
import colorama
from colorama import Fore, Back, Style

# standard text colors that will be used by this program
# colors and styles from the colorama module:
# Foreground colors: Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
# Background colors: Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE
# styles: Style.DIM, Style.NORMAL, Style.BRIGHT
color_normal = Fore.WHITE + Style.NORMAL + Back.CYAN
color_input = Fore.WHITE + Style.NORMAL + Back.CYAN
color_error = Fore.YELLOW + Style.BRIGHT + Back.CYAN
color_correct = Fore.GREEN + Style.BRIGHT + Back.CYAN

# Clear the screen 
# (uses an ANSI sequence, requires the colorama module on Windows)
def clear_screen():
	print('\x1b[2J', end='')

# Clear the current line (where the cursor is) 
# (uses an ANSI sequence, requires the colorama module on Windows)
def clear_line():
	print('\x1b[2K', end='')

# Move the cursor to the x,y coordinates on the screen 
# (uses an ANSI sequence, requires the colorama module on Windows)
def cursor_xy( x, y ):
	print('\x1b[%d;%dH' % (y, x), end='') 

def press_any_key():
    return input()

# Clear screen and displays the title
def new_screen():
    print( color_normal )
    clear_screen()
    cursor_xy( x_center_text(len(Title)), 1)
    print( color_normal + Title, end='' )


# Select the tables to learn: returns from_table, to_table
def select_table_range():
	from_table = -1
	to_table = -1
	while to_table < from_table or from_table < min_table or from_table > max_table or to_table < 0 or to_table > max_table :
		
		input_text = 'Learn table from (' +str(min_table) + ' to ' + str(max_table) +'): '
		while from_table < min_table or from_table > 10:
			cursor_xy( 1, y_center)
			clear_line()
			cursor_xy( x_center_text(len(input_text)), y_center)
			try:
				from_table = int(input(input_text))
			except:
				from_table = -1
				continue
		
		input_text = '        to table (' +str(min_table) + ' to ' + str(max_table) +'): '
		while to_table < from_table or to_table < min_table or to_table > 10 :
			cursor_xy( 1, (y_center + 1) )
			clear_line()
			cursor_xy( x_center_text(len(input_text)), (y_center + 1) )
			try:
				to_table = input(input_text)
				if to_table == '':
					to_table = from_table
				else:
					to_table = int(to_table)
			except:
				to_table = -1

	return from_table, to_table


# Build a string for the operation. Example: '5 x 9 = '
# Used to display the operation but also to build the key of the operation_dict{} dictionnary 
def operation_str(op1, op2):
    return ( str(op1) + ' x ' + str(op2) + ' = ' )


# Display an operation and ask for the answer
def ask_operation(op1, op2):
    clear_screen()
    text_to_display = operation_str(op1, op2)
    answer = -1
    while answer < 0 or answer > 199 :
        cursor_xy( 1, y_center)
        clear_line()
        cursor_xy( x_center_operation, y_center)
        print(color_input + text_to_display, end='')
        try:
            answer = press_any_key()
            answer = int(answer)
        except:
            answer = -1
    return answer


# Display a "right answer feedback", with an optional message 
def feedback_right_answer(op1, op2, result, Message):
    clear_screen()
    text_to_display = operation_str(op1, op2) + str(result)
    cursor_xy( x_center_operation, y_center)
    print( color_correct + text_to_display, end='' )
    print( color_normal + ' ' + Message, end='' )
    winsound.Beep(440, 100)


# Display a "wrong answer feedback", with an optional message 
def feedback_wrong_answer(op1, op2, result, Message):
    clear_screen()
    text_to_display = operation_str(op1, op2) + str(result)
    cursor_xy( x_center_operation, y_center)
    print( color_error + text_to_display, end='' )
    print( color_normal + ' ' + Message, end='' )
    winsound.Beep(700, 150); winsound.Beep(500, 150);winsound.Beep(400, 150);
    press_any_key()


def final_result_screen():
    # display the number of seconds per operation (not per input: several inputs possible for 1 operation)
    new_screen()
    text = str( round( (elapsed_time / len(operation_dict)), 1 ) ) + ' seconds per operation.'
    cursor_xy( x_center_text(len(text)), y_center)
    print(text)

    press_any_key()
    
    # Display one by one each operation for which at least one wrong answer was typed
    for table in range(from_table, (to_table+1)) :
        for operande in range(0, 11):
            if operation_dict[operation_str(table, operande)]['nb_wrong'] > 0:
                clear_screen()
                feedback_right_answer( table, operande, (table * operande), '<-- SING IT three times! ;-)' )
                press_any_key()
    
    # Display bye bye!
    new_screen()
    text = 'See you soon!'
    cursor_xy( x_center_text(len(text)), y_center)
    print(text)
    winsound.Beep(523, 100);winsound.Beep(698, 100);winsound.Beep(880, 100);winsound.Beep(1046, 200);winsound.Beep(880, 50);winsound.Beep(1046, 300);
    press_any_key()



##################  MAIN  ##################

colorama.init()


# Get the Width and Height of the console window from argv[1] and argv[2]
# The caller must pass them as first and second command line arguments
# On Windows, a shortcut can be created to set the console window size and the font (a BIG font is better, like Consola 72)
if len(sys.argv) < 3:
	print( color_error, 'ERROR: width and height of the console window must be passed as the 2 first command line arguments.' )
	print( color_error, 'Example:  multiplication_table.py 69 22' )
	press_any_key()
	exit(255)
else:
	screen_width = int(sys.argv[1])
	screen_height = int(sys.argv[2])


# horizontally and vertically center the text to display
def x_center_text(text_width):
	return int( (screen_width - text_width) / 2 )
x_center_operation = x_center_text(len('10 x 10 = 100'))   # will always be the same x, "slightly left centered"
y_center = int( screen_height / 2 )

new_screen()

# input the table range to learn, from from_table to to_table
from_table, to_table = select_table_range()

clear_screen()


# operation_dict{}: dictionnary for all operations to ask. The key is for example '5 x 3 =', generated with the function operation_str(op1, op2), hereafter the variable x:
#     Each item operation_dict[x] contains also a dictionary with 2 items: { 'nb_wrong': n, 'nb_last_right': m } where n and m are counters.
#         operation_dict[x]['nb_wrong']        Overall counter of wrong answers for the operation x 
#         operation_dict[x]['nb_last_right']   Counter of consecutive right answers for this operation. It is reset to 0 at each wrong answer.
operation_dict = {}

# operations_not_known[]: list of UNKNOWN operations: when an operation is known, it is removed from this list so that it will not be asked again.
# The index is 0 to n where n is the number of operations to ask because they are not known yet. This list should be empty at the end: all operations will be known.
# The value is also a list with 2 items (table, operande), for example (5, 3) for the operation '3 x 5 =' 
operations_not_known = []

# Generates the tables for the operations to ask: all operations are set to UNKNOWN
for table in range(from_table, (to_table+1)) :
    for operande in range(min_table, (max_table+1)):
        operation_dict[operation_str(table, operande)] = { 'nb_wrong': 0, 'nb_last_right': 0 }
        operations_not_known.append( (table, operande) )


# Stopwatch start time
start_time = time.time()

# While it remains some unknown operations
while len(operations_not_known) > 0:
    #
    # randomly choose an operation among those that are not yet known.: op1 et op2
    index_operations_not_known = randint(0, len(operations_not_known) - 1) 
    op1 = operations_not_known[index_operations_not_known][0]
    op2 = operations_not_known[index_operations_not_known][1]

    # Ask this operation
    answer = ask_operation(op1, op2)

    # Check the answer
    right_result = op1 * op2
    if int(answer) == right_result:
        # right answer
        if ( operation_dict[operation_str(op1, op2)]['nb_wrong'] == 0 ) and ( operation_dict[operation_str(op1, op2)]['nb_last_right'] == 0 ):
            #
            # right answer the first time
            operation_dict[operation_str(op1, op2)]['nb_last_right'] = 1	# Set the last right answer counter to 1answer to 1
            del operations_not_known[index_operations_not_known]      		# This operation is now assumed to be known: remove it from the unknown operation list
            feedback_right_answer( op1, op2, right_result, ':-)' )
        else:
            # right answer not the first time
            if operation_dict[operation_str(op1, op2)]['nb_last_right'] == 0:
                #
                # right answer, the previous answer was wrong ( operation_dict[operation_str(op1, op2)]['nb_wrong'] > 0 )
                operation_dict[operation_str(op1, op2)]['nb_last_right'] = 1
                feedback_right_answer( op1, op2, right_result, "yes, that's it..." )
            else:
                #
                # right answer, the previous answer was right
                operation_dict[operation_str(op1, op2)]['nb_last_right'] += 1
                if operation_dict[operation_str(op1, op2)]['nb_last_right'] >= nb_consecutive_right_answers_required:
                    del operations_not_known[index_operations_not_known]	# This operation is now assumed to be known: remove it from the unknown operation list
                    feedback_right_answer( op1, op2, right_result, 'Yes! done!' )
                else:
                    feedback_right_answer( op1, op2, right_result, 'yes...' )
                
    else:
        # Wrong answer
        operation_dict[operation_str(op1, op2)]['nb_wrong'] += 1			# Overall counter of wrong answers for this operation
        operation_dict[operation_str(op1, op2)]['nb_last_right'] = 0		# Counter of consecutive right answers for this operation. It is reset to 0 at each wrong answer
        feedback_wrong_answer( op1, op2, right_result, '<-- SING IT three times! ;-)' )


# All operations are known: end of learning

# Stopwatch: compute the elapsed time
elapsed_time = time.time() - start_time

final_result_screen()
