import json
import ast
#d = json.dumps('state_county.txt')

infile = open('state_county.txt', 'rU')
content = infile.read()

#print(content)
d = ast.literal_eval(content)
