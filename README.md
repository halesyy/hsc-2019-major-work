# HSC - Art 12 - Jack Hales

## (Fluffy)

17-year-old developer with ambitions to become a world-class developer. Blending my passion for programming with my love for art, to create my final-year major work that explores the idea: **who made the artwork, the artist, or the artwork?**. The robot's goal is to be able to decifer it's environment in a internet-disabled environment and push them into the computer's memory and blending it with A.I. and complex algorithm processes to create an artwork that is unique to that time, place, and audience that perceived it's creation.

## (Technical)

Technically from a development standpoint, I am working on Agile development on two segments of the application in this current commit. `/third` and `/bitmap` are slowly being implemented into each other, and I am planning on building `/bitmap` as a completely indipendant module from the `PixelArray` class, which manages all of the operations for bitmapping. This solves the first complex problem, **the travelling salesman algorithm which didn't have a solid solution, where I derived one** as well as **the "artwork" drawing in a derived, well-defined path** to come up with the first **objective** achieved: re-appropriating artworks at the running of code, e.g. "the mona lisa".

### "The Mona Lisa"

This objective entails:

* Breaking down the original artwork to be appropriated, "The Mona Lisa"
* Segmenting the artwork into "bitmap-acceptable" formats, for the `/bitmap` to parse and paint over, and potentially trim
* Re-joining the individual segments into the new, appropriated form and combining all the segments into one, the "reunification"
* Final touches

This is more formally referred in four principles: **Breaking, segmenting, reunifying, perfecting**

### Technical goals required breakthroughs before objectives can be initiated and completed

* ~~Coming up with a "BitMap" schema that can be universally applied~~
* ~~Creating a drawing tool that can run from angles, and draw in a "computer-derived runner" with nifty tricks~~
* ~~Creating a square-based BitMap accessor with meta-programming functions to help analyse the segments~~
* ~~Coming up with a solution to the "travelling salesman" problem, allowing the computer to solve a pilgrim-like puzzle to navigate the bitmap segment to fill in the shape from the broken segment~~
* Creating a parent integration family of functional algorithms to canvas an a segment onto a wholesome to-be appropriation

### Week 2, Art Goal: Create the "Controller" application mind

* Finally fix the re-writer, spending time at home to get a wholistic view and a visualization of the pathing that occurs during each step.
* Think of the integration of the controller, and whether dependency injection is really a good idea or not...


### Week 4

* Write a really intuitive debugger, so I can add much more functionality quickly and rapidly in the future - the functions
are linear, and not dynamically functional.
* Re-write the app and think of the schema.
* The crux of the performance is the attempt to resolve the
traveling salesman problem through a random occurance under certain
parameters, the idea I am thinking of that allows the program
to take as much time, but once it's done (rather quick) it
feeds back and iterates over the pattern to find any
similarities and remove them to shorten the movement. This would
just have the pure movements that aren't re-iterating over each
other in copies.
