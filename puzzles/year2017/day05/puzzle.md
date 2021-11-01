## --- Day 5: A Maze of Twisty Trampolines, All Alike ---

An urgent <span title="Later, on its turn, it sends you a sorcery.">interrupt</span> arrives from the CPU: it's trapped in a maze of jump instructions, and it would like assistance from any programs with spare cycles to help find the exit.

The message includes a list of the offsets for each jump. Jumps are relative: `` -1 `` moves to the previous instruction, and `` 2 `` skips the next one. Start at the first instruction in the list. The goal is to follow the jumps until one leads _outside_ the list.

In addition, these instructions are a little strange; after each jump, the offset of that instruction increases by `` 1 ``. So, if you come across an offset of `` 3 ``, you would move three instructions forward, but change it to a `` 4 `` for the next time it is encountered.

For example, consider the following list of jump offsets:

    0
    3
    0
    1
    -3

Positive jumps ("forward") move downward; negative jumps move upward. For legibility in this example, these offset values will be written all on one line, with the current instruction marked in parentheses. The following steps would be taken before an exit is found:

*   `` (0)&nbsp;3&nbsp;&nbsp;0&nbsp;&nbsp;1&nbsp;&nbsp;-3&nbsp; `` - _before_ we have taken any steps.
*   `` (1)&nbsp;3&nbsp;&nbsp;0&nbsp;&nbsp;1&nbsp;&nbsp;-3&nbsp; `` - jump with offset `` 0 `` (that is, don't jump at all). Fortunately, the instruction is then incremented to `` 1 ``.
*   `` &nbsp;2&nbsp;(3)&nbsp;0&nbsp;&nbsp;1&nbsp;&nbsp;-3&nbsp; `` - step forward because of the instruction we just modified. The first instruction is incremented again, now to `` 2 ``.
*   `` &nbsp;2&nbsp;&nbsp;4&nbsp;&nbsp;0&nbsp;&nbsp;1&nbsp;(-3) `` - jump all the way to the end; leave a `` 4 `` behind.
*   `` &nbsp;2&nbsp;(4)&nbsp;0&nbsp;&nbsp;1&nbsp;&nbsp;-2&nbsp; `` - go back to where we just were; increment `` -3 `` to `` -2 ``.
*   `` &nbsp;2&nbsp;&nbsp;5&nbsp;&nbsp;0&nbsp;&nbsp;1&nbsp;&nbsp;-2&nbsp; `` - jump `` 4 `` steps forward, escaping the maze.

In this example, the exit is reached in `` 5 `` steps.

_How many steps_ does it take to reach the exit?

## --- Part Two ---

Now, the jumps are even stranger: after each jump, if the offset was _three or more_, instead _decrease_ it by `` 1 ``. Otherwise, increase it by `` 1 `` as before.

Using this rule with the above example, the process now takes `` 10 `` steps, and the offset values after finding the exit are left as `` 2 3 2 3 -1 ``.

_How many steps_ does it now take to reach the exit?