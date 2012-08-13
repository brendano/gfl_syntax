# $ANTLR 3.0.1 psf.g 2012-08-13 16:03:20

from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
SLARROW=20
RRB=12
RARROW=7
HEAD=11
LARROW=6
LRB=10
RCB=15
Tokens=27
EOF=-1
EATWS=25
SRARROW=21
TOKEN=13
USP=26
DCOLON=9
WS=24
NEWLINE=4
LCB=14
DOLLARTOKEN=8
RSB=17
NL=22
VOCTAG=18
EQ=5
COMMENT=23
INTTAG=19
LSB=16

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






    # $ANTLR start HEAD
    def mHEAD(self, ):

        try:
            self.type = HEAD

            # psf.g:57:6: ( '*' )
            # psf.g:57:8: '*'
            self.match(u'*')





        finally:

            pass

    # $ANTLR end HEAD



    # $ANTLR start LSB
    def mLSB(self, ):

        try:
            self.type = LSB

            # psf.g:59:6: ( '[' )
            # psf.g:59:9: '['
            self.match(u'[')





        finally:

            pass

    # $ANTLR end LSB



    # $ANTLR start RSB
    def mRSB(self, ):

        try:
            self.type = RSB

            # psf.g:60:6: ( ']' )
            # psf.g:60:9: ']'
            self.match(u']')





        finally:

            pass

    # $ANTLR end RSB



    # $ANTLR start LCB
    def mLCB(self, ):

        try:
            self.type = LCB

            # psf.g:62:6: ( '{' )
            # psf.g:62:9: '{'
            self.match(u'{')





        finally:

            pass

    # $ANTLR end LCB



    # $ANTLR start RCB
    def mRCB(self, ):

        try:
            self.type = RCB

            # psf.g:63:6: ( '}' )
            # psf.g:63:9: '}'
            self.match(u'}')





        finally:

            pass

    # $ANTLR end RCB



    # $ANTLR start LRB
    def mLRB(self, ):

        try:
            self.type = LRB

            # psf.g:65:6: ( '(' )
            # psf.g:65:9: '('
            self.match(u'(')





        finally:

            pass

    # $ANTLR end LRB



    # $ANTLR start RRB
    def mRRB(self, ):

        try:
            self.type = RRB

            # psf.g:66:6: ( ')' )
            # psf.g:66:9: ')'
            self.match(u')')





        finally:

            pass

    # $ANTLR end RRB



    # $ANTLR start DCOLON
    def mDCOLON(self, ):

        try:
            self.type = DCOLON

            # psf.g:68:8: ( '::' )
            # psf.g:68:10: '::'
            self.match("::")






        finally:

            pass

    # $ANTLR end DCOLON



    # $ANTLR start SLARROW
    def mSLARROW(self, ):

        try:
            # psf.g:70:17: ( ( '<' ) )
            # psf.g:70:19: ( '<' )
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
            # psf.g:71:17: ( ( '>' ) )
            # psf.g:71:19: ( '>' )
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

            # psf.g:73:8: ( ( SRARROW | ( '-' )+ '>' ) )
            # psf.g:73:10: ( SRARROW | ( '-' )+ '>' )
            # psf.g:73:10: ( SRARROW | ( '-' )+ '>' )
            alt2 = 2
            LA2_0 = self.input.LA(1)

            if (LA2_0 == u'>') :
                alt2 = 1
            elif (LA2_0 == u'-') :
                alt2 = 2
            else:
                nvae = NoViableAltException("73:10: ( SRARROW | ( '-' )+ '>' )", 2, 0, self.input)

                raise nvae

            if alt2 == 1:
                # psf.g:73:11: SRARROW
                self.mSRARROW()



            elif alt2 == 2:
                # psf.g:73:19: ( '-' )+ '>'
                # psf.g:73:19: ( '-' )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == u'-') :
                        alt1 = 1


                    if alt1 == 1:
                        # psf.g:73:19: '-'
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

            # psf.g:74:8: ( ( SLARROW | '<' ( '-' )+ ) )
            # psf.g:74:10: ( SLARROW | '<' ( '-' )+ )
            # psf.g:74:10: ( SLARROW | '<' ( '-' )+ )
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == u'<') :
                LA4_1 = self.input.LA(2)

                if (LA4_1 == u'-') :
                    alt4 = 2
                else:
                    alt4 = 1
            else:
                nvae = NoViableAltException("74:10: ( SLARROW | '<' ( '-' )+ )", 4, 0, self.input)

                raise nvae

            if alt4 == 1:
                # psf.g:74:11: SLARROW
                self.mSLARROW()



            elif alt4 == 2:
                # psf.g:74:19: '<' ( '-' )+
                self.match(u'<')

                # psf.g:74:22: ( '-' )+
                cnt3 = 0
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == u'-') :
                        alt3 = 1


                    if alt3 == 1:
                        # psf.g:74:22: '-'
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

            # psf.g:77:9: ( '//' (~ ( NL ) )* )
            # psf.g:77:11: '//' (~ ( NL ) )*
            self.match("//")


            # psf.g:77:16: (~ ( NL ) )*
            while True: #loop5
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if ((u'\u0000' <= LA5_0 <= u'\t') or (u'\u000B' <= LA5_0 <= u'\f') or (u'\u000E' <= LA5_0 <= u'\u2027') or (u'\u202A' <= LA5_0 <= u'\uFFFE')) :
                    alt5 = 1


                if alt5 == 1:
                    # psf.g:77:16: ~ ( NL )
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

            # psf.g:80:8: ( ( WS )+ )
            # psf.g:80:10: ( WS )+
            # psf.g:80:10: ( WS )+
            cnt6 = 0
            while True: #loop6
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == u'\t' or (u'\u000B' <= LA6_0 <= u'\f') or LA6_0 == u' ' or LA6_0 == u'\u00A0' or LA6_0 == u'\u1680' or (u'\u2000' <= LA6_0 <= u'\u200B') or LA6_0 == u'\u202F' or LA6_0 == u'\u3000') :
                    alt6 = 1


                if alt6 == 1:
                    # psf.g:80:11: WS
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
            # psf.g:82:12: ( ( '\\u0009' | '\\u000b' | '\\u000c' | '\\u0020' | '\\u00a0' | USP ) )
            # psf.g:82:14: ( '\\u0009' | '\\u000b' | '\\u000c' | '\\u0020' | '\\u00a0' | USP )
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

            # psf.g:89:4: ( '=' )
            # psf.g:89:6: '='
            self.match(u'=')





        finally:

            pass

    # $ANTLR end EQ



    # $ANTLR start NEWLINE
    def mNEWLINE(self, ):

        try:
            self.type = NEWLINE

            # psf.g:91:9: ( ( NL )+ )
            # psf.g:91:11: ( NL )+
            # psf.g:91:11: ( NL )+
            cnt7 = 0
            while True: #loop7
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == u'\n' or LA7_0 == u'\r' or (u'\u2028' <= LA7_0 <= u'\u2029')) :
                    alt7 = 1


                if alt7 == 1:
                    # psf.g:91:12: NL
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
            # psf.g:93:13: ( ( '\\u000a' | '\\u000d' | '\\u2028' | '\\u2029' ) )
            # psf.g:93:15: ( '\\u000a' | '\\u000d' | '\\u2028' | '\\u2029' )
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
            # psf.g:95:13: ( '\\u1680' | '\\u2000' | '\\u2001' | '\\u2002' | '\\u2003' | '\\u2004' | '\\u2005' | '\\u2006' | '\\u2007' | '\\u2008' | '\\u2009' | '\\u200A' | '\\u200B' | '\\u202F' | '\\u3000' )
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

            # psf.g:113:9: ( '\\\\' ( WS )* ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' ) )
            # psf.g:113:11: '\\\\' ( WS )* ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )
            self.match(u'\\')

            # psf.g:113:16: ( WS )*
            while True: #loop8
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == u'\t' or (u'\u000B' <= LA8_0 <= u'\f') or LA8_0 == u' ' or LA8_0 == u'\u00A0' or LA8_0 == u'\u1680' or (u'\u2000' <= LA8_0 <= u'\u200B') or LA8_0 == u'\u202F' or LA8_0 == u'\u3000') :
                    alt8 = 1


                if alt8 == 1:
                    # psf.g:113:16: WS
                    self.mWS()



                else:
                    break #loop8


            # psf.g:113:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )
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
                        nvae = NoViableAltException("113:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )", 9, 3, self.input)

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
                        nvae = NoViableAltException("113:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )", 9, 5, self.input)

                        raise nvae

                else:
                    alt9 = 2
            else:
                nvae = NoViableAltException("113:20: ( 'V' | 'v' | 'VOC' | 'voc' | 'VOCATIVE' | 'vocative' )", 9, 0, self.input)

                raise nvae

            if alt9 == 1:
                # psf.g:113:21: 'V'
                self.match(u'V')



            elif alt9 == 2:
                # psf.g:113:25: 'v'
                self.match(u'v')



            elif alt9 == 3:
                # psf.g:113:29: 'VOC'
                self.match("VOC")




            elif alt9 == 4:
                # psf.g:113:35: 'voc'
                self.match("voc")




            elif alt9 == 5:
                # psf.g:113:41: 'VOCATIVE'
                self.match("VOCATIVE")




            elif alt9 == 6:
                # psf.g:113:52: 'vocative'
                self.match("vocative")









        finally:

            pass

    # $ANTLR end VOCTAG



    # $ANTLR start INTTAG
    def mINTTAG(self, ):

        try:
            self.type = INTTAG

            # psf.g:115:9: ( '\\\\' ( WS )* ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' ) )
            # psf.g:115:11: '\\\\' ( WS )* ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )
            self.match(u'\\')

            # psf.g:115:16: ( WS )*
            while True: #loop10
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == u'\t' or (u'\u000B' <= LA10_0 <= u'\f') or LA10_0 == u' ' or LA10_0 == u'\u00A0' or LA10_0 == u'\u1680' or (u'\u2000' <= LA10_0 <= u'\u200B') or LA10_0 == u'\u202F' or LA10_0 == u'\u3000') :
                    alt10 = 1


                if alt10 == 1:
                    # psf.g:115:16: WS
                    self.mWS()



                else:
                    break #loop10


            # psf.g:115:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )
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
                        nvae = NoViableAltException("115:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )", 11, 3, self.input)

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
                        nvae = NoViableAltException("115:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )", 11, 5, self.input)

                        raise nvae

                else:
                    alt11 = 2
            else:
                nvae = NoViableAltException("115:20: ( 'I' | 'i' | 'INT' | 'int' | 'INTERJECTION' | 'interjection' )", 11, 0, self.input)

                raise nvae

            if alt11 == 1:
                # psf.g:115:21: 'I'
                self.match(u'I')



            elif alt11 == 2:
                # psf.g:115:25: 'i'
                self.match(u'i')



            elif alt11 == 3:
                # psf.g:115:29: 'INT'
                self.match("INT")




            elif alt11 == 4:
                # psf.g:115:35: 'int'
                self.match("int")




            elif alt11 == 5:
                # psf.g:115:41: 'INTERJECTION'
                self.match("INTERJECTION")




            elif alt11 == 6:
                # psf.g:115:56: 'interjection'
                self.match("interjection")









        finally:

            pass

    # $ANTLR end INTTAG



    # $ANTLR start DOLLARTOKEN
    def mDOLLARTOKEN(self, ):

        try:
            self.type = DOLLARTOKEN

            # psf.g:118:2: ( '$' ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )* )
            # psf.g:118:4: '$' ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )*
            self.match(u'$')

            if (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # psf.g:118:30: ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )*
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

            # psf.g:120:9: ( (~ ( NL | WS | HEAD | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW ) )+ )
            # psf.g:120:11: (~ ( NL | WS | HEAD | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW ) )+
            # psf.g:120:11: (~ ( NL | WS | HEAD | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW ) )+
            cnt13 = 0
            while True: #loop13
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if ((u'\u0000' <= LA13_0 <= u'\b') or (u'\u000E' <= LA13_0 <= u'\u001F') or (u'!' <= LA13_0 <= u'\'') or (u'+' <= LA13_0 <= u';') or LA13_0 == u'=' or (u'?' <= LA13_0 <= u'Z') or LA13_0 == u'\\' or (u'^' <= LA13_0 <= u'z') or LA13_0 == u'|' or (u'~' <= LA13_0 <= u'\u009F') or (u'\u00A1' <= LA13_0 <= u'\u167F') or (u'\u1681' <= LA13_0 <= u'\u1FFF') or (u'\u200C' <= LA13_0 <= u'\u2027') or (u'\u202A' <= LA13_0 <= u'\u202E') or (u'\u2030' <= LA13_0 <= u'\u2FFF') or (u'\u3001' <= LA13_0 <= u'\uFFFE')) :
                    alt13 = 1


                if alt13 == 1:
                    # psf.g:120:11: ~ ( NL | WS | HEAD | RCB | RRB | RSB | LCB | LRB | LSB | SRARROW | SLARROW )
                    if (u'\u0000' <= self.input.LA(1) <= u'\b') or (u'\u000E' <= self.input.LA(1) <= u'\u001F') or (u'!' <= self.input.LA(1) <= u'\'') or (u'+' <= self.input.LA(1) <= u';') or self.input.LA(1) == u'=' or (u'?' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'\\' or (u'^' <= self.input.LA(1) <= u'z') or self.input.LA(1) == u'|' or (u'~' <= self.input.LA(1) <= u'\u009F') or (u'\u00A1' <= self.input.LA(1) <= u'\u167F') or (u'\u1681' <= self.input.LA(1) <= u'\u1FFF') or (u'\u200C' <= self.input.LA(1) <= u'\u2027') or (u'\u202A' <= self.input.LA(1) <= u'\u202E') or (u'\u2030' <= self.input.LA(1) <= u'\u2FFF') or (u'\u3001' <= self.input.LA(1) <= u'\uFFFE'):
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
        # psf.g:1:8: ( HEAD | LSB | RSB | LCB | RCB | LRB | RRB | DCOLON | RARROW | LARROW | COMMENT | EATWS | EQ | NEWLINE | VOCTAG | INTTAG | DOLLARTOKEN | TOKEN )
        alt14 = 18
        alt14 = self.dfa14.predict(self.input)
        if alt14 == 1:
            # psf.g:1:10: HEAD
            self.mHEAD()



        elif alt14 == 2:
            # psf.g:1:15: LSB
            self.mLSB()



        elif alt14 == 3:
            # psf.g:1:19: RSB
            self.mRSB()



        elif alt14 == 4:
            # psf.g:1:23: LCB
            self.mLCB()



        elif alt14 == 5:
            # psf.g:1:27: RCB
            self.mRCB()



        elif alt14 == 6:
            # psf.g:1:31: LRB
            self.mLRB()



        elif alt14 == 7:
            # psf.g:1:35: RRB
            self.mRRB()



        elif alt14 == 8:
            # psf.g:1:39: DCOLON
            self.mDCOLON()



        elif alt14 == 9:
            # psf.g:1:46: RARROW
            self.mRARROW()



        elif alt14 == 10:
            # psf.g:1:53: LARROW
            self.mLARROW()



        elif alt14 == 11:
            # psf.g:1:60: COMMENT
            self.mCOMMENT()



        elif alt14 == 12:
            # psf.g:1:68: EATWS
            self.mEATWS()



        elif alt14 == 13:
            # psf.g:1:74: EQ
            self.mEQ()



        elif alt14 == 14:
            # psf.g:1:77: NEWLINE
            self.mNEWLINE()



        elif alt14 == 15:
            # psf.g:1:85: VOCTAG
            self.mVOCTAG()



        elif alt14 == 16:
            # psf.g:1:92: INTTAG
            self.mINTTAG()



        elif alt14 == 17:
            # psf.g:1:99: DOLLARTOKEN
            self.mDOLLARTOKEN()



        elif alt14 == 18:
            # psf.g:1:111: TOKEN
            self.mTOKEN()








    # lookup tables for DFA #14

    DFA14_eot = DFA.unpack(
        u"\10\uffff\1\22\1\uffff\1\22\1\uffff\1\22\1\uffff\1\25\1\uffff\2"
        u"\22\1\uffff\1\34\1\36\2\uffff\2\40\2\37\1\46\1\uffff\1\36\3\uffff"
        u"\4\22\1\46\1\uffff\2\40\2\37\20\22\2\40\10\22\2\37"
        )

    DFA14_eof = DFA.unpack(
        u"\107\uffff"
        )

    DFA14_min = DFA.unpack(
        u"\1\0\7\uffff\1\72\1\uffff\1\55\1\uffff\1\57\1\uffff\1\0\1\uffff"
        u"\1\11\1\101\1\uffff\2\0\1\uffff\1\11\5\0\1\uffff\1\0\3\uffff\1"
        u"\103\1\143\1\124\1\164\1\0\1\uffff\4\0\1\124\1\164\1\122\1\162"
        u"\1\111\1\151\1\112\1\152\1\126\1\166\1\105\1\145\1\105\1\145\1"
        u"\103\1\143\2\0\1\124\1\164\1\111\1\151\1\117\1\157\1\116\1\156"
        u"\2\0"
        )

    DFA14_max = DFA.unpack(
        u"\1\ufffe\7\uffff\1\72\1\uffff\1\76\1\uffff\1\57\1\uffff\1\ufffe"
        u"\1\uffff\1\u3000\1\172\1\uffff\2\ufffe\1\uffff\1\u3000\5\ufffe"
        u"\1\uffff\1\ufffe\3\uffff\1\103\1\143\1\124\1\164\1\ufffe\1\uffff"
        u"\4\ufffe\1\124\1\164\1\122\1\162\1\111\1\151\1\112\1\152\1\126"
        u"\1\166\1\105\1\145\1\105\1\145\1\103\1\143\2\ufffe\1\124\1\164"
        u"\1\111\1\151\1\117\1\157\1\116\1\156\2\ufffe"
        )

    DFA14_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\1\3\1\4\1\5\1\6\1\7\1\uffff\1\11\1\uffff\1\12"
        u"\1\uffff\1\14\1\uffff\1\16\2\uffff\1\22\2\uffff\1\15\6\uffff\1"
        u"\10\1\uffff\1\13\1\20\1\17\5\uffff\1\21\40\uffff"
        )

    DFA14_special = DFA.unpack(
        u"\107\uffff"
        )

            
    DFA14_transition = [
        DFA.unpack(u"\11\22\1\15\1\17\2\15\1\17\22\22\1\15\3\22\1\21\3\22"
        u"\1\6\1\7\1\1\2\22\1\12\1\22\1\14\12\22\1\10\1\22\1\13\1\16\1\11"
        u"\34\22\1\2\1\20\1\3\35\22\1\4\1\22\1\5\42\22\1\15\u15df\22\1\15"
        u"\u097f\22\14\15\34\22\2\17\5\22\1\15\u0fd0\22\1\15\ucffe\22"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\23"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\12\20\uffff\1\11"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\24"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\35\22\1\uffff\1\22\1\uffff"
        u"\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff\34\22\2\uffff"
        u"\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\26\1\uffff\2\26\23\uffff\1\26\50\uffff\1\31\14\uffff"
        u"\1\27\22\uffff\1\32\14\uffff\1\30\51\uffff\1\26\u15df\uffff\1\26"
        u"\u097f\uffff\14\26\43\uffff\1\26\u0fd0\uffff\1\26"),
        DFA.unpack(u"\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\35\22\1\uffff\1\22\1\uffff"
        u"\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff\34\22\2\uffff"
        u"\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\35\5\uffff\22\35\1\uffff\7\35\3\uffff\21\35\1\uffff"
        u"\1\35\1\uffff\34\35\1\uffff\1\35\1\uffff\35\35\1\uffff\1\35\1\uffff"
        u"\42\35\1\uffff\u15df\35\1\uffff\u097f\35\14\uffff\34\35\2\uffff"
        u"\5\35\1\uffff\u0fd0\35\1\uffff\ucffe\35"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\26\1\uffff\2\26\23\uffff\1\26\50\uffff\1\37\14\uffff"
        u"\1\40\22\uffff\1\37\14\uffff\1\40\51\uffff\1\26\u15df\uffff\1\26"
        u"\u097f\uffff\14\26\43\uffff\1\26\u0fd0\uffff\1\26"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\20\22\1\41\13\22\1\uffff\1\22\1\uffff\35\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\21\22\1\42\13\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\17\22\1\43\14\22\1\uffff\1\22\1\uffff\35\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\20\22\1\44\14\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\5\22\12\45"
        u"\2\22\1\uffff\1\22\1\uffff\2\22\32\45\1\uffff\1\22\1\uffff\1\22"
        u"\1\45\1\22\32\45\1\uffff\1\22\1\uffff\42\22\1\uffff\u15df\22\1"
        u"\uffff\u097f\22\14\uffff\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1"
        u"\uffff\ucffe\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\35\5\uffff\22\35\1\uffff\7\35\3\uffff\21\35\1\uffff"
        u"\1\35\1\uffff\34\35\1\uffff\1\35\1\uffff\35\35\1\uffff\1\35\1\uffff"
        u"\42\35\1\uffff\u15df\35\1\uffff\u097f\35\14\uffff\34\35\2\uffff"
        u"\5\35\1\uffff\u0fd0\35\1\uffff\ucffe\35"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\47"),
        DFA.unpack(u"\1\50"),
        DFA.unpack(u"\1\51"),
        DFA.unpack(u"\1\52"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\5\22\12\45"
        u"\2\22\1\uffff\1\22\1\uffff\2\22\32\45\1\uffff\1\22\1\uffff\1\22"
        u"\1\45\1\22\32\45\1\uffff\1\22\1\uffff\42\22\1\uffff\u15df\22\1"
        u"\uffff\u097f\22\14\uffff\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1"
        u"\uffff\ucffe\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\2\22\1\53\31\22\1\uffff\1\22\1\uffff\35\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\3\22\1\54\31\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\6\22\1\55\25\22\1\uffff\1\22\1\uffff\35\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\7\22\1\56\25\22\1\uffff"
        u"\1\22\1\uffff\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff"
        u"\34\22\2\uffff\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
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
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\35\22\1\uffff\1\22\1\uffff"
        u"\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff\34\22\2\uffff"
        u"\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\35\22\1\uffff\1\22\1\uffff"
        u"\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff\34\22\2\uffff"
        u"\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\1\77"),
        DFA.unpack(u"\1\100"),
        DFA.unpack(u"\1\101"),
        DFA.unpack(u"\1\102"),
        DFA.unpack(u"\1\103"),
        DFA.unpack(u"\1\104"),
        DFA.unpack(u"\1\105"),
        DFA.unpack(u"\1\106"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\35\22\1\uffff\1\22\1\uffff"
        u"\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff\34\22\2\uffff"
        u"\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22"),
        DFA.unpack(u"\11\22\5\uffff\22\22\1\uffff\7\22\3\uffff\21\22\1\uffff"
        u"\1\22\1\uffff\34\22\1\uffff\1\22\1\uffff\35\22\1\uffff\1\22\1\uffff"
        u"\42\22\1\uffff\u15df\22\1\uffff\u097f\22\14\uffff\34\22\2\uffff"
        u"\5\22\1\uffff\u0fd0\22\1\uffff\ucffe\22")
    ]

    # class definition for DFA #14

    DFA14 = DFA
 

