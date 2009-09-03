-module(shop).
-export([cost/1, total/1]).

cost(oranges) -> 5;
cost(newspaper) -> 8;
cost(apples) -> 2;
cost(pears) -> 9;
cost(milk) -> 7;
cost(_) -> 0.

total([{Item, Number}|T]) -> cost(Item) * Number + total(T);
total([]) -> 0.


