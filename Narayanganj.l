%{
#include "narayanganj.tab.h"
%}

%%
"jodi dekhi x 4"          { return IF_X_4; }
"naile"                  { return ELSE; }
"x te 5 dao"             { return ADD5; }
"y te 3 dao"             { return ADD3; }
"x y gun"                { return MULTIPLY; }
"i ek barau"             { return INC_I; }
"x te i rakho"           { return ASSIGN_I; }

[\n]+                    ;
[ \t]+                   ;
.                         ;
%%

int yywrap() {
    return 1;
}


input:
jodi dekhi x 4
x te 5 dao
y te 3 dao
x y gun
i ek barau
x te i rakho
naile
x te 5 dao
