# Final_project
final project

HEYO SO BIG UPDATE:

I moved my main work into the file called testmapscript.py ; I also realized that the worldmap I am using from GeoPandas also has ISO3 country code data embedded into it, so I've set up the fetching country code thing to only depend on that map (which we are already using anyways) and NOT the .csv file.

I streamlined the code that displays the map significantly, and I also changed draw25 to "autocomplete," which one can call to add more random countries to their current data input session (i.e. if I manually imput three, autocomplete will input another random 22 to bring the count up to 25 for that session).

Lemme know if you have any q's about any of this!

Ok we have to fix the way we display the data. Are we doing one country across multiple times, or are we doing multiple countries and multiple times? Not sure. 

The other problem is that we have to join both tables, and the way it currently works is one table works off countries interpreted from a set of coordinates, and the other works off just coords. I couldn't find a historical temperature API that is based off coordinates because back in like the 70's they didn't have advanced satellite technology so they just measured by general area. Maybe we could still input the emissions in the
