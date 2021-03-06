import operator
import random
import re
import json

# Generates multiple numbers from 1 to the number stored in 'sides'
# based on the number stored in 'times'. Returns the result as a
# list.
# --Needs improvement, takes too long for large numbers of iteration.
# Check into embarrasingly parallel processing.
def simple_math(times, sides):
    results = []
    for each in enumerate(range(0, times)):
        results.append(random.randint(1, sides))
    return results

# Performs math based on the operator in the original message.
# Returns the results as a separate list.
def complex_math(results, expression, operand):
    # Declaring dictionary of functions with the key set to each operator.
    operators = {
             "+": operator.add,
             "-": operator.sub,
             "*": operator.mul,
             "/": operator.truediv,
             "^": operator.pow,
             "%": operator.mod
                }
    final_results = []
    for each in results:
        final_results.append(int(round(operators[expression](int(each), int(operand)))))
    return final_results

# Builds the return message for the discord bot to present the
# roll totals. Uses the lists returned by 'complex_math()' and
# 'simple_math()'.

def build_message(string, results, final_results, comment):
    # Splitting comment from rest of the string.
    string = string.split(" #")[0]
    # Removing "!roll " from the string as it is the first 6 characters.
    message = "{0} ".format(string[6:])
    # Setting a final result using the list from 'complex_math()'.
    final_results = sum(final_results)

    # Set message as equal to the initial dice "roll" followed by 
    # sequentially listing each item in 'simple_math()' results and
    # then finally listing the final value.
    for counter, value in enumerate(results):
        if counter == 0:
            message = "{0}({1}".format(message, value)
        else:
            message = "{0}, {1}".format(message, value)
    message = "{0}): {1}{2}".format(message, final_results, comment)
    if len(str(message)) > 2000:
       message = "{0} : {1}{2}".format(string[6:], final_results, comment)
    if len(str(message)) > 2000:
       message = "SIRWHYYOUDOTHIS. MESSAGE TOO LONG. ABORT! ABORT!!!!!!"
    
    return message

# Checks if the string is a valid roll, if it is it performs 'simple_math()',
# 'complex_math', and returns the message built by 'build_message()'.
def roll(string):
    # Pulling capture groups for the number of dice rolled, number of sides for the dice,
    # additional math to be performed on the results, and any comments.
    r = re.compile('^!roll (\d+)d(\d+)(?:([\+\-\/\*\^\%])(\d+))?(?:( #.+))?$')
    m = re.search(r, string)
    # Match will fail if the roll was not valid. Sanitizes input.
    if not m:
        return "This command did not meet the required syntax."
    else:
        # Initializing variables, setting comment/expression/operand to default values
        # incase there were none entered in the original message.
        times = int(m.group(1))
        sides = int(m.group(2))
        comment = ""
        expression = "+"
        operand = 0
        # If regex match  5 exists, replace comment with its contents.
        if m.group(5):
            comment = m.group(5)
        # If regex match 3 exists, replace expression with it. Also replace operand with
        # match 4. And yes, operand is the incorrect word. It's fine.
        if m.group(3):
            expression = m.group(3)
            operand = m.group(4)
        results = simple_math(times, sides)
        final_results = complex_math(results, expression, operand)

        message = build_message(string, results, final_results, comment)
        
        return message

def cast(string):
    #loading the casts.json first, then seeing if it matches, if it does, process roll(string)
    casts = {}
    with open('casts.json') as jsonData:
        casts = json.load(jsonData)
    if casts[string[6:]]:
        return roll("!roll {0}".format(casts[string[6:]]))
    else:
        return "This command did not meet the required syntax or match an existing cast."
