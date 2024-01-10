# easyrop
 - the while cycle produces a buffer overflow
 - the tricky part here is managing well the writings in the buffer cause they are made a little irksome
 - if we wanna write a 64 bit address we split the writing in two 32 bit parts and then always send an integer of 0 so the sum results in the half that we wanted
 - after that is a pretty standard rop
