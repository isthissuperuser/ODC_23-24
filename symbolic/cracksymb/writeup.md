#cracksymb
 - The program ends up in the function `check_flag` which has 23 `if`s inside. We can deduce that there is an `if` for every character of the flag
 - You can see the `if`s as a set of linear equation
 - we just needed to port the ifs inside python and made them run with z3 to get the condition to satisfy them all => the flag
