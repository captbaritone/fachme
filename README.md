What
====

FachMe uses a database of opera recording casts to find relationships between
opera roles. The user inputs a list of roles, and FachMe returns a list of
similar roles. You can find the live site at http://fachme.com, and my initial
writeup about the project at my blog:
http://blog.classicalcode.com/2011/05/fachme-find-your-roles/

Why
===

I have long been frustrated by the limitations of the pigeon-hole based fach
system. Singers and characters are each unique and I thought a data-driven
approach might be able to find more subtle and refined relationships between
roles and voices than a simple system of categorization.

How
===

As part of a separate project, I had collected a structured database of over
6,000 opera recordings and their casts. FachMe leverages that data to find
correlations between roles. In simple terms, FachMe works like so:

We attempt to define the user as a collection of characters, each character 
representing a percentage of the user's identity depending on it's relative 
relevance.

A relationship between the user and a character can be traced via the following 
five steps:

1. The user (U) is defined equally by the n characters (e.g. C1) they input.
2. C1 is defined equally by the n recordings (e.g. R1) with that character.
3. R1 is defined by the one singer (e.g. S1) portraying C1 on R1.
4. S1 is defined equally by the n recordings (e.g. R2) with that singer.
5. R1 is defined by the one character (e.g. C2) portrayed by S1 on R2.

By gathering a table of every one of these relationships we can computer the 
total percentage of U that is defined by C2, and therefore every character. In 
the table below, each line represents one of these relationships. The 
percentage of U that each relationship defines (or "weight") can be computed 
using the function given to the right of the U to C2 relationships.


    U ┌ C1 ┌ R1 - S1 ┌ R2 - C2  weight = 1/(Cs in U) * 1/(Rs in C1) * 1/(Rs in S1)
      |    |         | R3 - C3         = 1/2         * 1/3          * 1/3
      |    |         └ R4 - C4         = 1/18
      |    |
      |    | R2 - S2 ┌ R5 - C5
      |    |         | R6 - C6
      |    |         | R7 - C2  weight = 1/2         * 1/3          * 1/4
      |    |         └ R8 - C3         = 1/24
      |    |
      |    | R3 - S1 ┌ R2 - C2  weight = 1/2         * 1/3          * 1/3
      |    |         | R3 - C3         = 1/18
      |    └         └ R4 - C4
      |
      | C2 ┌ R9 - S3 ┌ R2 - C5
      └    └         └ R9 - C8

The sum of all the weights in the table will be 1, or 100%, representing the
percentages of the user that are defined by the various roles.

The percentage of U that is defined by C2 is the sum of all the weights of 
lines ending with C2:

    U is (1/18 + 1/24 + 1/18) C2
    U is        11/72         C2
    ----------------------------
    U is       ~15.3%         C2

The actual code is a bit more complicated because of the following additional
features:

1. Only correlate roles that were performed around the same time as the given
   roles.
2. Omit roles and singes with too few recordings on the grounds that they have
   an insufficient sample size.
3. Try to adjust for the biases in the database so that operas that are
   over-represented in our data are no disproportionately recommended.

Credit
======

- Wikipedia icons donated to the Creative Commons courtesy of [Paul Robert
  Lloyd](http://www.paulrobertlloyd.com/) 

- FachMe's user interface depends heavily on a modified version of the jQuery
  plugin [jQuery Tokeninput](http://loopj.com/jquery-tokeninput/) by James
  Smith.  Many thanks to Mr. Smith and all the people who work on that project.

- The original graphic design for FachMe was done by Sergio Bello
  <desk@sergioismy.name>. He has generously donated his intellectual property
  to this open source project.
