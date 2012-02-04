# $ANTLR 3.0.1 psf.g 2012-02-03 23:04:11

from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
SLARROW=19
RRB=11
RARROW=7
LARROW=6
LRB=10
RCB=14
Tokens=26
EOF=-1
EATWS=24
SRARROW=20
TOKEN=12
USP=25
DCOLON=9
WS=23
NEWLINE=4
LCB=13
DOLLARTOKEN=8
RSB=16
NL=21
VOCTAG=17
EQ=5
COMMENT=22
INTTAG=18
LSB=15

class psfLexer(Lexer):

    grammarFileName = "psf.g"

    def __init__(self, input=None):
        Lexer.__init__(self, input)
        self.dfa14 = self.DFA14(
            self, 14,
            eot = self.DFA14_eot,
            eof = self.DFA14_eof,
            min = self.DFA14_min,
            max = self.DFA14_max,
            accept = self.DFA14_accept,
            special = self.DFA14_special,
            transition = self.DFA14_transition
            )






    # $ANTLR start LSB
    def mLSB(self, ):

        try:
            self.type = LSB

            # psf.g:57:6: ( '[' )
            # psf.g:57:9: '['
            self.match(u'[')





        finally:

            pass

    # $ANTLR end LSB



    # $ANTLR start RSB
    def mRSB(self, ):

        try:
            self.type = RSB

            # psf.g:58:6: ( ']' )
            # psf.g:58:9: ']'
            self.match(u']')





        finally:

            pass

    # $ANTLR end RSB



    # $ANTLR start LCB
    def mLCB(self, ):

        try:
            self.type = LCB

            # psf.g:60:6: ( '{' )
            # psf.g:60:9: '{'
            self.match(u'{')





        finally:

            pass

    # $ANTLR end LCB



    # $ANTLR start RCB
    def mRCB(self, ):

        try:
            self.type = RCB

            # psf.g:61:6: ( '}' )
            # psf.g:61:9: '}'
            self.match(u'}')





        finally:

            pass

    # $ANTLR end RCB



    # $ANTLR start LRB
    def mLRB(self, ):

        try:
            self.type = LRB

            # psf.g:63:6: ( '(' )
            # psf.g:63:9: '('
            self.match(u'(')





        finally:

            pass

    # $ANTLR end LRB



    # $ANTLR start RRB
    def mRRB(self, ):

        try:
            self.type = RRB

            # psf.g:64:6: ( ')' )
            # psf.g:64:9: ')'
            self.match(u')')





        finally:

            pass

    # $ANTLR end RRB



    # $ANTLR start DCOLON
    def mDCOLON(self, ):

        try:
            self.type = DCOLON

            # psf.g:66:8: ( '::' )
            # psf.g:66:10: '::'
            self.match("::")






        finally:

            pass

    # $ANTLR end DCOLON



    # $ANTLR start SLARROW
    def mSLARROW(self, ):

        try:
            # psf.g:68:17: ( ( '<' ) )
            # psf.g:68:19: ( '<' )
            if self.input.LA(1) == u'<':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end SLARROW



    # $ANTLR start SRARROW
    def mSRARROW(self, ):

        try:
            # psf.g:69:17: ( ( '>' ) )
            # psf.g:69:19: ( '>' )
            if self.input.LA(1) == u'>':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end SRARROW



    # $ANTLR start RARROW
    def mRARROW(self, ):

        try:
            self.type = RARROW

            # psf.g:71:8: ( ( SRARROW | ( '-' )+ '>' ) )
            # psf.g:71:10: ( SRARROW | ( '-' )+ '>' )
            # psf.g:71:10: ( SRARROW | ( '-' )+ '>' )
            alt2 = 2
            LA2_0 = self.input.LA(1)

            if (LA2_0 == u'>') :
                alt2 = 1
            elif (LA2_0 == u'-') :
                alt2 = 2
            else:
                nvae = NoViableAltException("71:10: ( SRARROW | ( '-' )+ '>' )", 2, 0, self.input)

                raise nvae

            if alt2 == 1:
                # psf.g:71:11: SRARROW
                self.mSRARROW()



            elif alt2 == 2:
                # psf.g:71:19: ( '-' )+ '>'
                # psf.g:71:19: ( '-' )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == u'-') :
                        alt1 = 1


                    if alt1 == 1:
                        # psf.g:71:19: '-'
                        self.match(u'-')



                    else:
                        if cnt1 >= 1:
                            break #loop1

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1


                self.match(u'>')








        finally:

            pass

    # $ANTLR end RARROW



    # $ANTLR start LARROW
    def mLARROW(self, ):

        try:
            self.type = LARROW

            # psf.g:72:8: ( ( SLARROW | '<' ( '-' )+ ) )
            # psf.g:72:10: ( SLARROW | '<' ( '-' )+ )
            # psf.g:72:10: ( SLARROW | '<' ( '-' )+ )
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == u'<') :
                LA4_1 = self.input.LA(2)

                if (LA4_1 == u'-') :
                    alt4 = 2
                else:
                    alt4 = 1
            else:
                nvae = NoViableAltException("72:10: ( SLARROW | '<' ( '-' )+ )", 4, 0, self.input)

                raise nvae

            if alt4 == 1:
                # psf.g:72:11: SLARROW
                self.mSLARROW()



            elif alt4 == 2:
                # psf.g:72:19: '<' ( '-' )+
                self.match(u'<')

                # psf.g:72:22: ( '-' )+
                cnt3 = 0
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == u'-') :
                        alt3 = 1


                    if alt3 == 1:
                        # psf.g:72:22: '-'
                        self.match(u'-')



                    else:
                        if cnt3 >= 1:
                            break #loop3

                        eee = EarlyExitException(3, self.input)
                        raise eee

                    cnt3 += 1









        finally:

            pass

    # $ANTLR end LARROW



    # $ANTLR start COMMENT
    def mCOMMENT(self, ):

        try:
            self.type = COMMENT

            # psf.g:75:9: ( '//' (~ ( NL ) )* )
            # psf.g:75:11: '//' (~ ( NL ) )*
            self.match("//")


            # psf.g:75:16: (~ ( NL ) )*
            while True: #loop5
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if ((u'\u0000' <= LA5_0 <= u'\t') or (u'\u000B' <= LA5_0 <= u'\f') or (u'\u000E' <= LA5_0 <= u'\u2027') or (u'\u202A' <= LA5_0 <= u'\uFFFE')) :
                    alt5 = 1


                if alt5 == 1:
                    # psf.g:75:16: ~ ( NL )
                    if (u'\u0000' <= self.input.LA(1) <= u'\t') or (u'\u000B' <= self.input.LA(1) <= u'\f') or (u'\u000E' <= self.input.LA(1) <= u'\u2027') or (u'\u202A' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop5


            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end COMMENT



    # $ANTLR start EATWS
    def mEATWS(self, ):

        try:
            self.type = EATWS

            # psf.g:78:8: ( ( WS )+ )
            # psf.g:78:10: ( WS )+
            # psf.g:78:10: ( WS )+
            cnt6 = 0
            while True: #loop6
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == u'\t' or (u'\u000B' <= LA6_0 <= u'\f') or LA6_0 == u' ' or LA6_0 == u'\u00A0' or LA6_0 == u'\u1680' or (u'\u2000' <= LA6_0 <= u'\u200B') or LA6_0 == u'\u202F' or LA6_0 == u'\u3000') :
                    alt6 = 1


                if alt6 == 1:
                    # psf.g:78:11: WS
                    self.mWS()



                else:
                    if cnt6 >= 1:
                        break #loop6

                    eee = EarlyExitException(6, self.input)
                    raise eee

                cnt6 += 1


            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end EATWS



    # $ANTLR start WS
    def mWS(self, ):

        try:
            # psf.g:80:12: ( ( '\\u0009' | '\\u000b' | '\\u000c' | '\\u0020' | '\\u00a0' | USP ) )
            # psf.g:80:14: ( '\\u0009' | '\\u000b' | '\\u000c' | '\\u0020' | '\\u00a0' | USP )
            if self.input.LA(1) == u'\t' or (u'\u000B' <= self.input.LA(1) <= u'\f') or self.input.LA(1) == u' ' or self.input.LA(1) == u'\u00A0' or self.input.LA(1) == u'\u1680' or (u'\u2000' <= self.input.LA(1) <= u'\u200B') or self.input.LA(1) == u'\u202F' or self.input.LA(1) == u'\u3000':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end WS



    # $ANTLR start EQ
    def mEQ(self, ):

        try:
            self.type = EQ

            # psf.g:87:4: ( '=' )
            # psf.g:87:6: '='
            self.match(u'=')





        finally:

            pass

    # $ANTLR end EQ



    # $ANTLR start NEWLINE
    def mNEWLINE(self, ):

        try:
            self.type = NEWLINE

            # psf.g:89:9: ( ( NL )+ )
            # psf.g:89:11: ( NL )+
            # psf.g:89:11: ( NL )+
            cnt7 = 0
            while True: #loop7
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == u'\n' or LA7_0 == u'\r' or (u'\u2028' <= LA7_0 <= u'\u2029')) :
                    alt7 = 1


                if alt7 == 1:
                    # psf.g:89:12: NL
                    self.mNL()



                else:
                    if cnt7 >= 1:
                        break #loop7

                    eee = EarlyExitException(7, self.input)
                    raise eee

                cnt7 += 1


            #action start
            self.channel=HIDDEN
            #action end




        finally:

            pass

    # $ANTLR end NEWLINE



    # $ANTLR start NL
    def mNL(self, ):

        try:
            # psf.g:91:13: ( ( '\\u000a' | '\\u000d' | '\\u2028' | '\\u2029' ) )
            # psf.g:91:15: ( '\\u000a' | '\\u000d' | '\\u2028' | '\\u2029' )
            if self.input.LA(1) == u'\n' or self.input.LA(1) == u'\r' or (u'\u2028' <= self.input.LA(1) <= u'\u2029'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end NL



    # $ANTLR start USP
    def mUSP(self, ):

        try:
            # psf.g:93:13: ( '\\u1680' | '\\u2000' | '\\u2001' | '\\u2002' | '\\u2003' | '\\u2004' | '\\u2005' | '\\u2006' | '\\u2007' | '\\u2008' | '\\u2009' | '\\u200A' | '\\u200B' | '\\u202F' | '\\u3000' )
            # psf.g:
            if self.input.LA(1) == u'\u1680' or (u'\u2000' <= self.input.LA(1) <= u'\u200B') or self.input.LA(1) == u'\u202F' or self.input.LA(1) == u'\u3000':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end USP



    # $ANTLR start VOCTAG
    def mVOCTAG(self, ):

        try:
            self.type = VOCTAG

            # psf.g:111:9: ( '\\\\' ( WS )* ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' ) )
            # psf.g:111:11: '\\\\' ( WS )* ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )
            self.match(u'\\')

            # psf.g:111:16: ( WS )*
            while True: #loop8
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == u'\t' or (u'\u000B' <= LA8_0 <= u'\f') or LA8_0 == u' ' or LA8_0 == u'\u00A0' or LA8_0 == u'\u1680' or (u'\u2000' <= LA8_0 <= u'\u200B') or LA8_0 == u'\u202F' or LA8_0 == u'\u3000') :
                    alt8 = 1


                if alt8 == 1:
                    # psf.g:111:16: WS
                    self.mWS()



                else:
                    break #loop8


            # psf.g:111:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )
            alt9 = 6
            LA9_0 = self.input.LA(1)

            if (LA9_0 == u'V') :
                LA9_1 = self.input.LA(2)

                if (LA9_1 == u'O') :
                    LA9_3 = self.input.LA(3)

                    if (LA9_3 == u'C') :
                        LA9_7 = self.input.LA(4)

                        if (LA9_7 == u'A') :
                            alt9 = 5
                        else:
                            alt9 = 3
                    else:
                        nvae = NoViableAltException("111:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )", 9, 3, self.input)

                        raise nvae

                else:
                    alt9 = 1
            elif (LA9_0 == u'v') :
                LA9_2 = self.input.LA(2)

                if (LA9_2 == u'o') :
                    LA9_5 = self.input.LA(3)

                    if (LA9_5 == u'c') :
                        LA9_8 = self.input.LA(4)

                        if (LA9_8 == u'a') :
                            alt9 = 6
                        else:
                            alt9 = 4
                    else:
                        nvae = NoViableAltException("111:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )", 9, 5, self.input)

                        raise nvae

                else:
                    alt9 = 2
            else:
                nvae = NoViableAltException("111:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )", 9, 0, self.input)

                raise nvae

            if alt9 == 1:
                # psf.g:111:21: 'V'
                self.match(u'V')



            elif alt9 == 2:
                # psf.g:111:25: 'v'
                self.match(u'v')



            elif alt9 == 3:
                # psf.g:111:29: 'VOC'
                self.match("VOC")




            elif alt9 == 4:
                # psf.g:111:35: 'voc'
                self.match("voc")




            elif alt9 == 5:
                # psf.g:111:41: 'VOCATIVE'
                self.match("VOCATIVE")




            elif alt9 == 6:
                # psf.g:111:52: 'vocative'
                self.match("vocative")









        finally:

            pass

    # $ANTLR end VOCTAG



    # $ANTLR start INTTAG
    def mINTTAG(self, ):

        try:
            self.type = INTTAG

            # psf.g:113:9: ( '\\\\' ( WS )* ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' ) )
            # psf.g:113:11: '\\\\' ( WS )* ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )
            self.match(u'\\')

            # psf.g:113:16: ( WS )*
            while True: #loop10
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == u'\t' or (u'\u000B' <= LA10_0 <= u'\f') or LA10_0 == u' ' or LA10_0 == u'\u00A0' or LA10_0 == u'\u1680' or (u'\u2000' <= LA10_0 <= u'\u200B') or LA10_0 == u'\u202F' or LA10_0 == u'\u3000') :
                    alt10 = 1


                if alt10 == 1:
                    # psf.g:113:16: WS
                    self.mWS()



                else:
                    break #loop10


            # psf.g:113:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )
            alt11 = 6
            LA11_0 = self.input.LA(1)

            if (LA11_0 == u'I') :
                LA11_1 = self.input.LA(2)

                if (LA11_1 == u'N') :
                    LA11_3 = self.input.LA(3)

                    if (LA11_3 == u'T') :
                        LA11_7 = self.input.LA(4)

                        if (LA11_7 == u'E') :
                            alt11 = 5
                        else:
                            alt11 = 3
                    else:
                        nvae = NoViableAltException("113:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )", 11, 3, self.input)

                        raise nvae

                else:
                    alt11 = 1
            elif (LA11_0 == u'i') :
                LA11_2 = self.input.LA(2)

                if (LA11_2 == u'n') :
                    LA11_5 = self.input.LA(3)

                    if (LA11_5 == u't') :
                        LA11_8 = self.input.LA(4)

                        if (LA11_8 == u'e') :
                            alt11 = 6
                        else:
                            alt11 = 4
                    else:
                        nvae = NoViableAltException("113:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )", 11, 5, self.input)

                        raise nvae

                else:
                    alt11 = 2
            else:
                nvae = NoViableAltException("113:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )", 11, 0, self.input)

                raise nvae

            if alt11 == 1:
                # psf.g:113:21: 'I'
                self.match(u'I')



            elif alt11 == 2:
                # psf.g:113:25: 'i'
                self.match(u'i')



            elif alt11 == 3:
                # psf.g:113:29: 'INT'
                self.match("INT")




            elif alt11 == 4:
                # psf.g:113:35: 'int'
                self.match("int")




            elif alt11 == 5:
                # psf.g:113:41: 'INTERJECTION'
                self.match("INTERJECTION")




            elif alt11 == 6:
                # psf.g:113:56: 'interjection'
                self.match("interjection")









        finally:

            pass

    # $ANTLR end INTTAG



    # $ANTLR start DOLLARTOKEN
    def mDOLLARTOKEN(self, ):

        try:
            self.type = DOLLARTOKEN

            # psf.g:116:2: ( '$' ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )* )
            # psf.g:116:4: '$' ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )*
            self.match(u'$')

            if (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # psf.g:116:30: ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )*
            while True: #loop12
                alt12 = 2
                LA12_0 = self.input.LA(1)

                if ((u'0' <= LA12_0 <= u'9') or (u'A' <= LA12_0 <= u'Z') or LA12_0 == u'_' or (u'a' <= LA12_0 <= u'z')) :
                    alt12 = 1


                if alt12 == 1:
                    # psf.g:
                    if (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop12






        finally:

            pass

    # $ANTLR end DOLLARTOKEN



    # $ANTLR start TOKEN
    def mTOKEN(self, ):

        try:
            self.type = TOKEN

            # psf.g:118:9: ( (~ ( NL | WS | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW ) )+ )
            # psf.g:118:11: (~ ( NL | WS | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW ) )+
            # psf.g:118:11: (~ ( NL | WS | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW ) )+
            cnt13 = 0
            while True: #loop13
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if ((u'\u0000' <= LA13_0 <= u'\b') or (u'\u000E' <= LA13_0 <= u'\u001F') or (u'!' <= LA13_0 <= u'\'') or (u'*' <= LA13_0 <= u';') or LA13_0 == u'=' or (u'?' <= LA13_0 <= u'Z') or LA13_0 == u'\\' or (u'^' <= LA13_0 <= u'z') or LA13_0 == u'|' or (u'~' <= LA13_0 <= u'\u009F') or (u'\u00A1' <= LA13_0 <= u'\u167F') or (u'\u1681' <= LA13_0 <= u'\u1FFF') or (u'\u200C' <= LA13_0 <= u'\u2027') or (u'\u202A' <= LA13_0 <= u'\u202E') or (u'\u2030' <= LA13_0 <= u'\u2FFF') or (u'\u3001' <= LA13_0 <= u'\uFFFE')) :
                    alt13 = 1


                if alt13 == 1:
                    # psf.g:118:11: ~ ( NL | WS | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW )
                    if (u'\u0000' <= self.input.LA(1) <= u'\b') or (u'\u000E' <= self.input.LA(1) <= u'\u001F') or (u'!' <= self.input.LA(1) <= u'\'') or (u'*' <= self.input.LA(1) <= u';') or self.input.LA(1) == u'=' or (u'?' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'\\' or (u'^' <= self.input.LA(1) <= u'z') or self.input.LA(1) == u'|' or (u'~' <= self.input.LA(1) <= u'\u009F') or (u'\u00A1' <= self.input.LA(1) <= u'\u167F') or (u'\u1681' <= self.input.LA(1) <= u'\u1FFF') or (u'\u200C' <= self.input.LA(1) <= u'\u2027') or (u'\u202A' <= self.input.LA(1) <= u'\u202E') or (u'\u2030' <= self.input.LA(1) <= u'\u2FFF') or (u'\u3001' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt13 >= 1:
                        break #loop13

                    eee = EarlyExitException(13, self.input)
                    raise eee

                cnt13 += 1






        finally:

            pass

    # $ANTLR end TOKEN



    def mTokens(self):
        # psf.g:1:8: ( LSB | RSB | LCB | RCB | LRB | RRB | DCOLON | RARROW | LARROW | COMMENT | EATWS | EQ | NEWLINE | VOCTAG | INTTAG | DOLLARTOKEN | TOKEN )
        alt14 = 17
        alt14 = self.dfa14.predict(self.input)
        if alt14 == 1:
            # psf.g:1:10: LSB
            self.mLSB()



        elif alt14 == 2:
            # psf.g:1:14: RSB
            self.mRSB()



        elif alt14 == 3:
            # psf.g:1:18: LCB
            self.mLCB()



        elif alt14 == 4:
            # psf.g:1:22: RCB
            self.mRCB()



        elif alt14 == 5:
            # psf.g:1:26: LRB
            self.mLRB()



        elif alt14 == 6:
            # psf.g:1:30: RRB
            self.mRRB()



        elif alt14 == 7:
            # psf.g:1:34: DCOLON
            self.mDCOLON()



        elif alt14 == 8:
            # psf.g:1:41: RARROW
            self.mRARROW()



        elif alt14 == 9:
            # psf.g:1:48: LARROW
            self.mLARROW()



        elif alt14 == 10:
            # psf.g:1:55: COMMENT
            self.mCOMMENT()



        elif alt14 == 11:
            # psf.g:1:63: EATWS
            self.mEATWS()



        elif alt14 == 12:
            # psf.g:1:69: EQ
            self.mEQ()



        elif alt14 == 13:
            # psf.g:1:72: NEWLINE
            self.mNEWLINE()



        elif alt14 == 14:
            # psf.g:1:80: VOCTAG
            self.mVOCTAG()



        elif alt14 == 15:
            # psf.g:1:87: INTTAG
            self.mINTTAG()



        elif alt14 == 16:
            # psf.g:1:94: DOLLARTOKEN
            self.mDOLLARTOKEN()



        elif alt14 == 17:
            # psf.g:1:106: TOKEN
            self.mTOKEN()








    # lookup tables for DFA #14

    DFA14_eot = DFA.unpack(
        u"\7\uffff\1\21\1\uffff\1\21\1\uffff\1\21\1\uffff\1\24\1\uffff\2"
        u"\21\1\uffff\1\33\1\34\1\uffff\1\37\1\uffff\1\37\2\40\1\44\2\uffff"
        u"\1\34\1\21\2\uffff\3\21\1\uffff\1\44\2\37\2\40\22\21\2\40\6\21"
        u"\2\37"
        )

    DFA14_eof = DFA.unpack(
        u"\106\uffff"
        )

    DFA14_min = DFA.unpack(
        u"\1\0\6\uffff\1\72\1\uffff\1\55\1\uffff\1\57\1\uffff\1\0\1\uffff"
        u"\1\11\1\101\1\uffff\2\0\1\uffff\1\0\1\11\4\0\2\uffff\1\0\1\124"
        u"\2\uffff\1\164\1\103\1\143\1\uffff\5\0\1\122\1\162\1\124\1\164"
        u"\1\112\1\152\1\111\1\151\1\105\1\145\1\126\1\166\1\103\1\143\1"
        u"\105\1\145\1\124\1\164\2\0\1\111\1\151\1\117\1\157\1\116\1\156"
        u"\2\0"
        )

    DFA14_max = DFA.unpack(
        u"\1\ufffe\6\uffff\1\72\1\uffff\1\76\1\uffff\1\57\1\uffff\1\ufffe"
        u"\1\uffff\1\u3000\1\172\1\uffff\2\ufffe\1\uffff\1\ufffe\1\u3000"
        u"\4\ufffe\2\uffff\1\ufffe\1\124\2\uffff\1\164\1\103\1\143\1\uffff"
        u"\5\ufffe\1\122\1\162\1\124\1\164\1\112\1\152\1\111\1\151\1\105"
        u"\1\145\1\126\1\166\1\103\1\143\1\105\1\145\1\124\1\164\2\ufffe"
        u"\1\111\1\151\1\117\1\157\1\116\1\156\2\ufffe"
        )

    DFA14_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\1\3\1\4\1\5\1\6\1\uffff\1\10\1\uffff\1\11\1\uffff"
        u"\1\13\1\uffff\1\15\2\uffff\1\21\2\uffff\1\14\6\uffff\1\7\1\12\2"
        u"\uffff\1\17\1\16\3\uffff\1\20\41\uffff"
        )

    DFA14_special = DFA.unpack(
        u"\106\uffff"
        )

            
    DFA14_transition = [
        DFA.unpack(u"\11\21\1\14\1\16\2\14\1\16\22\21\1\14\3\21\1\20\3\21"
        u"\1\5\1\6\3\21\1\11\1\21\1\13\12\21\1\7\1\21\1\12\1\15\1\10\34\21"
        u"\1\1\1\17\1\2\35\21\1\3\1\21\1\4\42\21\1\14\u15df\21\1\14\u097f"
        u"\21\14\14\34\21\2\16\5\21\1\14\u0fd0\21\1\14\ucffe\21"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\11\20\uffff\1\10"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\23"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\35\21\1\uffff\1\21\1\uffff"
        u"\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff\34\21\2\uffff"
        u"\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\26\1\uffff\2\26\23\uffff\1\26\50\uffff\1\25\14\uffff"
        u"\1\30\22\uffff\1\27\14\uffff\1\31\51\uffff\1\26\u15df\uffff\1\26"
        u"\u097f\uffff\14\26\43\uffff\1\26\u0fd0\uffff\1\26"),
        DFA.unpack(u"\32\32\4\uffff\1\32\1\uffff\32\32"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\35\21\1\uffff\1\21\1\uffff"
        u"\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff\34\21\2\uffff"
        u"\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\35\5\uffff\22\35\1\uffff\7\35\2\uffff\22\35\1\uffff"
        u"\1\35\1\uffff\34\35\1\uffff\1\35\1\uffff\35\35\1\uffff\1\35\1\uffff"
        u"\42\35\1\uffff\u15df\35\1\uffff\u097f\35\14\uffff\34\35\2\uffff"
        u"\5\35\1\uffff\u0fd0\35\1\uffff\ucffe\35"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\17\21\1\36\14\21\1\uffff\1\21\1\uffff\35\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\1\26\1\uffff\2\26\23\uffff\1\26\50\uffff\1\37\14\uffff"
        u"\1\40\22\uffff\1\37\14\uffff\1\40\51\uffff\1\26\u15df\uffff\1\26"
        u"\u097f\uffff\14\26\43\uffff\1\26\u0fd0\uffff\1\26"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\20\21\1\41\14\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\20\21\1\42\13\21\1\uffff\1\21\1\uffff\35\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\21\21\1\43\13\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\6\21\12\45"
        u"\2\21\1\uffff\1\21\1\uffff\2\21\32\45\1\uffff\1\21\1\uffff\1\21"
        u"\1\45\1\21\32\45\1\uffff\1\21\1\uffff\42\21\1\uffff\u15df\21\1"
        u"\uffff\u097f\21\14\uffff\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1"
        u"\uffff\ucffe\21"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\11\35\5\uffff\22\35\1\uffff\7\35\2\uffff\22\35\1\uffff"
        u"\1\35\1\uffff\34\35\1\uffff\1\35\1\uffff\35\35\1\uffff\1\35\1\uffff"
        u"\42\35\1\uffff\u15df\35\1\uffff\u097f\35\14\uffff\34\35\2\uffff"
        u"\5\35\1\uffff\u0fd0\35\1\uffff\ucffe\35"),
        DFA.unpack(u"\1\46"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\47"),
        DFA.unpack(u"\1\50"),
        DFA.unpack(u"\1\51"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\6\21\12\45"
        u"\2\21\1\uffff\1\21\1\uffff\2\21\32\45\1\uffff\1\21\1\uffff\1\21"
        u"\1\45\1\21\32\45\1\uffff\1\21\1\uffff\42\21\1\uffff\u15df\21\1"
        u"\uffff\u097f\21\14\uffff\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1"
        u"\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\6\21\1\52\25\21\1\uffff\1\21\1\uffff\35\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\7\21\1\53\25\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\2\21\1\54\31\21\1\uffff\1\21\1\uffff\35\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\3\21\1\55\31\21\1\uffff"
        u"\1\21\1\uffff\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff"
        u"\34\21\2\uffff\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\1\56"),
        DFA.unpack(u"\1\57"),
        DFA.unpack(u"\1\60"),
        DFA.unpack(u"\1\61"),
        DFA.unpack(u"\1\62"),
        DFA.unpack(u"\1\63"),
        DFA.unpack(u"\1\64"),
        DFA.unpack(u"\1\65"),
        DFA.unpack(u"\1\66"),
        DFA.unpack(u"\1\67"),
        DFA.unpack(u"\1\70"),
        DFA.unpack(u"\1\71"),
        DFA.unpack(u"\1\72"),
        DFA.unpack(u"\1\73"),
        DFA.unpack(u"\1\74"),
        DFA.unpack(u"\1\75"),
        DFA.unpack(u"\1\76"),
        DFA.unpack(u"\1\77"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\35\21\1\uffff\1\21\1\uffff"
        u"\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff\34\21\2\uffff"
        u"\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\35\21\1\uffff\1\21\1\uffff"
        u"\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff\34\21\2\uffff"
        u"\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\1\100"),
        DFA.unpack(u"\1\101"),
        DFA.unpack(u"\1\102"),
        DFA.unpack(u"\1\103"),
        DFA.unpack(u"\1\104"),
        DFA.unpack(u"\1\105"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\35\21\1\uffff\1\21\1\uffff"
        u"\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff\34\21\2\uffff"
        u"\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21"),
        DFA.unpack(u"\11\21\5\uffff\22\21\1\uffff\7\21\2\uffff\22\21\1\uffff"
        u"\1\21\1\uffff\34\21\1\uffff\1\21\1\uffff\35\21\1\uffff\1\21\1\uffff"
        u"\42\21\1\uffff\u15df\21\1\uffff\u097f\21\14\uffff\34\21\2\uffff"
        u"\5\21\1\uffff\u0fd0\21\1\uffff\ucffe\21")
    ]

    # class definition for DFA #14

    DFA14 = DFA
 

