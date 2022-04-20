%This is the file and module for your first attempt and run an Erlang file
-module(test).
-export([print_hello/0]).

print_hello()->
io:fwrite("Hello everybody\nThis is soooo cool!!!\n").