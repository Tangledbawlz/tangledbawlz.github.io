-module(task03).
-export([flavors/0]).


flavors()->
Flavors1 = ["Vanilla", "Chocolate", "Cherry Ripple"],
Flavors2 = ["Lemon", "ButterScotch", "Licorice Ripple"],
lists: join(Flavors1, Flavors2).