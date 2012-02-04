# $ANTLR 3.0.1 psf.g 2012-02-03 23:04:11

from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
SLARROW=19
RRB=11
RARROW=7
LARROW=6
LRB=10
RCB=14
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
EQ=5
VOCTAG=17
COMMENT=22
LSB=15
INTTAG=18

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "NEWLINE", "EQ", "LARROW", "RARROW", "DOLLARTOKEN", "DCOLON", "LRB", 
    "RRB", "TOKEN", "LCB", "RCB", "LSB", "RSB", "VOCTAG", "INTTAG", "SLARROW", 
    "SRARROW", "NL", "COMMENT", "WS", "EATWS", "USP"
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
    # psf.g:39:1: atom : ( narrow | curlyset | LRB expr RRB );
    def atom(self, ):

        retval = self.atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LRB24 = None
        RRB26 = None
        narrow22 = None

        curlyset23 = None

        expr25 = None


        LRB24_tree = None
        RRB26_tree = None

        try:
            try:
                # psf.g:39:6: ( narrow | curlyset | LRB expr RRB )
                alt6 = 3
                LA6 = self.input.LA(1)
                if LA6 == DOLLARTOKEN or LA6 == TOKEN or LA6 == LSB:
                    alt6 = 1
                elif LA6 == LCB:
                    alt6 = 2
                elif LA6 == LRB:
                    alt6 = 3
                else:
                    nvae = NoViableAltException("39:1: atom : ( narrow | curlyset | LRB expr RRB );", 6, 0, self.input)

                    raise nvae

                if alt6 == 1:
                    # psf.g:39:8: narrow
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_narrow_in_atom167)
                    narrow22 = self.narrow()
                    self.following.pop()

                    self.adaptor.addChild(root_0, narrow22.tree)


                elif alt6 == 2:
                    # psf.g:40:4: curlyset
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_curlyset_in_atom172)
                    curlyset23 = self.curlyset()
                    self.following.pop()

                    self.adaptor.addChild(root_0, curlyset23.tree)


                elif alt6 == 3:
                    # psf.g:41:4: LRB expr RRB
                    root_0 = self.adaptor.nil()

                    LRB24 = self.input.LT(1)
                    self.match(self.input, LRB, self.FOLLOW_LRB_in_atom177)

                    self.following.append(self.FOLLOW_expr_in_atom180)
                    expr25 = self.expr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, expr25.tree)
                    RRB26 = self.input.LT(1)
                    self.match(self.input, RRB, self.FOLLOW_RRB_in_atom182)



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

        TOKEN27 = None
        DOLLARTOKEN28 = None
        phrase29 = None


        TOKEN27_tree = None
        DOLLARTOKEN28_tree = None

        try:
            try:
                # psf.g:44:8: ( TOKEN | DOLLARTOKEN | phrase )
                alt7 = 3
                LA7 = self.input.LA(1)
                if LA7 == TOKEN:
                    alt7 = 1
                elif LA7 == DOLLARTOKEN:
                    alt7 = 2
                elif LA7 == LSB:
                    alt7 = 3
                else:
                    nvae = NoViableAltException("44:1: narrow : ( TOKEN | DOLLARTOKEN | phrase );", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # psf.g:44:10: TOKEN
                    root_0 = self.adaptor.nil()

                    TOKEN27 = self.input.LT(1)
                    self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_narrow193)


                    TOKEN27_tree = self.adaptor.createWithPayload(TOKEN27)
                    self.adaptor.addChild(root_0, TOKEN27_tree)



                elif alt7 == 2:
                    # psf.g:45:4: DOLLARTOKEN
                    root_0 = self.adaptor.nil()

                    DOLLARTOKEN28 = self.input.LT(1)
                    self.match(self.input, DOLLARTOKEN, self.FOLLOW_DOLLARTOKEN_in_narrow198)


                    DOLLARTOKEN28_tree = self.adaptor.createWithPayload(DOLLARTOKEN28)
                    self.adaptor.addChild(root_0, DOLLARTOKEN28_tree)



                elif alt7 == 3:
                    # psf.g:46:4: phrase
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_phrase_in_narrow203)
                    phrase29 = self.phrase()
                    self.following.pop()

                    self.adaptor.addChild(root_0, phrase29.tree)


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

        LCB30 = None
        RCB32 = None
        atom31 = None


        LCB30_tree = None
        RCB32_tree = None

        try:
            try:
                # psf.g:49:9: ( LCB ( atom )* RCB )
                # psf.g:49:11: LCB ( atom )* RCB
                root_0 = self.adaptor.nil()

                LCB30 = self.input.LT(1)
                self.match(self.input, LCB, self.FOLLOW_LCB_in_curlyset212)


                LCB30_tree = self.adaptor.createWithPayload(LCB30)
                root_0 = self.adaptor.becomeRoot(LCB30_tree, root_0)
                # psf.g:49:16: ( atom )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == DOLLARTOKEN or LA8_0 == LRB or (TOKEN <= LA8_0 <= LCB) or LA8_0 == LSB) :
                        alt8 = 1


                    if alt8 == 1:
                        # psf.g:49:16: atom
                        self.following.append(self.FOLLOW_atom_in_curlyset215)
                        atom31 = self.atom()
                        self.following.pop()

                        self.adaptor.addChild(root_0, atom31.tree)


                    else:
                        break #loop8


                RCB32 = self.input.LT(1)
                self.match(self.input, RCB, self.FOLLOW_RCB_in_curlyset218)




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

        LSB33 = None
        TOKEN34 = None
        TOKEN35 = None
        RSB36 = None

        LSB33_tree = None
        TOKEN34_tree = None
        TOKEN35_tree = None
        RSB36_tree = None

        try:
            try:
                # psf.g:52:8: ( LSB TOKEN ( TOKEN )+ RSB )
                # psf.g:52:10: LSB TOKEN ( TOKEN )+ RSB
                root_0 = self.adaptor.nil()

                LSB33 = self.input.LT(1)
                self.match(self.input, LSB, self.FOLLOW_LSB_in_phrase229)


                LSB33_tree = self.adaptor.createWithPayload(LSB33)
                root_0 = self.adaptor.becomeRoot(LSB33_tree, root_0)
                TOKEN34 = self.input.LT(1)
                self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_phrase232)


                TOKEN34_tree = self.adaptor.createWithPayload(TOKEN34)
                self.adaptor.addChild(root_0, TOKEN34_tree)

                # psf.g:52:21: ( TOKEN )+
                cnt9 = 0
                while True: #loop9
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if (LA9_0 == TOKEN) :
                        alt9 = 1


                    if alt9 == 1:
                        # psf.g:52:22: TOKEN
                        TOKEN35 = self.input.LT(1)
                        self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_phrase235)


                        TOKEN35_tree = self.adaptor.createWithPayload(TOKEN35)
                        self.adaptor.addChild(root_0, TOKEN35_tree)



                    else:
                        if cnt9 >= 1:
                            break #loop9

                        eee = EarlyExitException(9, self.input)
                        raise eee

                    cnt9 += 1


                RSB36 = self.input.LT(1)
                self.match(self.input, RSB, self.FOLLOW_RSB_in_phrase239)




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

        TOKEN37 = None
        set38 = None

        TOKEN37_tree = None
        set38_tree = None

        try:
            try:
                # psf.g:55:9: ( TOKEN ( VOCTAG | INTTAG ) )
                # psf.g:55:11: TOKEN ( VOCTAG | INTTAG )
                root_0 = self.adaptor.nil()

                TOKEN37 = self.input.LT(1)
                self.match(self.input, TOKEN, self.FOLLOW_TOKEN_in_tagexpr250)


                TOKEN37_tree = self.adaptor.createWithPayload(TOKEN37)
                self.adaptor.addChild(root_0, TOKEN37_tree)

                set38 = self.input.LT(1)
                if (VOCTAG <= self.input.LA(1) <= INTTAG):
                    self.input.consume();
                    root_0 = self.adaptor.becomeRoot(self.adaptor.createWithPayload(set38), root_0)
                    self.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_tagexpr252
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
        u"\1\10\2\4\1\14\4\uffff\2\14\1\4"
        )

    DFA2_max = DFA.unpack(
        u"\1\17\1\22\1\17\1\14\4\uffff\1\14\1\20\1\17"
        )

    DFA2_accept = DFA.unpack(
        u"\4\uffff\1\2\1\1\1\4\1\3\3\uffff"
        )

    DFA2_special = DFA.unpack(
        u"\13\uffff"
        )

            
    DFA2_transition = [
        DFA.unpack(u"\1\2\1\uffff\1\4\1\uffff\1\1\1\4\1\uffff\1\3"),
        DFA.unpack(u"\1\4\1\6\3\4\1\uffff\1\4\1\uffff\2\4\1\uffff\1\4\1"
        u"\uffff\2\5"),
        DFA.unpack(u"\1\4\1\6\3\4\1\7\1\4\1\uffff\2\4\1\uffff\1\4"),
        DFA.unpack(u"\1\10"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\11"),
        DFA.unpack(u"\1\11\3\uffff\1\12"),
        DFA.unpack(u"\1\4\1\6\3\4\1\uffff\1\4\1\uffff\2\4\1\uffff\1\4")
    ]

    # class definition for DFA #2

    DFA2 = DFA
 

    FOLLOW_line_in_annotate35 = frozenset([1, 4, 8, 10, 12, 13, 15])
    FOLLOW_NEWLINE_in_annotate39 = frozenset([1, 4, 8, 10, 12, 13, 15])
    FOLLOW_tagexpr_in_line51 = frozenset([1])
    FOLLOW_expr_in_line57 = frozenset([1])
    FOLLOW_conjexpr_in_line62 = frozenset([1])
    FOLLOW_corefexpr_in_line67 = frozenset([1])
    FOLLOW_narrow_in_corefexpr78 = frozenset([5])
    FOLLOW_EQ_in_corefexpr80 = frozenset([8, 12, 15])
    FOLLOW_narrow_in_corefexpr83 = frozenset([1])
    FOLLOW_lc_in_expr96 = frozenset([1])
    FOLLOW_rc_in_lc106 = frozenset([1, 6])
    FOLLOW_LARROW_in_lc109 = frozenset([8, 10, 12, 13, 15])
    FOLLOW_lc_in_lc112 = frozenset([1])
    FOLLOW_atom_in_rc124 = frozenset([1, 7])
    FOLLOW_RARROW_in_rc127 = frozenset([8, 10, 12, 13, 15])
    FOLLOW_atom_in_rc130 = frozenset([1, 7])
    FOLLOW_DOLLARTOKEN_in_conjexpr141 = frozenset([9])
    FOLLOW_DCOLON_in_conjexpr143 = frozenset([8, 10, 12, 13, 15])
    FOLLOW_atom_in_conjexpr146 = frozenset([1, 9])
    FOLLOW_DCOLON_in_conjexpr149 = frozenset([8, 10, 12, 13, 15])
    FOLLOW_atom_in_conjexpr152 = frozenset([1])
    FOLLOW_narrow_in_atom167 = frozenset([1])
    FOLLOW_curlyset_in_atom172 = frozenset([1])
    FOLLOW_LRB_in_atom177 = frozenset([8, 10, 12, 13, 15])
    FOLLOW_expr_in_atom180 = frozenset([11])
    FOLLOW_RRB_in_atom182 = frozenset([1])
    FOLLOW_TOKEN_in_narrow193 = frozenset([1])
    FOLLOW_DOLLARTOKEN_in_narrow198 = frozenset([1])
    FOLLOW_phrase_in_narrow203 = frozenset([1])
    FOLLOW_LCB_in_curlyset212 = frozenset([8, 10, 12, 13, 14, 15])
    FOLLOW_atom_in_curlyset215 = frozenset([8, 10, 12, 13, 14, 15])
    FOLLOW_RCB_in_curlyset218 = frozenset([1])
    FOLLOW_LSB_in_phrase229 = frozenset([12])
    FOLLOW_TOKEN_in_phrase232 = frozenset([12])
    FOLLOW_TOKEN_in_phrase235 = frozenset([12, 16])
    FOLLOW_RSB_in_phrase239 = frozenset([1])
    FOLLOW_TOKEN_in_tagexpr250 = frozenset([17, 18])
    FOLLOW_set_in_tagexpr252 = frozenset([1])

