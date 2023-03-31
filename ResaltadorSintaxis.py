import sys

#Julian Lawrence Gil Soares - A00832272
#para resolver este proyecto implemente una matriz de transicion para ir construyendo las palabras y asignandoles un token que
#se utiliza en la funcion check para colorear ciertas partes del codigo de cierto color y otros de otros colores.
# la complejidad en el peor de los casos del algoritmo es de O(n)

fileI = sys.argv[1]
fileO = sys.argv[2]

#open HTML
fileOut = fileO + ".html"
output = open(fileOut, 'w', encoding = "utf-8")

#tokens
NUM = 100 #numbers
OPE = 101 #operators
SYM = 102 #symbols
VAR = 103 #variable
COM = 104 #coments
INQ = 105 #in quotes
COL = 106 #Colon
END = 107 #end of entry
NLN = 108 #new line
ERR = 200 #error
PAR = 109 #paranthsis
SPA = 110 #empty space
TAB = 111 #tab
# takes the char that was last red and send it too filter and then generates indices for the matrix in the following fashion MT[state][filter]
# [fila][Columna]
#       0    1    2    3    4    5    6    7     8   9    10   11   12
#.     Num  var   .   " "  OPE   (    _    #    ""   :    \n  Tab  Empty
MT = [[NUM,   2, SYM,  13,   4, SYM, SYM,   7,   8, COL, NLN,  14, NLN], # 0- Initial
      [  1, NUM, NUM, NUM, NUM, NUM, NUM, NUM, NUM, NUM, NUM, TAB, END], # 1- Numero
      [NUM,   2, VAR, VAR, VAR, VAR,   2, VAR, VAR, VAR, VAR, TAB, VAR], # 2- Variable 
      [NUM, NUM, ERR, NUM, NUM, NUM, NUM, NUM, NUM, NUM, SYM, TAB, END], # 3- punto 
      [OPE, OPE, ERR, OPE, OPE, OPE, ERR, ERR, OPE, ERR, OPE, TAB, END], # 4- operator
      [NUM, NUM, OPE, SYM, OPE, ERR, SYM, NUM,   8, NUM, SYM, TAB, END], # 5- symbol
      [SYM,   2, VAR, ERR, VAR, VAR, VAR, NUM, NUM, NUM, ERR, TAB, END], # 6- underscore
      [  7,   7,   7,   7,   7,   7,   7,   7,   7,   7, COM, TAB, COM], # 7- Comment
      [ 12,  12,  12,  12,  12,  12,  12,  12,  13,  12, INQ, TAB,  12], # 8- Quote
      [ 10,  10,  10, SPA,  10,  10,  10,  10,  10, ERR, NLN, TAB, COL], # 9- Colon
      [COL, COL, COL, SPA, COL, COL, COL, COL, COL, ERR, NLN, TAB, COL], # 10- New line
      [ERR,  12, ERR, ERR, ERR, ERR, ERR, NUM, NUM, NUM, ERR, TAB, END], # 11- ERROR
      [ 12,  12,  12,  12,  12,  12,  12,  12,  13,  12, INQ, TAB, COL], # 12- 2nd quote
      [INQ, INQ, INQ, INQ, INQ, INQ, INQ, INQ, INQ, INQ, INQ, INQ, INQ], # 13- 3rd quote
      [TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB, TAB], # 14- tab
      [SPA, SPA, SPA, SPA, SPA, SPA, SPA, SPA, SPA, SPA, SPA, TAB, SPA], # 15- empty space
      ]

#filter recives the read from he txt and checks what type of character is read in order to generate the matixs' index
def filter(c):
    if (c =='0' or c =='1' or c =='2' or c =='3' or c =='4' or c =='5' or c =='6' or c =='7' or c =='8' or c =='9'):
        return 0
    elif ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')):
        return 1
    elif (c == '.'):
        return 2
    elif (c == ' ' or c == ''):
        return 3
    elif (c == '+' or c == '-' or c =='*' or c =='/' or c == '^' or c == '=' or c == '<' or c == '>' or c =='!'):
        return 4
    elif (c == '[' or c == ']' or c == ',' or (c =='(' or c == ')')):
        return 5
    elif (c == '_'):
        return 6
    elif (c == '#'):
        return 7
    elif (c == '"' or c == "'"):
        return 8
    elif(c == ':'):
        return 9
    elif(c == '/n'):
        return 10
    elif(c == '/t'):
        return 11
    else:
        return 12

#Main function recives our txt and starts the process of building the words, coloring them and adding them to our HTML
def check(w):
    state = 0
    lex = ""
    i = 0
    flag = True
    output.write("""<pre>""")
    while (i < len(w)):
        if(state < 100 ):
            char = w[i]
            state = MT[state][filter(char)]
            if state >= 100 and flag: 
                flag = False
            else : 
                flag = True

            if flag:
                lex += char

            indent = False
            #Starts adding to the HTML
            if(state >= 100):
                if(state != 107):
                    if (state == NUM):
                        read = False;
                        color = """<font color = "#D36A00">""" #Orange
                        endC = """</font></div>"""
                        output.write(color + lex + endC)
                        
                    if  (state == OPE):
                        read = False;
                        color = """<font color = "#0098D6">""" #blue
                        endC = """</font></div>"""
                        output.write(color + lex + endC)
                        
                    if (state == NLN):
                        read = False;
                        output.write("""<div class="cm-line"> </div> """)
                        
                    if (state == SYM):
                        read = False;
                        color = """<font color = "#7E455B">""" #Scarlet
                        endC = """</font></div>"""
                        output.write(lex)
                                                       
                    if (state == VAR):
                        read = False;
                        if (lex == "import" or lex == "read" or lex == "write" or lex == "for" or lex == "while" or lex == "switch" or lex == "case" or lex == "in"  or lex == "" or lex == "and" or lex == "not" or lex == "or" or lex == "if" or lex == "elif" or lex == "else" or lex == "def" or lex == "print" or lex == "return" or lex == "this" or lex == "False" or lex == "True"):
                            read = False
                            color1 = """<font color = "#0DF2C2">""" #Agent P
                            endC1 = """</font></div>"""
                            output.write(color1 + lex + endC1)
                        else:
                            output.write(lex)
                    if (state == COM):
                        read = False;
                        color = """<font color = "#BEC30A">""" #Yellow
                        endC = """</font></div>"""
                        output.write(color + lex + endC)
                        
                    if (state == INQ):
                        read = False;
                        color = """<font color = "#04EC19">""" #green
                        endC = """</font></div>"""
                        output.write(color + lex + endC)
                        
                    if (state == COL):
                        read = False;
                        output.write(lex)
                        
                    if (state == SPA):
                        read = False;
                        output.write(lex)
                        
                    if (state == TAB):
                        read = False;
                        output.write("""<div> <t></div> """)
                        
                    if (state == END):
                         read = False;
                         output.write(lex)
                        
                    if (state == ERR):
                        read = False;
                        output.write(lex)
                        
                        
        
                lex = ""
                state = 0
                
                    
        if (flag):
            i += 1
    output.write("""</div></body></html>""")

f = open(fileI, "r")
word = f.read() 
check(word)
    
f.close()
output.close()
