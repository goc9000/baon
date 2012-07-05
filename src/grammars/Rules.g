grammar Rules;

options {
    language=Python;
}

@header {
    from logic.RuleSet import RuleSet
    from logic.Rule import Rule
    from logic.matches.special.MatchSequence import MatchSequence
    from logic.matches.special.BetweenMatch import BetweenMatch
    from logic.matches.special.SearchReplaceMatch import SearchReplaceMatch
    from logic.matches.special.SubRuleMatch import SubRuleMatch
    from logic.matches.special.RepeatMatch import RepeatMatch
    from logic.matches.syn.InsertAliasMatch import InsertAliasMatch
    from logic.matches.syn.InsertLiteralMatch import InsertLiteralMatch
    from logic.matches.FormatMatch import FormatMatch
    from logic.matches.LiteralMatch import LiteralMatch
    from logic.matches.RegexMatch import RegexMatch
    from logic.matches.StartAnchorMatch import StartAnchorMatch
    from logic.matches.EndAnchorMatch import EndAnchorMatch
    from logic.actions.ApplyFunctionAction import ApplyFunctionAction
    from logic.actions.ApplyRuleSetAction import ApplyRuleSetAction
    from logic.actions.DeleteAction import DeleteAction
    from logic.actions.SaveToAliasAction import SaveToAliasAction
    from logic.actions.ReformatAction import ReformatAction
    from logic.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
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

// Lexer rules

fragment OP_RULE_SEP : ';';
OP_OR                : '|';
OP_DELETE            : '!';
OP_XFORM             : '->';
OP_INSERT            : '<<';
OP_SAVE              : '>>';
OP_OPEN_PARA         : '(';
OP_CLOSE_PARA        : ')';
OP_OPTIONAL          : '?';
OP_STAR              : '*';
OP_PLUS              : '+';
OP_SEARCH            : '@';
OP_BETWEEN           : '..';
ANCHOR_START         : '^';
ANCHOR_END           : '$';
WS                   : (' '|'\t') {$channel=HIDDEN;};
fragment LINE_SEP    : ('\r'|'\n');
fragment HEX_DIGIT   : ('0'..'9'|'a'..'f'|'A'..'F');
fragment UNICODE_ESC : '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT;
fragment OCTAL_ESC   : '\\' ('0'..'3') ('0'..'7') ('0'..'7')
                     | '\\' ('0'..'7') ('0'..'7')
                     | '\\' ('0'..'7');
fragment ESC_SEQ     : '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
                     | UNICODE_ESC
                     | OCTAL_ESC;
STRING_LITERAL       : '"' (ESC_SEQ | ~('\\'|'"'))* '"'
                     | '\'' (ESC_SEQ | ~('\\'|'\''))* '\'';
FORMAT_SPEC          : '%' ('0'..'9')* ('a'..'z'|'A'..'Z')+;
fragment REGEX_DELIM : '/';
REGEX                : REGEX_DELIM (~REGEX_DELIM|REGEX_DELIM REGEX_DELIM)* REGEX_DELIM ('a'..'z'|'A'..'Z')*;
ID                   : ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;
RULE_SEP             : (OP_RULE_SEP|LINE_SEP)+;

// Parser rules

main          returns [ out_rset ]
              : ruleset EOF { out_rset = $ruleset.out_rset };

ruleset       returns [ out_rset ]
              : { out_rset = RuleSet() }
                  r0=rule { out_rset.rules.append($r0.out_rule) }
                  (RULE_SEP ru=rule { out_rset.rules.append($ru.out_rule) })*;

rule          returns [ out_rule ]
              : { out_rule=Rule() }
                  s0=match_seq { out_rule.alternatives.append($s0.out_seq) }
                  (OP_OR sm=match_seq { out_rule.alternatives.append($sm.out_seq) })*;

match_seq     returns [ out_seq ]
              : { out_seq=MatchSequence() }
                  (st=seq_term { out_seq.terms.append($st.out_term) })*;     

seq_term      returns [ out_term ]
              : OP_BETWEEN { out_term=BetweenMatch() } (a=action { out_term.actions.append($a.out_action) })*
              | OP_SEARCH m=match_ { out_term=SearchReplaceMatch($m.out_match) }
              | m=match_ { out_term=$m.out_match };

match_        returns [ out_match ]
              : ( em=elem_match { out_match=$em.out_match }
                  | sm=insert_match { out_match=$sm.out_match }
                  | OP_OPEN_PARA ru=rule OP_CLOSE_PARA { out_match=SubRuleMatch($ru.out_rule) })
                (a=action { out_match.actions.append($a.out_action) })*
                (
                  	(OP_OPTIONAL { out_match=RepeatMatch(out_match, 0, 1) }
                  	|OP_STAR { out_match=RepeatMatch(out_match, 0, None) }
                  	|OP_PLUS { out_match=RepeatMatch(out_match, 1, None) })
                  	(a=action { out_match.actions.append($a.out_action) })*
                )*;

action        returns [ out_action ]
              : OP_DELETE { out_action=DeleteAction() }
              | OP_SAVE ID { out_action=SaveToAliasAction($ID.text) }
              | OP_XFORM ( OP_OPEN_PARA rs=ruleset OP_CLOSE_PARA { out_action=ApplyRuleSetAction($rs.out_rset) }
                         | STRING_LITERAL { out_action=ReplaceByLiteralAction(decode_literal($STRING_LITERAL.text)) }
                         | FORMAT_SPEC { out_action=ReformatAction($FORMAT_SPEC.text) }
                         | ID { out_action=ApplyFunctionAction($ID.text) }
              );

insert_match  returns [ out_match ]
              : OP_INSERT ( ID {  out_match=InsertAliasMatch($ID.text) }
                          | STRING_LITERAL { out_match=InsertLiteralMatch(decode_literal($STRING_LITERAL.text)) } );

elem_match    returns [ out_match ]
              : FORMAT_SPEC { out_match=FormatMatch($FORMAT_SPEC.text) }
              | STRING_LITERAL { out_match=LiteralMatch(decode_literal($STRING_LITERAL.text)) }
              | REGEX { out_match=RegexMatch($REGEX.text) }
              | ANCHOR_START { out_match=StartAnchorMatch() }
              | ANCHOR_END { out_match=EndAnchorMatch() };
