-module(temperature).
-export([convert/2]).

convert({fahrenheit, Temp}, celsius) ->
        {celsius, 5 * (Temp-32)/9};

convert({celsius, Temp}, fahrenheit) ->
        {fahrenheit, 32 + Temp * 9 / 5};

convert({reaumur, Temp}, celsius) ->
        {celsius, 10 * Temp / 8};


convert({fahrenheit, Temp}, reaumur) ->
        {_, C} = convert({fahrenheit, Temp}, celsius),
        convert({celsius, C}, reaumur);

convert({celsius, Temp}, reaumur) -> 
        {reaumur, 8 * Temp / 10};

convert({X, _}, Y) ->
        {cannot, convert, X, to, Y}.
