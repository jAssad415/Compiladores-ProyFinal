import ply.lex as lex

# ------------------------------------------------------------
# LISTA DE TOKENS
# ------------------------------------------------------------

tokens = [
    # Identificadores y literales
    'IDENT',
    'NUM',
    'BOOL',
    'CHARLIT',

    # Operadores
    'OP_ARIT',
    'OP_REL',
    'OP_LOG',
    'ASIGN',

    # Puntuación y símbolos
    'PUNTOCOM',
    'PARENINI',
    'PARENFIN',
    'LLAVEINI',
    'LLAVEFIN',
    'COMA'
]

# Palabras reservadas del lenguaje
reserved = {
    'if'     : 'IF',
    'while'  : 'WHILE',
    'println': 'PRINTLN',
    'min'    : 'MIN',
    'ceil'   : 'CEIL',
    'float'  : 'FLOAT',
    'boolean': 'BOOLEAN',
    'char'   : 'CHAR',
    'true'   : 'BOOL',
    'false'  : 'BOOL',
}

# Agregar tokens de palabras reservadas
tokens += list(reserved.values())

# ------------------------------------------------------------
# IGNORAR ESPACIOS Y TABULACIONES
# ------------------------------------------------------------

t_ignore = ' \t'

# ------------------------------------------------------------
# EXPRESIONES REGULARES BÁSICAS
# ------------------------------------------------------------

t_ASIGN     = r'='
t_PUNTOCOM  = r';'
t_PARENINI  = r'\('
t_PARENFIN  = r'\)'
t_LLAVEINI  = r'\{'
t_LLAVEFIN  = r'\}'
t_COMA      = r','

# Operadores aritméticos
t_OP_ARIT   = r'(\+|\-|\*|/)'

# Operadores relacionales
t_OP_REL    = r'(<=|>=|==|<|>)'

# Operadores lógicos
t_OP_LOG    = r'(and|or|not)'

# ------------------------------------------------------------
# IDENTIFICADORES Y PALABRAS RESERVADAS
# ------------------------------------------------------------

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')  # Si es palabra reservada, cambiar tipo
    return t

# ------------------------------------------------------------
# NÚMEROS: enteros o flotantes
# ------------------------------------------------------------

def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# ------------------------------------------------------------
# BOOLEANOS (true / false)
# Ya se reconocen en reserved: se convierten en token BOOL
# ------------------------------------------------------------

# ------------------------------------------------------------
# LITERAL DE CARACTER: 'a', '\n', '\t', '\''
# ------------------------------------------------------------

def t_CHARLIT(t):
    r"'([^\\]|\\.)'"
    return t

# ------------------------------------------------------------
# COMENTARIOS: /* ... */
# ------------------------------------------------------------

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass  # no devolver token

# ------------------------------------------------------------
# CONTAR LÍNEAS
# ------------------------------------------------------------

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ------------------------------------------------------------
# ERRORES LÉXICOS
# ------------------------------------------------------------

def t_error(t):
    print(f"Error léxico en línea {t.lineno}: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# ------------------------------------------------------------
# CONSTRUIR EL LÉXICO
# ------------------------------------------------------------

lexer = lex.lex()
