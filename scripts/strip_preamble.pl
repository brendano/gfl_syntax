#!/usr/bin/perl -w

use strict;

while(<>) {
  if (/^% ANNO/) {
    print while(<>);
    last;
  }
}

