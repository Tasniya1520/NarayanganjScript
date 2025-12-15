%{
#include <stdio.h>
#include <stdlib.h>

int x = 4, y = 2, i = 1;
int kaj_chalu = 0;

FILE *out;

int yylex();
void yyerror(const char *s);
%}

%token IF_X_4 ELSE ADD5 ADD3 MULTIPLY INC_I ASSIGN_I

%%
program:
        program statement
        | statement
        ;

statement:
        IF_X_4 {
            if (x == 4) {
                kaj_chalu = 1;
                fprintf(out, "Dekha gese: x 4 er shoman\n");
            } else {
                kaj_chalu = 0;
                fprintf(out, "Dekha gese na\n");
            }
        }
        | ELSE {
            kaj_chalu = !kaj_chalu;
            fprintf(out, "Naile block e dhuksi\n");
        }
        | ADD5 {
            if (kaj_chalu) {
                x += 5;
                fprintf(out, "x te 5 dao hoise → x = %d\n", x);
            }
        }
        | ADD3 {
            if (kaj_chalu) {
                y += 3;
                fprintf(out, "y te 3 dao hoise → y = %d\n", y);
            }
        }
        | MULTIPLY {
            if (kaj_chalu) {
                x = x * y;
                fprintf(out, "x ar y gun hoise → x = %d\n", x);
            }
        }
        | INC_I {
            if (kaj_chalu) {
                i++;
                fprintf(out, "i ek barlo → i = %d\n", i);
            }
        }
        | ASSIGN_I {
            if (kaj_chalu) {
                x = i;
                fprintf(out, "x te i rakha hoise → x = %d\n", x);
            }
        }
        ;
%%
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    out = fopen("output.txt", "w");

    fprintf(out, "Narayanganj Banglish Local Language Compiler choltesey\n\n");

    yyparse();

    fprintf(out, "\nKaj shundor bhabe sesh hoise 💪\n");

    fclose(out);

    printf("Compiler run hoise. output.txt dekho.\n");
    return 0;
}


bison code
