import os 
import sys
import glob
from typing import List, Optional, Tuple
import re 
#import attr


def h_to_txt(h_filename):
    nl_file = h_filename[:h_filename.find('.')]
    print(nl_file)
    txt_filename = str(nl_file + '.txt')
    os.rename(h_filename, txt_filename)
    return txt_filename



def recurse_down(root_dir):
    print(root_dir)
    print(os.getcwd())
    for filename in glob.glob(root_dir + '**/*.h', recursive=True):
        print(filename)
        
        new_filename = h_to_txt(filename)
        print(new_filename)
        parse_txt(new_filename)
        
        '''
        with open(filename) as f:
            rdr = CharReader(f.read())
        tokens = rdr.read_all()
        print(len(tokens))
        print(tokens)
        '''

def parse_txt(txtfile):
    with open(txtfile) as f:
        lines = f.read()
        block = ""
        #previous_line = ""
        #print(lines)
        for line in lines:
            #line = line.strip()
            if "#" in line:
                continue
            
            #arr_line = line.split()
            #for word in arr_line:
            block += line
            '''
            #https://stackoverflow.com/questions/476173/regex-to-pull-out-c-function-prototype-declarations
            if re.match(r"^(\w+( )?){2,}\([^!@#$+%^]+?\)",line):
                print(line)
            '''
            
            #this has to be all of the logic for parsing 
            if '}' in block and '{' in block and '(' in block and ')' in block:
                print("---------")
                func_prototype = block[:block.find('{')]
                print(func_prototype)
                print("---------")
                block = ""
            #previous_line = line

#below class adopted from https://gist.github.com/jjfiv/0370da170b8515e64e5f279a6fc3f1c2
#@attr.s
'''
@attr.s
class Token(object):
    start = attr.ib(type=int)
    kind = attr.ib(type=str)
    contents = attr.ib(type=str, default="")


#below class adopted from https://gist.github.com/jjfiv/0370da170b8515e64e5f279a6fc3f1c2
class CharReader(object):
    def __init__(self, char_data: str):
        self.char_data = char_data
        self.position = 0
        self.limit = len(self.char_data)

    def eof(self) -> bool:
        return self.position >= self.limit

    def peek(self) -> Optional[str]:
        if self.position < self.limit:
            return self.char_data[self.position]
        return None

    def getc(self) -> Optional[str]:
        out = self.peek()
        if out:
            self.position += 1
        return out

    def skip_whitespace(self):
        while True:
            next = self.peek()
            if next is None:
                break
            if next.isspace():
                self.position += 1
                continue
            else:
                break
    
    def consume_quoted_character(self) -> Tuple[bool, str]:
        next = self.getc()
        if next is None:
            raise EOFError()
        if next == "\\":
            # handle escapes!
            esc = self.getc()
            if esc is None:
                raise ValueError("EOF in Escape")
            if esc == "\\":
                return (True, "\\")
            elif esc == "'":
                return (True, "'")
            elif esc == '"':
                return (True, '"')
            elif esc == "n":
                return (True, "\n")
            elif esc == "t":
                return (True, "\t")
            else:
                raise ValueError("Unhandled Escape: \\{}".format(esc))
        return (False, next)
    

    def consume(self, char) -> str:
        actual = self.getc()
        if actual != char:
            print(self.consume_until("\n"))
            raise ValueError(
                "Consume found <{}> but expected <{}>.".format(actual, char)
            )
        return char

    def can_consume(self, literal) -> Optional[str]:
        n = len(literal)
        if self.char_data[self.position : self.position + n] == literal:
            self.position += n
            return literal
        return None

    def consume_until(self, seek: str = "\n") -> str:
        out = []
        while True:
            next = self.peek()
            if next is None:
                raise EOFError()
            if next == seek:
                break
            out.append(next)
            self.position += 1
        return "".join(out)

    def next_token(self) -> Optional[Token]:
        self.skip_whitespace()
        if self.eof():
            return None
        start = self.position
        next = self.peek()

        # consider comments before operators EDIT for C
        if next == "/":
            self.consume("/")
            next = self.peek()
            if next == "*":
                self.consume("*")
                comment = "/*"
                while True:
                    comment += self.consume_until("*")
                    comment += self.consume("*")  # the *
                    if self.peek() == "/":
                        comment += self.consume("/")
                        break
                return Token(start, "/*", comment)
                # multi-line comment found
            else:
                # reset so this can be caught as a single-identifier.
                self.position = start
                next = "/"
        
        if next in OPERATOR_START:
            for op in JAVA_OPERATORS:
                found = self.can_consume(op)
                if found is not None:
                    return Token(start, "operator", found)
            raise ValueError("OPERATOR? startswith {}".format(next))
        elif next == '"':
            self.consume('"')
            quoted_str = ""
            while True:
                esc, ch = self.consume_quoted_character()
                if not esc and ch == '"':
                    break
                else:
                    quoted_str += ch
            return Token(start, "string", quoted_str)
        elif next == "'":
            self.consume("'")
            (_esc, ch) = self.consume_quoted_character()
            self.consume("'")
            return Token(start, "char", ch)
        elif is_java_id_start(next):
            ident = self.consume(next)
            while is_java_id_continue(self.peek()):
                next = self.getc()
                assert next is not None
                ident += next
            if ident in JAVA_KEYWORDS:
                return Token(start, "keyword", ident)
            return Token(start, "id", ident)
        elif is_java_num(next):
            num = self.consume(next)
            while is_java_num(self.peek()):
                next = self.getc()
                assert next is not None
                num += next
            return Token(start, "num", num)
        elif next == "#" or next == "\\":
            line = self.consume_until()
            self.position = self.limit
            return Token(start, "ERROR", line)
        
        raise ValueError(self.position, next)

    def read_all(self) -> List[Token]:
        out: List[Token] = []
        while True:
            tok = self.next_token()
            if tok is None:
                break
            out.append(tok)
        return out
'''

if __name__ == '__main__':
    recurse_down('linux-test/')
    
