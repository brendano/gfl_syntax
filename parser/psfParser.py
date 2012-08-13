# $ANTLR 3.0.1 psf.g 2012-08-13 16:03:20

from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *



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
EQ=5
VOCTAG=18
COMMENT=23
LSB=16
INTTAG=19

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "NEWLINE", "EQ", "LARROW", "RARROW", "DOLLARTOKEN", "DCOLON", "LRB", 
    "HEAD", "RRB", "TOKEN", "LCB", "RCB", "LSB", "RSB", "VOCTAG", "INTTAG", 
    "SLARROW", "SRARROW", "NL", "COMMENT", "WS", "EATWS", "USP"
]



class psfParser(Parser):
    grammarFileName = "psf.g"
    tokenNames = tokenNames

    def __init__(self, input):
        Parser.__init__(self, input)
        self.dfa2 = self.DFA2(
            self, 2,
            eot = self.DFA2_eot,
            eof = self.DFA2_eof,
            min = self.DFA2_min,
            max = self.DFA2_max,
            accept = self.DFA2_accept,
            special = self.DFA2_special,
            transition = self.DFA2_transition
            )




                
        self.adaptor = CommonTreeAdaptor()




    class annotate_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start annotate
    # psf.g:8:1: annotate : ( line | NEWLINE )* ;
    def annotate(self, ):

        retval = self.annotate_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NEWLINE2 = None
        line1 = None


        NEWLINE2_tree = None

        try:
            try:
                # psf.g:8:9: ( ( line | NEWLINE )* )
                # psf.g:8:11: ( line | NEWLINE )*
                root_0 = self.adaptor.nil()

                # psf.g:8:11: ( line | NEWLINE )*
                while True: #loop1
                    alt1 = 3
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == DOLLARTOKEN or LA1_0 == LRB or (TOKEN <= LA1_0 <= LCB) or LA1_0 == LSB) :
                        alt1 = 1
                    elif (LA1_0 == NEWLINE) :
                        alt1 = 2


                    if alt1 == 1:
                        # psf.g:8:12: line
                        self.following.append(self.FOLLOW_line_in_annotate35)
                        line1 = self.line()
                        self.following.pop()

                        self.adaptor.addChild(root_0, line1.tree)


                    elif alt1 == 2:
                        # psf.g:8:19: NEWLINE
                        NEWLINE2 = self.input.LT(1)
                        self.match(self.input, NEWLINE, self.FOLLOW_NEWLINE_in_annotate39)


                        NEWLINE2_tree = self.adaptor.createWithPayload(NEWLINE2)
                        self.adaptor.addChild(root_0, NEWLINE2_tree)



                    else:
                        break #loop1





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end annotate

    class line_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start line
    # psf.g:11:1: line : ( tagexpr | expr | conjexpr | corefexpr );
    def line(self, ):

        retval = self.line_return()
        retval.start = self.input.LT(1)

        root_0 = None

        tagexpr3 = None

        expr4 = None

        conjexpr5 = None

        corefexpr6 = None



        try:
            try:
                # psf.g:11:6: ( tagexpr | expr | conjexpr | corefexpr )
                alt2 = 4
                alt2 = self.dfa2.predict(self.input)
                if alt2 == 1:
                    # psf.g:11:8: tagexpr
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_tagexpr_in_line51)
                    tagexpr3 = self.tagexpr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, tagexpr3.tree)


                elif alt2 == 2:
                    # psf.g:12:5: expr
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_expr_in_line57)
                    expr4 = self.expr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, expr4.tree)


                elif alt2 == 3:
                    # psf.g:13:4: conjexpr
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_conjexpr_in_line62)
                    conjexpr5 = self.conjexpr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, conjexpr5.tree)


                elif alt2 == 4:
                    # psf.g:14:4: corefexpr
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_corefexpr_in_line67)
                    corefexpr6 = self.corefexpr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, corefexpr6.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end line

    class corefexpr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start corefexpr
    # psf.g:17:1: corefexpr : narrow EQ narrow ;
    def corefexpr(self, ):

        retval = self.corefexpr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        EQ8 = None
        narrow7 = None

        narrow9 = None


        EQ8_tree = None

        try:
            try:
                # psf.g:17:10: ( narrow EQ narrow )
                # psf.g:18:3: narrow EQ narrow
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_narrow_in_corefexpr78)
                narrow7 = self.narrow()
                self.following.pop()

                self.adaptor.addChild(root_0, narrow7.tree)
                EQ8 = self.input.LT(1)
                self.match(self.input, EQ, self.FOLLOW_EQ_in_corefexpr80)


                EQ8_tree = self.adaptor.createWithPayload(EQ8)
                root_0 = self.adaptor.becomeRoot(EQ8_tree, root_0)
                self.following.append(self.FOLLOW_narrow_in_corefexpr83)
                narrow9 = self.narrow()
                self.following.pop()

                self.adaptor.addChild(root_0, narrow9.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end corefexpr

    class expr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start expr
    # psf.g:24:1: expr : lc ;
    def expr(self, ):

        retval = self.expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        lc10 = None



        try:
            try:
                # psf.g:24:6: ( lc )
                # psf.g:24:8: lc
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_lc_in_expr96)
                lc10 = self.lc()
                self.following.pop()

                self.adaptor.addChild(root_0, lc10.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end expr

    class lc_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start lc
    # psf.g:27:1: lc : rc ( LARROW lc )? ;
    def lc(self, ):

        retval = self.lc_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LARROW12 = None
        rc11 = None

        lc13 = None


        LARROW12_tree = None

        try:
            try:
                # psf.g:27:4: ( rc ( LARROW lc )? )
                # psf.g:27:6: rc ( LARROW lc )?
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_rc_in_lc106)
                rc11 = self.rc()
                self.following.pop()

                self.adaptor.addChild(root_0, rc11.tree)
                # psf.g:27:9: ( LARROW lc )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == LARROW) :
                    alt3 = 1
                if alt3 == 1:
                    # psf.g:27:10: LARROW lc
                    LARROW12 = self.input.LT(1)
                    self.match(self.input, LARROW, self.FOLLOW_LARROW_in_lc109)


                    LARROW12_tree = self.adaptor.createWithPayload(LARROW12)
                    root_0 = self.adaptor.becomeRoot(LARROW12_tree, root_0)
                    self.following.append(self.FOLLOW_lc_in_lc112)
                    lc13 = self.lc()
                    self.following.pop()

                    self.adaptor.addChild(root_0, lc13.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end lc

    class rc_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start rc
    # psf.g:30:1: rc : atom ( RARROW atom )* ;
    def rc(self, ):

        retval = self.rc_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RARROW15 = None
        atom14 = None

        atom16 = None


        RARROW15_tree = None

        try:
            try:
                # psf.g:30:4: ( atom ( RARROW atom )* )
                # psf.g:30:6: atom ( RARROW atom )*
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_atom_in_rc124)
                atom14 = self.atom()
                self.following.pop()

                self.adaptor.addChild(root_0, atom14.tree)
                # psf.g:30:11: ( RARROW atom )*
                while True: #loop4
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == RARROW) :
                        alt4 = 1


                    if alt4 == 1:
                        # psf.g:30:12: RARROW atom
                        RARROW15 = self.input.LT(1)
                        self.match(self.input, RARROW, self.FOLLOW_RARROW_in_rc127)


                        RARROW15_tree = self.adaptor.createWithPayload(RARROW15)
                        root_0 = self.adaptor.becomeRoot(RARROW15_tree, root_0)
                        self.following.append(self.FOLLOW_atom_in_rc130)
                        atom16 = self.atom()
                        self.following.pop()

                        self.adaptor.addChild(root_0, atom16.tree)


                    else:
                        break #loop4





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end rc

    class conjexpr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start conjexpr
    # psf.g:33:1: conjexpr : DOLLARTOKEN DCOLON atom ( DCOLON atom )? ;
    def conjexpr(self, ):

        retval = self.conjexpr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DOLLARTOKEN17 = None
        DCOLON18 = None
        DCOLON20 = None
        atom19 = None

        atom21 = None


        DOLLARTOKEN17_tree = None
        DCOLON18_tree = None
        DCOLON20_tree = None

        try:
            try:
                # psf.g:33:9: ( DOLLARTOKEN DCOLON atom ( DCOLON atom )? )
                # psf.g:33:11: DOLLARTOKEN DCOLON atom ( DCOLON atom )?
                root_0 = self.adaptor.nil()

                DOLLARTOKEN17 = self.input.LT(1)
                self.match(self.input, DOLLARTOKEN, self.FOLLOW_DOLLARTOKEN_in_conjexpr141)


                DOLLARTOKEN17_tree = self.adaptor.createWithPayload(DOLLARTOKEN17)
                self.adaptor.addChild(root_0, DOLLARTOKEN17_tree)

                DCOLON18 = self.input.LT(1)
                self.match(self.input, DCOLON, self.FOLLOW_DCOLON_in_conjexpr143)


                DCOLON18_tree = self.adaptor.createWithPayload(DCOLON18)
                root_0 = self.adaptor.becomeRoot(DCOLON18_tree, root_0)
                self.following.append(self.FOLLOW_atom_in_conjexpr146)
                atom19 = self.atom()
                self.following.pop()

                self.adaptor.addChild(root_0, atom19.tree)
                # psf.g:33:36: ( DCOLON atom )?
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == DCOLON) :
                    alt5 = 1
                if alt5 == 1:
                    # psf.g:33:37: DCOLON atom
                    DCOLON20 = self.input.LT(1)
                    self.match(self.input, DCOLON, self.FOLLOW_DCOLON_in_conjexpr149)

                    self.following.append(self.FOLLOW_atom_in_conjexpr152)
                    atom21 = self.atom()
                    self.following.pop()

                    self.adaptor.addChild(root_0, atom21.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end conjexpr

    class atom_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start atom
    # psf.g:39:1: atom : ( narrow | curlyset | LRB ( expr )+ ( HEAD ( expr )* )? RRB );
    def atom(self, ):

        retval = self.atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LRB24 = None
        HEAD26 = None
        RRB28 = None
        narrow22 = None

        curlyset23 = None

        expr25 = None

        expr27 = None


        LRB24_tree = None
        HEAD26_tree = None
        RRB28_tree = None

        try:
            try:
                # psf.g:39:6: ( narrow | curlyset | LRB ( expr )+ ( HEAD ( expr )* )? RRB )
                alt9 = 3
                LA9 = self.input.LA(1)
                if LA9 == DOLLARTOKEN or LA9 == TOKEN or LA9 == LSB:
                    alt9 = 1
                elif LA9 == LCB:
                    alt9 = 2
                elif LA9 == LRB:
                    alt9 = 3
                else:
                    nvae = NoViableAltException("39:1: atom : ( narrow | curlyset | LRB ( expr )+ ( HEAD ( expr )* )? RRB );", 9, 0, self.input)

                    raise nvae

                if alt9 == 1:
                    # psf.g:39:8: narrow
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_narrow_in_atom167)
                    narrow22 = self.narrow()
                    self.following.pop()

                    self.adaptor.addChild(root_0, narrow22.tree)


                elif alt9 == 2:
                    # psf.g:40:4: curlyset
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_curlyset_in_atom172)
                    curlyset23 = self.curlyset()
                    self.following.pop()

                    self.adaptor.addChild(root_0, curlyset23.tree)


                elif alt9 == 3:
                    # psf.g:41:4: LRB ( expr )+ ( HEAD ( expr )* )? RRB
                    root_0 = self.adaptor.nil()

                    LRB24 = self.input.LT(1)
                    self.match(self.input, LRB, self.FOLLOW_LRB_in_atom177)


                    LRB24_tree = self.adaptor.createWithPayload(LRB24)
                    root_0 = self.adaptor.becomeRoot(LRB24_tree, root_0)
                    # psf.g:41:9: ( expr )+
                    cnt6 = 0
                    while True: #loop6
                        alt6 = 2
                        LA6_0 = self.input.LA(1)

                        if (LA6_0 == DOLLARTOKEN or LA6_0 == LRB or (TOKEN <= LA6_0 <= LCB) or LA6_0 == LSB) :
                            alt6 = 1


                        if alt6 == 1:
                            # psf.g:41:9: expr
                            self.following.append(self.FOLLOW_expr_in_atom180)
                            expr25 = self.expr()
                            self.following.pop()

                            self.adaptor.addChild(root_0, expr25.tree)


                        else:
                            if cnt6 >= 1:
                                break #loop6

                            eee = EarlyExitException(6, self.input)
                            raise eee

                        cnt6 += 1


                    # psf.g:41:15: ( HEAD ( expr )* )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == HEAD) :
                        alt8 = 1
                    if alt8 == 1:
                        # psf.g:41:16: HEAD ( expr )*
                        HEAD26 = self.input.LT(1)
                        self.match(self.input, HEAD, self.FOLLOW_HEAD_in_atom184)


                        HEAD26_tree = self.adaptor.createWithPayload(HEAD26)
                        self.adaptor.addChild(root_0, HEAD26_tree)

                        # psf.g:41:21: ( expr )*
                        while True: #loop7
                            alt7 = 2
                            LA7_0 = self.input.LA(1)

                            if (LA7_0 == DOLLARTOKEN or LA7_0 == LRB or (TOKEN <= LA7_0 <= LCB) or LA7_0 == LSB) :
                                alt7 = 1


                            if alt7 == 1:
                                # psf.g:41:21: expr
                                self.following.append(self.FOLLOW_expr_in_atom186)
                                expr27 = self.expr()
                                self.following.pop()

                                self.adaptor.addChild(root_0, expr27.tree)


                            else:
                                break #loop7





                    RRB28 = self.input.LT(1)
                    self.match(self.input, RRB, self.FOLLOW_RRB_in_atom191)



                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end atom

    class narrow_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start narrow
    # psf.g:44:1: narrow : ( TOKEN | DOLLARTOKEN | phrase );
    def narrow(self, ):

        retval = self.narrow_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TOKEN29 = None
        DOLLARTOKEN30 = None
        phrase31 = None


        TOKEN29_tree = None
        DOLLARTOKEN30_tree = None

        try:
            try:
                # psf.g:44:8: ( TOKEN | DOLLARTOKEN | phrase )
                alt10 = 3
                LA10 = self.input.LA(1)
                if LA10 == TOKEN:
                    alt10 = 1
                elif LA10 == DOLLARTOKEN:
                    alt10 = 2
                elif LA10 == LSB:
                    alt10 = 3
                else:
                    nvae = NoViableAltException("44:1: narrow : ( TOKEN | DOLLARTOKEN | phrase );", 10, 0, self.input)

                    raise nvae

                if alt10 == 1:
                    # psf.g:44:10: TOKEN
                    root_0 = self.adaptor.nil()

                    TOKEN29 = self.input.LT(1)
                    self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_narrow202)


                    TOKEN29_tree = self.adaptor.createWithPayload(TOKEN29)
                    self.adaptor.addChild(root_0, TOKEN29_tree)



                elif alt10 == 2:
                    # psf.g:45:4: DOLLARTOKEN
                    root_0 = self.adaptor.nil()

                    DOLLARTOKEN30 = self.input.LT(1)
                    self.match(self.input, DOLLARTOKEN, self.FOLLOW_DOLLARTOKEN_in_narrow207)


                    DOLLARTOKEN30_tree = self.adaptor.createWithPayload(DOLLARTOKEN30)
                    self.adaptor.addChild(root_0, DOLLARTOKEN30_tree)



                elif alt10 == 3:
                    # psf.g:46:4: phrase
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_phrase_in_narrow212)
                    phrase31 = self.phrase()
                    self.following.pop()

                    self.adaptor.addChild(root_0, phrase31.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end narrow

    class curlyset_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start curlyset
    # psf.g:49:1: curlyset : LCB ( atom )* RCB ;
    def curlyset(self, ):

        retval = self.curlyset_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LCB32 = None
        RCB34 = None
        atom33 = None


        LCB32_tree = None
        RCB34_tree = None

        try:
            try:
                # psf.g:49:9: ( LCB ( atom )* RCB )
                # psf.g:49:11: LCB ( atom )* RCB
                root_0 = self.adaptor.nil()

                LCB32 = self.input.LT(1)
                self.match(self.input, LCB, self.FOLLOW_LCB_in_curlyset221)


                LCB32_tree = self.adaptor.createWithPayload(LCB32)
                root_0 = self.adaptor.becomeRoot(LCB32_tree, root_0)
                # psf.g:49:16: ( atom )*
                while True: #loop11
                    alt11 = 2
                    LA11_0 = self.input.LA(1)

                    if (LA11_0 == DOLLARTOKEN or LA11_0 == LRB or (TOKEN <= LA11_0 <= LCB) or LA11_0 == LSB) :
                        alt11 = 1


                    if alt11 == 1:
                        # psf.g:49:16: atom
                        self.following.append(self.FOLLOW_atom_in_curlyset224)
                        atom33 = self.atom()
                        self.following.pop()

                        self.adaptor.addChild(root_0, atom33.tree)


                    else:
                        break #loop11


                RCB34 = self.input.LT(1)
                self.match(self.input, RCB, self.FOLLOW_RCB_in_curlyset227)




                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end curlyset

    class phrase_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start phrase
    # psf.g:52:1: phrase : LSB TOKEN ( TOKEN )+ RSB ;
    def phrase(self, ):

        retval = self.phrase_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LSB35 = None
        TOKEN36 = None
        TOKEN37 = None
        RSB38 = None

        LSB35_tree = None
        TOKEN36_tree = None
        TOKEN37_tree = None
        RSB38_tree = None

        try:
            try:
                # psf.g:52:8: ( LSB TOKEN ( TOKEN )+ RSB )
                # psf.g:52:10: LSB TOKEN ( TOKEN )+ RSB
                root_0 = self.adaptor.nil()

                LSB35 = self.input.LT(1)
                self.match(self.input, LSB, self.FOLLOW_LSB_in_phrase238)


                LSB35_tree = self.adaptor.createWithPayload(LSB35)
                root_0 = self.adaptor.becomeRoot(LSB35_tree, root_0)
                TOKEN36 = self.input.LT(1)
                self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_phrase241)


                TOKEN36_tree = self.adaptor.createWithPayload(TOKEN36)
                self.adaptor.addChild(root_0, TOKEN36_tree)

                # psf.g:52:21: ( TOKEN )+
                cnt12 = 0
                while True: #loop12
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if (LA12_0 == TOKEN) :
                        alt12 = 1


                    if alt12 == 1:
                        # psf.g:52:22: TOKEN
                        TOKEN37 = self.input.LT(1)
                        self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_phrase244)


                        TOKEN37_tree = self.adaptor.createWithPayload(TOKEN37)
                        self.adaptor.addChild(root_0, TOKEN37_tree)



                    else:
                        if cnt12 >= 1:
                            break #loop12

                        eee = EarlyExitException(12, self.input)
                        raise eee

                    cnt12 += 1


                RSB38 = self.input.LT(1)
                self.match(self.input, RSB, self.FOLLOW_RSB_in_phrase248)




                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end phrase

    class tagexpr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start tagexpr
    # psf.g:55:1: tagexpr : TOKEN ( VOCTAG | INTTAG ) ;
    def tagexpr(self, ):

        retval = self.tagexpr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TOKEN39 = None
        set40 = None

        TOKEN39_tree = None
        set40_tree = None

        try:
            try:
                # psf.g:55:9: ( TOKEN ( VOCTAG | INTTAG ) )
                # psf.g:55:11: TOKEN ( VOCTAG | INTTAG )
                root_0 = self.adaptor.nil()

                TOKEN39 = self.input.LT(1)
                self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_tagexpr259)


                TOKEN39_tree = self.adaptor.createWithPayload(TOKEN39)
                self.adaptor.addChild(root_0, TOKEN39_tree)

                set40 = self.input.LT(1)
                if (VOCTAG <= self.input.LA(1) <= INTTAG):
                    self.input.consume();
                    root_0 = self.adaptor.becomeRoot(self.adaptor.createWithPayload(set40), root_0)
                    self.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_tagexpr261
                        )
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end tagexpr


    # lookup tables for DFA #2

    DFA2_eot = DFA.unpack(
        u"\13\uffff"
        )

    DFA2_eof = DFA.unpack(
        u"\1\uffff\2\4\7\uffff\1\4"
        )

    DFA2_min = DFA.unpack(
        u"\1\10\2\4\1\15\4\uffff\2\15\1\4"
        )

    DFA2_max = DFA.unpack(
        u"\1\20\1\23\1\20\1\15\4\uffff\1\15\1\21\1\20"
        )

    DFA2_accept = DFA.unpack(
        u"\4\uffff\1\2\1\1\1\4\1\3\3\uffff"
        )

    DFA2_special = DFA.unpack(
        u"\13\uffff"
        )

            
    DFA2_transition = [
        DFA.unpack(u"\1\2\1\uffff\1\4\2\uffff\1\1\1\4\1\uffff\1\3"),
        DFA.unpack(u"\1\4\1\6\3\4\1\uffff\1\4\2\uffff\2\4\1\uffff\1\4\1"
        u"\uffff\2\5"),
        DFA.unpack(u"\1\4\1\6\3\4\1\7\1\4\2\uffff\2\4\1\uffff\1\4"),
        DFA.unpack(u"\1\10"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\11"),
        DFA.unpack(u"\1\11\3\uffff\1\12"),
        DFA.unpack(u"\1\4\1\6\3\4\1\uffff\1\4\2\uffff\2\4\1\uffff\1\4")
    ]

    # class definition for DFA #2

    DFA2 = DFA
 

    FOLLOW_line_in_annotate35 = frozenset([1, 4, 8, 10, 13, 14, 16])
    FOLLOW_NEWLINE_in_annotate39 = frozenset([1, 4, 8, 10, 13, 14, 16])
    FOLLOW_tagexpr_in_line51 = frozenset([1])
    FOLLOW_expr_in_line57 = frozenset([1])
    FOLLOW_conjexpr_in_line62 = frozenset([1])
    FOLLOW_corefexpr_in_line67 = frozenset([1])
    FOLLOW_narrow_in_corefexpr78 = frozenset([5])
    FOLLOW_EQ_in_corefexpr80 = frozenset([8, 13, 16])
    FOLLOW_narrow_in_corefexpr83 = frozenset([1])
    FOLLOW_lc_in_expr96 = frozenset([1])
    FOLLOW_rc_in_lc106 = frozenset([1, 6])
    FOLLOW_LARROW_in_lc109 = frozenset([8, 10, 13, 14, 16])
    FOLLOW_lc_in_lc112 = frozenset([1])
    FOLLOW_atom_in_rc124 = frozenset([1, 7])
    FOLLOW_RARROW_in_rc127 = frozenset([8, 10, 13, 14, 16])
    FOLLOW_atom_in_rc130 = frozenset([1, 7])
    FOLLOW_DOLLARTOKEN_in_conjexpr141 = frozenset([9])
    FOLLOW_DCOLON_in_conjexpr143 = frozenset([8, 10, 13, 14, 16])
    FOLLOW_atom_in_conjexpr146 = frozenset([1, 9])
    FOLLOW_DCOLON_in_conjexpr149 = frozenset([8, 10, 13, 14, 16])
    FOLLOW_atom_in_conjexpr152 = frozenset([1])
    FOLLOW_narrow_in_atom167 = frozenset([1])
    FOLLOW_curlyset_in_atom172 = frozenset([1])
    FOLLOW_LRB_in_atom177 = frozenset([8, 10, 13, 14, 16])
    FOLLOW_expr_in_atom180 = frozenset([8, 10, 11, 12, 13, 14, 16])
    FOLLOW_HEAD_in_atom184 = frozenset([8, 10, 12, 13, 14, 16])
    FOLLOW_expr_in_atom186 = frozenset([8, 10, 12, 13, 14, 16])
    FOLLOW_RRB_in_atom191 = frozenset([1])
    FOLLOW_TOKEN_in_narrow202 = frozenset([1])
    FOLLOW_DOLLARTOKEN_in_narrow207 = frozenset([1])
    FOLLOW_phrase_in_narrow212 = frozenset([1])
    FOLLOW_LCB_in_curlyset221 = frozenset([8, 10, 13, 14, 15, 16])
    FOLLOW_atom_in_curlyset224 = frozenset([8, 10, 13, 14, 15, 16])
    FOLLOW_RCB_in_curlyset227 = frozenset([1])
    FOLLOW_LSB_in_phrase238 = frozenset([13])
    FOLLOW_TOKEN_in_phrase241 = frozenset([13])
    FOLLOW_TOKEN_in_phrase244 = frozenset([13, 17])
    FOLLOW_RSB_in_phrase248 = frozenset([1])
    FOLLOW_TOKEN_in_tagexpr259 = frozenset([18, 19])
    FOLLOW_set_in_tagexpr261 = frozenset([1])

