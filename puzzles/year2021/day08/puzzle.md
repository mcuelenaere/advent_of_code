## --- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit <a href="https://en.wikipedia.org/wiki/Seven-segment_display" target="_blank">seven-segment displays</a> in your submarine are malfunctioning; <span title="Yes, just the four-digit seven-segment ones. Whole batch must have been faulty.">they must have been damaged</span> during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named `` a `` through `` g ``:

<pre><code>  0:      1:      2:      3:      4:
 <em>aaaa</em>    ....    <em>aaaa    aaaa</em>    ....
<em>b    c</em>  .    <em>c</em>  .    <em>c</em>  .    <em>c  b    c</em>
<em>b    c</em>  .    <em>c</em>  .    <em>c</em>  .    <em>c  b    c</em>
 ....    ....    <em>dddd    dddd    dddd</em>
<em>e    f</em>  .    <em>f  e</em>    .  .    <em>f</em>  .    <em>f</em>
<em>e    f</em>  .    <em>f  e</em>    .  .    <em>f</em>  .    <em>f</em>
 <em>gggg</em>    ....    <em>gggg    gggg</em>    ....

  5:      6:      7:      8:      9:
 <em>aaaa    aaaa    aaaa    aaaa    aaaa</em>
<em>b</em>    .  <em>b</em>    .  .    <em>c  b    c  b    c</em>
<em>b</em>    .  <em>b</em>    .  .    <em>c  b    c  b    c</em>
 <em>dddd    dddd</em>    ....    <em>dddd    dddd</em>
.    <em>f  e    f</em>  .    <em>f  e    f</em>  .    <em>f</em>
.    <em>f  e    f</em>  .    <em>f  e    f</em>  .    <em>f</em>
 <em>gggg    gggg</em>    ....    <em>gggg    gggg</em>
</code></pre>

So, to render a `` 1 ``, only segments `` c `` and `` f `` would be turned on; the rest would be off. To render a `` 7 ``, only segments `` a ``, `` c ``, and `` f `` would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires `` a `` through `` g ``, but those wires are connected to segments _randomly_. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits _within_ a display use the same connections, though.)

So, you might know that only signal wires `` b `` and `` g `` are turned on, but that doesn't mean _segments_ `` b `` and `` g `` are turned on: the only digit that uses two segments is `` 1 ``, so it must mean segments `` c `` and `` f `` are meant to be on. With just that information, you still can't tell which wire (`` b ``/`` g ``) goes to which segment (`` c ``/`` f ``). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of _all ten unique signal patterns_ you see, and then write down a single _four digit output value_ (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

    acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
    cdfeb fcadb cdfeb cdbaf

(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten _unique signal patterns_, a `` | `` delimiter, and finally the _four digit output value_. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because `` 7 `` is the only digit that uses three segments, `` dab `` in the above example means that to render a `` 7 ``, signal lines `` d ``, `` a ``, and `` b `` are on. Because `` 4 `` is the only digit that uses four segments, `` eafb `` means that to render a `` 4 ``, signal lines `` e ``, `` a ``, `` f ``, and `` b `` are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (`` cdfeb fcadb cdfeb cdbaf ``) use five segments and are more difficult to deduce.

For now, _focus on the easy digits_. Consider this larger example:

<pre><code>be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
<em>fdgacbe</em> cefdb cefbgd <em>gcbe</em>
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb <em>cgb</em> <em>dgebacf</em> <em>gc</em>
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
<em>cg</em> <em>cg</em> fdcagb <em>cbg</em>
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec <em>cb</em>
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
<em>gecf</em> <em>egdcabf</em> <em>bgf</em> bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
<em>gebdcfa</em> <em>ecba</em> <em>ca</em> <em>fadegcb</em>
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
<em>cefg</em> dcbef <em>fcge</em> <em>gbcadfe</em>
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
<em>ed</em> bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
<em>gbdfcae</em> <em>bgc</em> <em>cg</em> <em>cgb</em>
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
<em>fgae</em> cfgab <em>fg</em> bagce
</code></pre>

Because the digits `` 1 ``, `` 4 ``, `` 7 ``, and `` 8 `` each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting _only digits in the output values_ (the part after `` | `` on each line), in the above example, there are <code><em>26</em></code> instances of digits that use a unique number of segments (highlighted above).

_In the output values, how many times do digits `` 1 ``, `` 4 ``, `` 7 ``, or `` 8 `` appear?_

## --- Part Two ---

Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

    acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
    cdfeb fcadb cdfeb cdbaf

After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

     dddd
    e    a
    e    a
     ffff
    g    b
    g    b
     cccc

So, the unique signal patterns would correspond to the following digits:

*   `` acedgfb ``: `` 8 ``
*   `` cdfbe ``: `` 5 ``
*   `` gcdfa ``: `` 2 ``
*   `` fbcad ``: `` 3 ``
*   `` dab ``: `` 7 ``
*   `` cefabd ``: `` 9 ``
*   `` cdfgeb ``: `` 6 ``
*   `` eafb ``: `` 4 ``
*   `` cagedb ``: `` 0 ``
*   `` ab ``: `` 1 ``

Then, the four digits of the output value can be decoded:

*   `` cdfeb ``: <code><em>5</em></code>
*   `` fcadb ``: <code><em>3</em></code>
*   `` cdfeb ``: <code><em>5</em></code>
*   `` cdbaf ``: <code><em>3</em></code>

Therefore, the output value for this entry is <code><em>5353</em></code>.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

*   `` fdgacbe cefdb cefbgd gcbe ``: `` 8394 ``
*   `` fcgedb cgb dgebacf gc ``: `` 9781 ``
*   `` cg cg fdcagb cbg ``: `` 1197 ``
*   `` efabcd cedba gadfec cb ``: `` 9361 ``
*   `` gecf egdcabf bgf bfgea ``: `` 4873 ``
*   `` gebdcfa ecba ca fadegcb ``: `` 8418 ``
*   `` cefg dcbef fcge gbcadfe ``: `` 4548 ``
*   `` ed bcgafe cdgba cbgef ``: `` 1625 ``
*   `` gbdfcae bgc cg cgb ``: `` 8717 ``
*   `` fgae cfgab fg bagce ``: `` 4315 ``

Adding all of the output values in this larger example produces <code><em>61229</em></code>.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. _What do you get if you add up all of the output values?_