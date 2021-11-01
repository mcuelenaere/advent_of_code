## --- Day 12: The N-Body Problem ---

The space near Jupiter is not a very safe place; you need to be careful of a [big distracting red spot](https://en.wikipedia.org/wiki/Great_Red_Spot), extreme [radiation](https://en.wikipedia.org/wiki/Magnetosphere_of_Jupiter), and a [whole lot of moons](https://en.wikipedia.org/wiki/Moons_of_Jupiter#List) swirling around. You decide to start by tracking the four largest moons: _Io_, _Europa_, _Ganymede_, and _Callisto_.

After a brief scan, you calculate the _position of each moon_ (your puzzle input). You just need to _simulate their motion_ so you can <span title="Or you could just leave, but where's the fun in that?">avoid them</span>.

Each moon has a 3-dimensional position (`` x ``, `` y ``, and `` z ``) and a 3-dimensional velocity. The position of each moon is given in your scan; the `` x ``, `` y ``, and `` z `` velocity of each moon starts at `` 0 ``.

Simulate the motion of the moons in _time steps_. Within each time step, first update the velocity of every moon by applying _gravity_. Then, once all moons' velocities have been updated, update the position of every moon by applying _velocity_. Time progresses by one step once all of the positions are updated.

To apply _gravity_, consider every _pair_ of moons. On each axis (`` x ``, `` y ``, and `` z ``), the velocity of each moon changes by _exactly +1 or -1_ to pull the moons together. For example, if Ganymede has an `` x `` position of `` 3 ``, and Callisto has a `` x `` position of `` 5 ``, then Ganymede's `` x `` velocity _changes by +1_ (because `` 5 &gt; 3 ``) and Callisto's `` x `` velocity _changes by -1_ (because `` 3 &lt; 5 ``). However, if the positions on a given axis are the same, the velocity on that axis _does not change_ for that pair of moons.

Once all gravity has been applied, apply _velocity_: simply add the velocity of each moon to its own position. For example, if Europa has a position of `` x=1, y=2, z=3 `` and a velocity of `` x=-2, y=0,z=3 ``, then its new position would be `` x=-1, y=2, z=6 ``. This process does not modify the velocity of any moon.

For example, suppose your scan reveals the following positions:

    &lt;x=-1, y=0, z=2&gt;
    &lt;x=2, y=-10, z=-7&gt;
    &lt;x=4, y=-8, z=8&gt;
    &lt;x=3, y=5, z=-1&gt;

Simulating the motion of these moons would produce the following:

    After 0 steps:
    pos=&lt;x=-1, y=  0, z= 2&gt;, vel=&lt;x= 0, y= 0, z= 0&gt;
    pos=&lt;x= 2, y=-10, z=-7&gt;, vel=&lt;x= 0, y= 0, z= 0&gt;
    pos=&lt;x= 4, y= -8, z= 8&gt;, vel=&lt;x= 0, y= 0, z= 0&gt;
    pos=&lt;x= 3, y=  5, z=-1&gt;, vel=&lt;x= 0, y= 0, z= 0&gt;
    
    After 1 step:
    pos=&lt;x= 2, y=-1, z= 1&gt;, vel=&lt;x= 3, y=-1, z=-1&gt;
    pos=&lt;x= 3, y=-7, z=-4&gt;, vel=&lt;x= 1, y= 3, z= 3&gt;
    pos=&lt;x= 1, y=-7, z= 5&gt;, vel=&lt;x=-3, y= 1, z=-3&gt;
    pos=&lt;x= 2, y= 2, z= 0&gt;, vel=&lt;x=-1, y=-3, z= 1&gt;
    
    After 2 steps:
    pos=&lt;x= 5, y=-3, z=-1&gt;, vel=&lt;x= 3, y=-2, z=-2&gt;
    pos=&lt;x= 1, y=-2, z= 2&gt;, vel=&lt;x=-2, y= 5, z= 6&gt;
    pos=&lt;x= 1, y=-4, z=-1&gt;, vel=&lt;x= 0, y= 3, z=-6&gt;
    pos=&lt;x= 1, y=-4, z= 2&gt;, vel=&lt;x=-1, y=-6, z= 2&gt;
    
    After 3 steps:
    pos=&lt;x= 5, y=-6, z=-1&gt;, vel=&lt;x= 0, y=-3, z= 0&gt;
    pos=&lt;x= 0, y= 0, z= 6&gt;, vel=&lt;x=-1, y= 2, z= 4&gt;
    pos=&lt;x= 2, y= 1, z=-5&gt;, vel=&lt;x= 1, y= 5, z=-4&gt;
    pos=&lt;x= 1, y=-8, z= 2&gt;, vel=&lt;x= 0, y=-4, z= 0&gt;
    
    After 4 steps:
    pos=&lt;x= 2, y=-8, z= 0&gt;, vel=&lt;x=-3, y=-2, z= 1&gt;
    pos=&lt;x= 2, y= 1, z= 7&gt;, vel=&lt;x= 2, y= 1, z= 1&gt;
    pos=&lt;x= 2, y= 3, z=-6&gt;, vel=&lt;x= 0, y= 2, z=-1&gt;
    pos=&lt;x= 2, y=-9, z= 1&gt;, vel=&lt;x= 1, y=-1, z=-1&gt;
    
    After 5 steps:
    pos=&lt;x=-1, y=-9, z= 2&gt;, vel=&lt;x=-3, y=-1, z= 2&gt;
    pos=&lt;x= 4, y= 1, z= 5&gt;, vel=&lt;x= 2, y= 0, z=-2&gt;
    pos=&lt;x= 2, y= 2, z=-4&gt;, vel=&lt;x= 0, y=-1, z= 2&gt;
    pos=&lt;x= 3, y=-7, z=-1&gt;, vel=&lt;x= 1, y= 2, z=-2&gt;
    
    After 6 steps:
    pos=&lt;x=-1, y=-7, z= 3&gt;, vel=&lt;x= 0, y= 2, z= 1&gt;
    pos=&lt;x= 3, y= 0, z= 0&gt;, vel=&lt;x=-1, y=-1, z=-5&gt;
    pos=&lt;x= 3, y=-2, z= 1&gt;, vel=&lt;x= 1, y=-4, z= 5&gt;
    pos=&lt;x= 3, y=-4, z=-2&gt;, vel=&lt;x= 0, y= 3, z=-1&gt;
    
    After 7 steps:
    pos=&lt;x= 2, y=-2, z= 1&gt;, vel=&lt;x= 3, y= 5, z=-2&gt;
    pos=&lt;x= 1, y=-4, z=-4&gt;, vel=&lt;x=-2, y=-4, z=-4&gt;
    pos=&lt;x= 3, y=-7, z= 5&gt;, vel=&lt;x= 0, y=-5, z= 4&gt;
    pos=&lt;x= 2, y= 0, z= 0&gt;, vel=&lt;x=-1, y= 4, z= 2&gt;
    
    After 8 steps:
    pos=&lt;x= 5, y= 2, z=-2&gt;, vel=&lt;x= 3, y= 4, z=-3&gt;
    pos=&lt;x= 2, y=-7, z=-5&gt;, vel=&lt;x= 1, y=-3, z=-1&gt;
    pos=&lt;x= 0, y=-9, z= 6&gt;, vel=&lt;x=-3, y=-2, z= 1&gt;
    pos=&lt;x= 1, y= 1, z= 3&gt;, vel=&lt;x=-1, y= 1, z= 3&gt;
    
    After 9 steps:
    pos=&lt;x= 5, y= 3, z=-4&gt;, vel=&lt;x= 0, y= 1, z=-2&gt;
    pos=&lt;x= 2, y=-9, z=-3&gt;, vel=&lt;x= 0, y=-2, z= 2&gt;
    pos=&lt;x= 0, y=-8, z= 4&gt;, vel=&lt;x= 0, y= 1, z=-2&gt;
    pos=&lt;x= 1, y= 1, z= 5&gt;, vel=&lt;x= 0, y= 0, z= 2&gt;
    
    After 10 steps:
    pos=&lt;x= 2, y= 1, z=-3&gt;, vel=&lt;x=-3, y=-2, z= 1&gt;
    pos=&lt;x= 1, y=-8, z= 0&gt;, vel=&lt;x=-1, y= 1, z= 3&gt;
    pos=&lt;x= 3, y=-6, z= 1&gt;, vel=&lt;x= 3, y= 2, z=-3&gt;
    pos=&lt;x= 2, y= 0, z= 4&gt;, vel=&lt;x= 1, y=-1, z=-1&gt;

Then, it might help to calculate the _total energy in the system_. The total energy for a single moon is its _potential energy_ multiplied by its _kinetic energy_. A moon's _potential energy_ is the sum of the [absolute values](https://en.wikipedia.org/wiki/Absolute_value) of its `` x ``, `` y ``, and `` z `` position coordinates. A moon's _kinetic energy_ is the sum of the absolute values of its velocity coordinates. Below, each line shows the calculations for a moon's potential energy (`` pot ``), kinetic energy (`` kin ``), and total energy:

<pre><code>Energy after 10 steps:
pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18
Sum of total energy: 36 + 45 + 80 + 18 = <em>179</em>
</code></pre>

In the above example, adding together the total energy for all moons after 10 steps produces the total energy in the system, <code><em>179</em></code>.

Here's a second example:

    &lt;x=-8, y=-10, z=0&gt;
    &lt;x=5, y=5, z=10&gt;
    &lt;x=2, y=-7, z=3&gt;
    &lt;x=9, y=-8, z=-3&gt;

Every ten steps of simulation for 100 steps produces:

<pre><code>After 0 steps:
pos=&lt;x= -8, y=-10, z=  0&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
pos=&lt;x=  5, y=  5, z= 10&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
pos=&lt;x=  2, y= -7, z=  3&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
pos=&lt;x=  9, y= -8, z= -3&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;

After 10 steps:
pos=&lt;x= -9, y=-10, z=  1&gt;, vel=&lt;x= -2, y= -2, z= -1&gt;
pos=&lt;x=  4, y= 10, z=  9&gt;, vel=&lt;x= -3, y=  7, z= -2&gt;
pos=&lt;x=  8, y=-10, z= -3&gt;, vel=&lt;x=  5, y= -1, z= -2&gt;
pos=&lt;x=  5, y=-10, z=  3&gt;, vel=&lt;x=  0, y= -4, z=  5&gt;

After 20 steps:
pos=&lt;x=-10, y=  3, z= -4&gt;, vel=&lt;x= -5, y=  2, z=  0&gt;
pos=&lt;x=  5, y=-25, z=  6&gt;, vel=&lt;x=  1, y=  1, z= -4&gt;
pos=&lt;x= 13, y=  1, z=  1&gt;, vel=&lt;x=  5, y= -2, z=  2&gt;
pos=&lt;x=  0, y=  1, z=  7&gt;, vel=&lt;x= -1, y= -1, z=  2&gt;

After 30 steps:
pos=&lt;x= 15, y= -6, z= -9&gt;, vel=&lt;x= -5, y=  4, z=  0&gt;
pos=&lt;x= -4, y=-11, z=  3&gt;, vel=&lt;x= -3, y=-10, z=  0&gt;
pos=&lt;x=  0, y= -1, z= 11&gt;, vel=&lt;x=  7, y=  4, z=  3&gt;
pos=&lt;x= -3, y= -2, z=  5&gt;, vel=&lt;x=  1, y=  2, z= -3&gt;

After 40 steps:
pos=&lt;x= 14, y=-12, z= -4&gt;, vel=&lt;x= 11, y=  3, z=  0&gt;
pos=&lt;x= -1, y= 18, z=  8&gt;, vel=&lt;x= -5, y=  2, z=  3&gt;
pos=&lt;x= -5, y=-14, z=  8&gt;, vel=&lt;x=  1, y= -2, z=  0&gt;
pos=&lt;x=  0, y=-12, z= -2&gt;, vel=&lt;x= -7, y= -3, z= -3&gt;

After 50 steps:
pos=&lt;x=-23, y=  4, z=  1&gt;, vel=&lt;x= -7, y= -1, z=  2&gt;
pos=&lt;x= 20, y=-31, z= 13&gt;, vel=&lt;x=  5, y=  3, z=  4&gt;
pos=&lt;x= -4, y=  6, z=  1&gt;, vel=&lt;x= -1, y=  1, z= -3&gt;
pos=&lt;x= 15, y=  1, z= -5&gt;, vel=&lt;x=  3, y= -3, z= -3&gt;

After 60 steps:
pos=&lt;x= 36, y=-10, z=  6&gt;, vel=&lt;x=  5, y=  0, z=  3&gt;
pos=&lt;x=-18, y= 10, z=  9&gt;, vel=&lt;x= -3, y= -7, z=  5&gt;
pos=&lt;x=  8, y=-12, z= -3&gt;, vel=&lt;x= -2, y=  1, z= -7&gt;
pos=&lt;x=-18, y= -8, z= -2&gt;, vel=&lt;x=  0, y=  6, z= -1&gt;

After 70 steps:
pos=&lt;x=-33, y= -6, z=  5&gt;, vel=&lt;x= -5, y= -4, z=  7&gt;
pos=&lt;x= 13, y= -9, z=  2&gt;, vel=&lt;x= -2, y= 11, z=  3&gt;
pos=&lt;x= 11, y= -8, z=  2&gt;, vel=&lt;x=  8, y= -6, z= -7&gt;
pos=&lt;x= 17, y=  3, z=  1&gt;, vel=&lt;x= -1, y= -1, z= -3&gt;

After 80 steps:
pos=&lt;x= 30, y= -8, z=  3&gt;, vel=&lt;x=  3, y=  3, z=  0&gt;
pos=&lt;x= -2, y= -4, z=  0&gt;, vel=&lt;x=  4, y=-13, z=  2&gt;
pos=&lt;x=-18, y= -7, z= 15&gt;, vel=&lt;x= -8, y=  2, z= -2&gt;
pos=&lt;x= -2, y= -1, z= -8&gt;, vel=&lt;x=  1, y=  8, z=  0&gt;

After 90 steps:
pos=&lt;x=-25, y= -1, z=  4&gt;, vel=&lt;x=  1, y= -3, z=  4&gt;
pos=&lt;x=  2, y= -9, z=  0&gt;, vel=&lt;x= -3, y= 13, z= -1&gt;
pos=&lt;x= 32, y= -8, z= 14&gt;, vel=&lt;x=  5, y= -4, z=  6&gt;
pos=&lt;x= -1, y= -2, z= -8&gt;, vel=&lt;x= -3, y= -6, z= -9&gt;

After 100 steps:
pos=&lt;x=  8, y=-12, z= -9&gt;, vel=&lt;x= -7, y=  3, z=  0&gt;
pos=&lt;x= 13, y= 16, z= -3&gt;, vel=&lt;x=  3, y=-11, z= -5&gt;
pos=&lt;x=-29, y=-11, z= -1&gt;, vel=&lt;x= -3, y=  7, z=  4&gt;
pos=&lt;x= 16, y=-13, z= 23&gt;, vel=&lt;x=  7, y=  1, z=  1&gt;

Energy after 100 steps:
pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
Sum of total energy: 290 + 608 + 574 + 468 = <em>1940</em>
</code></pre>

_What is the total energy in the system_ after simulating the moons given in your scan for `` 1000 `` steps?

## --- Part Two ---

All this drifting around in space makes you wonder about the nature of the universe. Does history really repeat itself? You're curious whether the moons will ever return to a previous state.

Determine _the number of steps_ that must occur before all of the moons' _positions and velocities_ exactly match a previous point in time.

For example, the first example above takes `` 2772 `` steps before they exactly match a previous point in time; it eventually returns to the initial state:

    After 0 steps:
    pos=&lt;x= -1, y=  0, z=  2&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    pos=&lt;x=  2, y=-10, z= -7&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    pos=&lt;x=  4, y= -8, z=  8&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    pos=&lt;x=  3, y=  5, z= -1&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    
    After 2770 steps:
    pos=&lt;x=  2, y= -1, z=  1&gt;, vel=&lt;x= -3, y=  2, z=  2&gt;
    pos=&lt;x=  3, y= -7, z= -4&gt;, vel=&lt;x=  2, y= -5, z= -6&gt;
    pos=&lt;x=  1, y= -7, z=  5&gt;, vel=&lt;x=  0, y= -3, z=  6&gt;
    pos=&lt;x=  2, y=  2, z=  0&gt;, vel=&lt;x=  1, y=  6, z= -2&gt;
    
    After 2771 steps:
    pos=&lt;x= -1, y=  0, z=  2&gt;, vel=&lt;x= -3, y=  1, z=  1&gt;
    pos=&lt;x=  2, y=-10, z= -7&gt;, vel=&lt;x= -1, y= -3, z= -3&gt;
    pos=&lt;x=  4, y= -8, z=  8&gt;, vel=&lt;x=  3, y= -1, z=  3&gt;
    pos=&lt;x=  3, y=  5, z= -1&gt;, vel=&lt;x=  1, y=  3, z= -1&gt;
    
    After 2772 steps:
    pos=&lt;x= -1, y=  0, z=  2&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    pos=&lt;x=  2, y=-10, z= -7&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    pos=&lt;x=  4, y= -8, z=  8&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;
    pos=&lt;x=  3, y=  5, z= -1&gt;, vel=&lt;x=  0, y=  0, z=  0&gt;

Of course, the universe might last for a _very long time_ before repeating. Here's a copy of the second example from above:

    &lt;x=-8, y=-10, z=0&gt;
    &lt;x=5, y=5, z=10&gt;
    &lt;x=2, y=-7, z=3&gt;
    &lt;x=9, y=-8, z=-3&gt;

This set of initial positions takes `` 4686774924 `` steps before it repeats a previous state! Clearly, you might need to _find a more efficient way to simulate the universe_.

_How many steps does it take_ to reach the first state that exactly matches a previous state?