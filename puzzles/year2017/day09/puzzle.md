## --- Day 9: Stream Processing ---

A large stream blocks your path. According to the locals, it's not safe to <span title="&quot;Don't cross the streams!&quot;, they yell, even though there's only one. They seem to think they're hilarious.">cross the stream</span> at the moment because it's full of _garbage_. You look down at the stream; rather than water, you discover that it's a _stream of characters_.

You sit for a while and record part of the stream (your puzzle input). The characters represent _groups_ - sequences that begin with `` { `` and end with `` } ``. Within a group, there are zero or more other things, separated by commas: either another _group_ or _garbage_. Since groups can contain other groups, a `` } `` only closes the _most-recently-opened unclosed group_ - that is, they are nestable. Your puzzle input represents a single, large group which itself contains many smaller ones.

Sometimes, instead of a group, you will find _garbage_. Garbage begins with `` &lt; `` and ends with `` &gt; ``. Between those angle brackets, almost any character can appear, including `` { `` and `` } ``. _Within_ garbage, `` &lt; `` has no special meaning.

In a futile attempt to clean up the garbage, some program has _canceled_ some of the characters within it using `` ! ``: inside garbage, _any_ character that comes after `` ! `` should be _ignored_, including `` &lt; ``, `` &gt; ``, and even another `` ! ``.

You don't see any characters that deviate from these rules. Outside garbage, you only find well-formed groups, and garbage always terminates according to the rules above.

Here are some self-contained pieces of garbage:

*   `` &lt;&gt; ``, empty garbage.
*   `` &lt;random characters&gt; ``, garbage containing random characters.
*   `` &lt;&lt;&lt;&lt;&gt; ``, because the extra `` &lt; `` are ignored.
*   `` &lt;{!&gt;}&gt; ``, because the first `` &gt; `` is canceled.
*   `` &lt;!!&gt; ``, because the second `` ! `` is canceled, allowing the `` &gt; `` to terminate the garbage.
*   `` &lt;!!!&gt;&gt; ``, because the second `` ! `` and the first `` &gt; `` are canceled.
*   `` &lt;{o"i!a,&lt;{i&lt;a&gt; ``, which ends at the first `` &gt; ``.

Here are some examples of whole streams and the number of groups they contain:

*   `` {} ``, `` 1 `` group.
*   `` {{{}}} ``, `` 3 `` groups.
*   `` {{},{}} ``, also `` 3 `` groups.
*   `` {{{},{},{{}}}} ``, `` 6 `` groups.
*   `` {&lt;{},{},{{}}&gt;} ``, `` 1 `` group (which itself contains garbage).
*   `` {&lt;a&gt;,&lt;a&gt;,&lt;a&gt;,&lt;a&gt;} ``, `` 1 `` group.
*   `` {{&lt;a&gt;},{&lt;a&gt;},{&lt;a&gt;},{&lt;a&gt;}} ``, `` 5 `` groups.
*   `` {{&lt;!&gt;},{&lt;!&gt;},{&lt;!&gt;},{&lt;a&gt;}} ``, `` 2 `` groups (since all but the last `` &gt; `` are canceled).

Your goal is to find the total score for all groups in your input. Each group is assigned a _score_ which is one more than the score of the group that immediately contains it. (The outermost group gets a score of `` 1 ``.)

*   `` {} ``, score of `` 1 ``.
*   `` {{{}}} ``, score of `` 1 + 2 + 3 = 6 ``.
*   `` {{},{}} ``, score of `` 1 + 2 + 2 = 5 ``.
*   `` {{{},{},{{}}}} ``, score of `` 1 + 2 + 3 + 3 + 3 + 4 = 16 ``.
*   `` {&lt;a&gt;,&lt;a&gt;,&lt;a&gt;,&lt;a&gt;} ``, score of `` 1 ``.
*   `` {{&lt;ab&gt;},{&lt;ab&gt;},{&lt;ab&gt;},{&lt;ab&gt;}} ``, score of `` 1 + 2 + 2 + 2 + 2 = 9 ``.
*   `` {{&lt;!!&gt;},{&lt;!!&gt;},{&lt;!!&gt;},{&lt;!!&gt;}} ``, score of `` 1 + 2 + 2 + 2 + 2 = 9 ``.
*   `` {{&lt;a!&gt;},{&lt;a!&gt;},{&lt;a!&gt;},{&lt;ab&gt;}} ``, score of `` 1 + 2 = 3 ``.

_What is the total score_ for all groups in your input?

## --- Part Two ---

Now, you're ready to remove the garbage.

To prove you've removed it, you need to count all of the characters within the garbage. The leading and trailing `` &lt; `` and `` &gt; `` don't count, nor do any canceled characters or the `` ! `` doing the canceling.

*   `` &lt;&gt; ``, `` 0 `` characters.
*   `` &lt;random characters&gt; ``, `` 17 `` characters.
*   `` &lt;&lt;&lt;&lt;&gt; ``, `` 3 `` characters.
*   `` &lt;{!&gt;}&gt; ``, `` 2 `` characters.
*   `` &lt;!!&gt; ``, `` 0 `` characters.
*   `` &lt;!!!&gt;&gt; ``, `` 0 `` characters.
*   `` &lt;{o"i!a,&lt;{i&lt;a&gt; ``, `` 10 `` characters.

_How many non-canceled characters are within the garbage_ in your puzzle input?