grammar Rules;

options {
    language=Python;
}

@header {
    from logic.RuleSet import *
    from logic.utils import *
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

OP_BETWEEN : '..';
OP_DELETE  : '!';
OP_INSERT  : '<<';
OP_SAVE    : '>>';

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

xruleset returns [ RuleSet rset ]
        : { rset=RuleSet() }
          xrule_sep? r0=xrule { rset.rules.append($r0.rule) }
          (xrule_sep ru=xrule { rset.rules.append($ru.rule) })*
          xrule_sep? EOF;

xrule_sep : (LINE_SEP | ';')+;

xrule returns [ Rule rule ]
        : { rule=Rule() }
          (te=xterm { rule.terms.append($te.term) })+;

xterm returns [ Term term ]
        : { term=Term() }
          ma=xmatch { term.match = $ma.match }
          (ac=xaction { term.actions.append($ac.action) })*;

xmatch returns [ Match match ]
        : (
          m=xliteral_match
        | m=xbetween_match
        | m=xinsertion_match
        ) { match=$m.match };

xaction returns [ Action action ]
        : (
          a=xaction_delete
        | a=xaction_save
        ) { action=$a.action };

xliteral_match returns [ LiteralMatch match ]
        : LITERAL { match = LiteralMatch(decodeLiteral($LITERAL.text)) }
        ;

xbetween_match returns [ BetweenMatch match ]
        : OP_BETWEEN { match = BetweenMatch() }
        ;

xinsertion_match returns [ InsertionMatch match ]
        : OP_INSERT ( LITERAL { match = InsertLiteralMatch(decodeLiteral($LITERAL.text)) }
                    | ID { match = InsertAliasMatch($ID.text) } )
        ;

xaction_delete returns [ DeleteAction action ]
        : OP_DELETE { action = DeleteAction() }
        ;

xaction_save returns [ SaveAction action ]
        : OP_SAVE ID { action = SaveAction($ID.text) }
        ;
