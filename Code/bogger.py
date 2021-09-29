from enum import Enum

###########
# Numbers #
###########

NUMBERS = '0123456789'

##########
# Tokens #
##########

class Token_Types(Enum):
    INT = '(-)'
    UNSIGNED = '(/)'
    FLOAT = '(.)'
    BOOL = '(?)'
    CHAR = '(c)'
    STRING = '(s)'
    BIGGER_THEN = '(/\->)'
    SMALLER_THEN = '(\/->)'
    PLUS = '(p)'
    MIN = '(m)'
    EQUAL = '(IS)'
    START_BLOCK = '/'
    END_BLOCK = '\\'
    CODE_BLOCK = 'CODE BLOCK'

    def __str__(self):
        return '%s' % self.value

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
        
#########
# Error #
#########

class Error:
    def __init__(self, error_type, details):
        self.error_type = error_type
        self.details = details

    def __str__(self):
        return '{self.error_type}'.format(self=self)

class CharError(Error):
    def __init__(self, details):
        super().__init__("Unknown input", details)

#########
# Lexer #
#########

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while  self.current_char != None:
            #Space
            if self.current_char in ' \t':
                self.advance()
            #Numbers
            elif self.current_char in NUMBERS:
                tokens.append(self.make_number())
            #Types
            elif self.current_char == 'i':
                self.advance()
                if(self.current_char == 'n'):
                    self.advance()
                    if(self.current_char == 't'):
                        tokens.append(Token_Types.INT.value)
                        self.advance()
            
            elif self.current_char == 'u':
                self.advance()
                if(self.current_char == 'n'):
                    self.advance()
                    if(self.current_char == 's'):
                        self.advance()
                        if(self.current_char == 'i'):
                            self.advance()
                            if(self.current_char == 'g'):
                                self.advance()
                                if(self.current_char == 'n'):
                                    self.advance()
                                    if(self.current_char == 'e'):
                                        self.advance()
                                        if(self.current_char == 'd'):
                                            tokens.append(Token_Types.UNSIGNED.value)
                                            self.advance()
            elif self.current_char == 'b':
                self.advance()
                if(self.current_char == 'o'):
                    self.advance()
                    if(self.current_char == 'o'):
                        self.advance()
                        if(self.current_char == 'l'):
                            tokens.append(Token_Types.BOOL.value)
                            self.advance()

            elif self.current_char == 'float':
                tokens.append(Token_Types.FLOAT)
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token_Types.START_BLOCK)
                self.advance()

            elif(self.current_char == '\\'):
                tokens.append(Token_Types.END_BLOCK)
                self.advance()
                        
            elif self.current_char == 'char':
                tokens.append(Token_Types.CHAR)
                self.advance()
            elif self.current_char == 'string':
                tokens.append(Token_Types.STRING)
                self.advance()
            #Math
            elif self.current_char == '+':
                tokens.append(Token_Types.PLUS.value)
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token_Types.MIN.value)
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token_Types.BIGGER_THEN.value)
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token_Types.SMALLER_THEN.value)
                self.advance()
            #Error
            else:
                char = self.current_char
                self.advance()
                return [], CharError("'" + char + "'")

        return tokens, None

    def make_number(self):
        number_as_string = ''
        amount_of_dots = 0

        while self.current_char != None and self.current_char in NUMBERS + '.': # Checks if current character isn't empty and if current character is in numbers 
            if self.current_char == '.':
                if amount_of_dots == 1:
                    break
                amount_of_dots += 1
                number_as_string += '.'
            else:
                number_as_string += self.current_char # when it does not have a dot it is not a float so number is the current character
            self.advance()
    
        if amount_of_dots == 0:
            return Token(Token_Types.INT, int(number_as_string))
        else:
            return Token(Token_Types.FLOAT, float(number_as_string))


#######
# RUN #
#######

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error
                



