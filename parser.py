import ply.yacc as yacc
from lexer import tokens

# ------------------------------------------------------------
# PRECEDENCIA (opcional pero recomendado)
# ------------------------------------------------------------

precedence = (
    ('left', 'OP_LOG'),
    ('left', 'OP_REL'),
    ('left', 'OP_ARIT'),
)

# ------------------------------------------------------------
# PROGRAMA
# ------------------------------------------------------------

def p_program(p):
    'program : items'
    p[0] = ('program', p[1])
    print("Análisis sintáctico exitoso: programa válido.")

def p_items_multiple(p):
    'items : items item'
    p[0] = p[1] + [p[2]]

def p_items_single(p):
    'items : item'
    p[0] = [p[1]]

def p_item(p):
    '''item : declaration
            | statement'''
    p[0] = p[1]

# ------------------------------------------------------------
# DECLARACIONES
# ------------------------------------------------------------

def p_declaration_with_assign(p):
    'declaration : type IDENT ASIGN expression PUNTOCOM'
    p[0] = ('decl_assign', p[1], p[2], p[4])

def p_declaration_simple(p):
    'declaration : type IDENT PUNTOCOM'
    p[0] = ('decl', p[1], p[2])

def p_type(p):
    '''type : FLOAT
            | BOOLEAN
            | CHAR'''
    p[0] = p[1]

# ------------------------------------------------------------
# STATEMENTS
# ------------------------------------------------------------

def p_statement_assignment(p):
    'statement : assignment PUNTOCOM'
    p[0] = p[1]

def p_statement_println(p):
    'statement : println_stmt PUNTOCOM'
    p[0] = p[1]

def p_statement_if(p):
    'statement : if_stmt'
    p[0] = p[1]

def p_statement_while(p):
    'statement : while_stmt'
    p[0] = p[1]

def p_statement_block(p):
    'statement : block'
    p[0] = p[1]

# ------------------------------------------------------------
# SENTENCIA: ASIGNACIÓN
# ------------------------------------------------------------

def p_assignment(p):
    'assignment : IDENT ASIGN expression'
    p[0] = ('assign', p[1], p[3])

# ------------------------------------------------------------
# PRINTLN
# ------------------------------------------------------------

def p_println_empty(p):
    'println_stmt : PRINTLN PARENINI PARENFIN'
    p[0] = ('println', None)

def p_println_args(p):
    'println_stmt : PRINTLN PARENINI arg_list PARENFIN'
    p[0] = ('println', p[3])

def p_arg_list_multiple(p):
    'arg_list : arg_list COMA expression'
    p[0] = p[1] + [p[3]]

def p_arg_list_single(p):
    'arg_list : expression'
    p[0] = [p[1]]

# ------------------------------------------------------------
# IF
# ------------------------------------------------------------

def p_if_stmt(p):
    'if_stmt : IF PARENINI expression PARENFIN statement'
    p[0] = ('if', p[3], p[5])

# ------------------------------------------------------------
# WHILE
# ------------------------------------------------------------

def p_while_stmt(p):
    'while_stmt : WHILE PARENINI expression PARENFIN statement'
    p[0] = ('while', p[3], p[5])

# ------------------------------------------------------------
# BLOQUES
# ------------------------------------------------------------

def p_block(p):
    'block : LLAVEINI items LLAVEFIN'
    p[0] = ('block', p[2])

# ------------------------------------------------------------
# EXPRESIONES
# ------------------------------------------------------------

def p_expression(p):
    'expression : logic_or'
    p[0] = p[1]

# LOGIC OR
def p_logic_or_multiple(p):
    'logic_or : logic_or OP_LOG logic_and'
    p[0] = ('log_or', p[1], p[3])

def p_logic_or_single(p):
    'logic_or : logic_and'
    p[0] = p[1]

# LOGIC AND
def p_logic_and_multiple(p):
    'logic_and : logic_and OP_LOG logic_not'
    p[0] = ('log_and', p[1], p[3])

def p_logic_and_single(p):
    'logic_and : logic_not'
    p[0] = p[1]

# NOT
def p_logic_not(p):
    '''logic_not : OP_LOG logic_not
                 | rel'''
    if p[1] == 'not':
        p[0] = ('not', p[2])
    else:
        p[0] = p[1]

# RELACIONALES
def p_rel_comparison(p):
    'rel : rel OP_REL add'
    p[0] = ('rel', p[1], p[2], p[3])

def p_rel_single(p):
    'rel : add'
    p[0] = p[1]

# SUMA / RESTA
def p_add(p):
    '''add : add OP_ARIT mul
           | mul'''
    if len(p) == 4:
        p[0] = ('add', p[1], p[2], p[3])
    else:
        p[0] = p[1]

# MULTIPLICACIÓN / DIVISIÓN
def p_mul(p):
    '''mul : mul OP_ARIT unary
           | unary'''
    if len(p) == 4:
        p[0] = ('mul', p[1], p[2], p[3])
    else:
        p[0] = p[1]

# UNARIOS
def p_unary_negative(p):
    'unary : OP_ARIT unary'
    if p[1] == '-':
        p[0] = ('uminus', p[2])
    else:
        p[0] = ('uplus', p[2])

def p_unary_primary(p):
    'unary : primary'
    p[0] = p[1]

# PRIMARIOS
def p_primary_ident(p):
    'primary : IDENT'
    p[0] = ('ident', p[1])

def p_primary_num(p):
    'primary : NUM'
    p[0] = ('num', p[1])

def p_primary_bool(p):
    'primary : BOOL'
    p[0] = ('bool', p[1])

def p_primary_char(p):
    'primary : CHARLIT'
    p[0] = ('char', p[1])

def p_primary_grouped(p):
    'primary : PARENINI expression PARENFIN'
    p[0] = p[2]

# LLAMADA MIN
def p_primary_min(p):
    'primary : MIN PARENINI expression COMA expression PARENFIN'
    p[0] = ('min', p[3], p[5])

# LLAMADA CEIL
def p_primary_ceil(p):
    'primary : CEIL PARENINI expression PARENFIN'
    p[0] = ('ceil', p[3])

# ------------------------------------------------------------
# ERROR SINTÁCTICO
# ------------------------------------------------------------

def p_error(p):
    if p:
        print(f"Error sintáctico en línea {p.lineno}: token inesperado -> {p.type}")
    else:
        print("Error sintáctico: fin de archivo inesperado")

# ------------------------------------------------------------
# COMPILAR EL PARSER
# ------------------------------------------------------------

parser = yacc.yacc()
