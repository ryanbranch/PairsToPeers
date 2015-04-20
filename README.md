# PairsToPeers
####The repository for the creation of the Pairs To Peers game

======
###Instructions:

An explanation of the actual gameplay is included in the game itself.  However, there are a few "hidden" features that we'd like to clear up here.

1. The About Screen
By clicking on the game logo on the main menu screen, the user will be taken to the About Screen, which has some basic information about the game and its creators, as well as some thank-yous for the creators of the modules and sound files that we used.

2. Cheat Codes
On the difficulty screen, if a user enters their name as "Chesney", "chesney", or "CHESNEY", cheat mode will be activated.  This mode allows the user to see exactly how many points the cards in their answer deck are worth when paired with the given scenario, before they actually play any cards.

3. Dynamic Difficulty
Our game features a dynamic difficulty system, although it is not incredibly evident as it is designed to smoothly transition over time and to not be too noticeable.  Basically, there is a counter in the game that keeps track of how many "Great" (6 - 10 point) answers the user has played in a row.  The amount of time that a user is given for each round of the game is modified, based on this number.  Upon submitting an "Okay" (1 - 5 point) answer, the streak is not broken, but is not added to either.  Running out of time or submitting a "Poor" (0 point) answer causes the streak to be broken and the amount of time alotted per round to be returned to its initial value.

======
###Explanation of Outside Sources

This program makes use of the module "TextRect", which is a part of the pygame code repository.  The module, also known as "Word-wrapped text display module", was written by David Clark in 2001 and allows pygame users to render wrapped text, bound by a specified rectangle.

Pairs to Peers also uses the module "EzText", a user-submitted python library created by Jerome Rasky in 2008.  It allows pygame users to create their own text input fields.

The game also makes use of 2 sound files, all of which are licensed under either Public Domain or the Creative Commons Attribution 3.0 license.  The sounds were downloaded in their raw MP3 form and then chopped and/or given various effects in order to make them better fit the game.  The software used for this is Audacity, which is distributed under the GNU General Public License.

The fonts used in this game are OpenSans and OpenSans Bold, both of which were created by Steve Matteson and are licensed under the Apache 2.0 License. 

======
###Citations

Clark, David.  (2001) TextRect [Computer Program].  Available at http://www.pygame.org/pcr/text_rect/index.php (Accessed 16 February 2015)

DiAngelo, Mark. (2013) Blop [Sound Recording].  Available at http://soundbible.com/2067-Blop.html (Accessed 17 February 2015)

Matteson, Steve. OpenSans [Font].  Available at https://www.google.com/fonts/specimen/Open+Sans (Accessed 16 February 2015)

Rasky, Jerome. (2008) EzText. Available at http://pygame.org/project-EzText-920-.html (Accessed 27 March 2015)

Thore. (2009) Auditorium Applause [Sound Recording].  Available at http://soundbible.com/1260-Auditorium-Applause.html (Accessed 18 February 2015)