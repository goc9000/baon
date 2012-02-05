grammar Rules;

options {
    language=Python;
}

@rulecatch {
except RecognitionException as exc:
    raise exc
}

@members {
def reportError(self, exc):
    raise exc
def recover(self, exc):
    raise exc
}

@lexer::members {
def reportError(self, exc):
    raise exc
def recover(self, exc):
    raise exc
}

OP_DELETE : '!';
OP_INSERT : '<<';
OP_SAVE   : '>>';

WS : (' '|'\t') {$channel=HIDDEN;};

LINE_SEP : ('\r'|'\n');

LITERAL : '"' (ESC_SEQ | ~('\\'|'"'))* '"'
        | '\'' (ESC_SEQ | ~('\\'|'\''))* '\''
        ;

fragment HEX_DIGIT : ('0'..'9'|'a'..'f'|'A'..'F');

fragment ESC_SEQ : '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
                 | UNICODE_ESC
                 | OCTAL_ESC
                 ;

fragment OCTAL_ESC : '\\' ('0'..'3') ('0'..'7') ('0'..'7')
                   | '\\' ('0'..'7') ('0'..'7')
                   | '\\' ('0'..'7')
                   ;

fragment UNICODE_ESC : '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT;

ID : ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
   ;

xruleset : xrule_sep? xrule (xrule_sep xrule)* xrule_sep? EOF;

xrule_sep : (LINE_SEP | ';')+;

xrule : (xmatch xaction*)+;

xmatch : xliteral_match
       | xinsertion_match
       ;

xaction : xaction_delete
        | xaction_save
        ;

xliteral_match: LITERAL;
xinsertion_match : OP_INSERT (LITERAL | ID);

xaction_delete: OP_DELETE;
xaction_save: OP_SAVE ID;
