# pybook
 - the webapp lets you write andexecute code if it gets successfully validated
 - we first send valid code and then in parallel not valid code to print the flag
 - we repeat this process infinitely and we create a race condition on the file were we write (one file in common for all requests)
 - there is a chance that this serie of events happens:
   1 valid file is written
   2 valid file is checked ok
   3 unsafe file is written
   4 file is executed
 - all these events might happen in the flow of the first request hence actually running an unsafe file and displaying us the flag
