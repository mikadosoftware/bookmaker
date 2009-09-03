-module(myappend).
-export([myappend/2]).

myappend([H|L1], L2) -> [H|myappend(L1, L2)];
myappend([], L) -> L.


