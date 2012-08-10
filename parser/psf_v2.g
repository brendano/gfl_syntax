grammar psf;
options {
  output=AST;
  language=Python;
  ASTLabelType=CommonTree;
}

annotate:	(line | NEWLINE)*
	;

line	:	tagexpr
	| 	expr
	|	conjexpr
	|	corefexpr
	;

corefexpr:
		narrow EQ^ narrow
	;

// > is left associative, i.e. a > b > c = (a > b) > c
// < is right associative, i.e. x < y < z = x < (y < z)
// NOTE: a < b > x is interpreted as a < (b > x)
expr	:	lc
	;

lc	:	rc (LARROW^ lc)?
	;

rc	:	atom (RARROW^ atom)*
	;

conjexpr:	DOLLARTOKEN DCOLON^ atom (DCOLON! atom)?
	;


// curlyset has a slightly different distribution than other atoms;
// however, it makes the precedence weird
atom	:	narrow
	|	curlyset
	|	LRB! expr+ (HEAD expr*)? RRB!
	;

narrow	:	TOKEN
	|	DOLLARTOKEN
	|	phrase
	;

curlyset:	LCB^ atom* RCB!
	;

phrase	:	LSB^ TOKEN (TOKEN)+ RSB!
	;

tagexpr :	TOKEN (VOCTAG|INTTAG)^ ;

HEAD	:	'*' ;

LSB 	:	 '[' ;
RSB 	:	 ']' ;

LCB 	:	 '{' ;
RCB 	:	 '}' ;

LRB 	:	 '(' ;
RRB 	:	 ')' ;

DCOLON	:	'::' ;

fragment SLARROW:	('<');
fragment SRARROW:	('>');

RARROW	: (SRARROW|'-'+'>');
LARROW	: (SLARROW|'<''-'+);

// we let NEWLINE consume the \n
COMMENT	:	'//' ~(NL)* {$channel=HIDDEN;}
	;

EATWS 	:	(WS)+ {$channel=HIDDEN;};

fragment WS:	(       '\u0009'   // tab
                |       '\u000b'   // VT
                |       '\u000c'   // FF
                |       '\u0020'   // SPC
                |       '\u00a0'   // NBSP
                |       USP);

EQ	:	'=' ;

NEWLINE	:	(NL)+ {$channel=HIDDEN};

fragment NL :	('\u000a'|'\u000d'|'\u2028'|'\u2029');

fragment USP:	'\u1680'  // OGHAM SPACE MARK
		| '\u2000'  // EN QUAD
		| '\u2001'  // EM QUAD
		| '\u2002'  // EN SPACE
		| '\u2003'  // EM SPACE
		| '\u2004'  // THREE-PER-EM SPACE
		| '\u2005'  // FOUR-PER-EM SPACE
		| '\u2006'  // SIX-PER-EM SPACE
		| '\u2007'  // FIGURE SPACE
		| '\u2008'  // PUNCTUATION SPACE
		| '\u2009'  // THIN SPACE
		| '\u200A'  // HAIR SPACE
		| '\u200B'  // ZERO WIDTH SPACE
		| '\u202F'  // NARROW NO-BREAK SPACE
		| '\u3000'  // IDEOGRAPHIC SPACE
		;


VOCTAG 	:	'\\' WS* ('V'|'v'|'VOC'|'voc'|'VOCATIVE'|'vocative') ;

INTTAG 	:	'\\' WS* ('I'|'i'|'INT'|'int'|'INTERJECTION'|'interjection') ;

DOLLARTOKEN
	:	'$'('a'..'z'|'A'..'Z'|'_')('a'..'z'|'A'..'Z'|'_'|'0'..'9')*  ;

TOKEN   :	~(NL|WS|HEAD|RCB|RRB|RSB|LCB|LRB|LSB|SRARROW|SLARROW)+ ;

