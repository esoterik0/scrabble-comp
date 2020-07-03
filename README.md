# scrabble-comp
Scrabble word list filtering based on list comprehensions

# Word List Filter (Wolf)

Each filter method will return a new wolf so that calls can be chained together.

    ex. wolf(words).len(2).prefix('a').words

        wolf().smaller(3).words

Each filter will keep track of a descripton of the operations performed on the list.
n.b. no ,'s or ;'s are used in the desc, just a space between each condition; it looks
somewhat like set notation.

## Filters:
    .len        filters by length
    .lenst      filters by lengths set by a list
    .smaller    filters by length <=
    .bigger     filters by length >=
    .prefix     filters by prefix
    .starts         " "
    .postfix    filters by postfix
    .ends           " "
    .contains   filters for words with the whole string
    .hasltrs    filters for words with all of the letters in ltrs
    .notltrs    filters for words with none of the letters in ltrs
    .foo        filters for words that return true for foo(word); catch all for fancier stuff

## Set operations:
    .union
    .difference
    .intersection

## Utilities:
    .empty      returns an empty wolf
    .save       saves list to file
    .getDesc    gets a description of list
