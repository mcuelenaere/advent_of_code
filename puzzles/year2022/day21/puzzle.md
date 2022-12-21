## --- Day 21: Monkey Math ---

The [monkeys](11) are back! You're worried they're going to try to steal your stuff again, but it seems like they're just holding their ground and making various monkey noises at you.

Eventually, one of the elephants realizes you don't speak monkey and comes over to interpret. As it turns out, they overheard you talking about trying to find the grove; they can show you a shortcut if you answer their _riddle_.

Each monkey is given a _job_: either to _yell a specific number_ or to _yell the result of a math operation_. All of the number-yelling monkeys know their number from the start; however, the math operation monkeys need to wait for two other monkeys to yell a number, and those two other monkeys might _also_ be waiting on other monkeys.

Your job is to _work out the number the monkey named `` root `` will yell_ before the monkeys figure it out themselves.

For example:

    root: pppw + sjmn
    dbpl: 5
    cczh: sllz + lgvd
    zczc: 2
    ptdq: humn - dvpt
    dvpt: 3
    lfqf: 4
    humn: 5
    ljgn: 2
    sjmn: drzm * dbpl
    sllz: 4
    pppw: cczh / lfqf
    lgvd: ljgn * ptdq
    drzm: hmdt - zczc
    hmdt: 32

Each line contains the name of a monkey, a colon, and then the job of that monkey:

*   A lone number means the monkey's job is simply to yell that number.
*   A job like `` aaaa + bbbb `` means the monkey waits for monkeys `` aaaa `` and `` bbbb `` to yell each of their numbers; the monkey then yells the sum of those two numbers.
*   `` aaaa - bbbb `` means the monkey yells `` aaaa ``'s number minus `` bbbb ``'s number.
*   Job `` aaaa * bbbb `` will yell `` aaaa ``'s number multiplied by `` bbbb ``'s number.
*   Job `` aaaa / bbbb `` will yell `` aaaa ``'s number divided by `` bbbb ``'s number.

So, in the above example, monkey `` drzm `` has to wait for monkeys `` hmdt `` and `` zczc `` to yell their numbers. Fortunately, both `` hmdt `` and `` zczc `` have jobs that involve simply yelling a single number, so they do this immediately: `` 32 `` and `` 2 ``. Monkey `` drzm `` can then yell its number by finding `` 32 `` minus `` 2 ``: <code><em>30</em></code>.

Then, monkey `` sjmn `` has one of its numbers (`` 30 ``, from monkey `` drzm ``), and already has its other number, `` 5 ``, from `` dbpl ``. This allows it to yell its own number by finding `` 30 `` multiplied by `` 5 ``: <code><em>150</em></code>.

This process continues until `` root `` yells a number: <code><em>152</em></code>.

However, your actual situation involves <span title="Advent of Code 2022: Now With Considerably More Monkeys">considerably more monkeys</span>. _What number will the monkey named `` root `` yell?_

## --- Part Two ---

Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

First, you got the wrong job for the monkey named `` root ``; specifically, you got the wrong math operation. The correct operation for monkey `` root `` should be `` = ``, which means that it still listens for two numbers (from the same two monkeys as before), but now checks that the two numbers _match_.

Second, you got the wrong monkey for the job starting with `` humn: ``. It isn't a monkey - it's _you_. Actually, you got the job wrong, too: you need to figure out _what number you need to yell_ so that `` root ``'s equality check passes. (The number that appears after `` humn: `` in your input is now irrelevant.)

In the above example, the number you need to yell to pass `` root ``'s equality test is <code><em>301</em></code>. (This causes `` root `` to get the same number, `` 150 ``, from both of its monkeys.)

_What number do you yell to pass `` root ``'s equality test?_