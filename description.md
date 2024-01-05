# automatic chess board
#### Video Demo:  <https://youtu.be/XD8byjU84CI>
#### Description:

I made a Python program to automate movement on a chess board. If you give it a chess notation it while move the pieces to the corresponding locations.

#### thirde party code
It uses pybricks to run the program on the LEGO EV3.

#### file
It uses just 1 file the main.py.

#### start program
It starts by asking for a command these are handy things to control the cart easily. Thy are more for testing and so.

- Move up with a distance of a given value.
- Any other direction to move.
- Move the cart from any position to the 0.0 position.
- Turn the magnet in the cart on or off.
- Print the current location of the cart.
- And most important of all the "game" command to start the game.

#### game mode
With game you can play the game. It asks one move each for white and then black. Until there is a winner.

To enter a move I use my own variant of the long algebraic notation.

- \# means check mate.
- \+ means the king is in check.
- = means that a pawn has crossed over and is promoted to another piece. (this is not done automatically in my program)
- 0-0 kingsidecastle
- 0-0-0 queensidecastle
- e.p. is to indicate an en passant.
- \- Is used for a normal move.
- x is used when a piece is taken.

#### example
Eg: qd8xd5p (the p at the end means that a pawn is taken)
sentence: Queen on d8 captures on d5.
Pc4xb4 e.p. (here the piece taken is not specified because it is always a pawn)
sentence: Pwan on c4 captures the pwan en passent on c4

#### sentens
After you have entered your move it is translated into a sentence for easy reference. This is also useful because in the future I would like you to be able to play against the computer and then when the computer makes a move it will be shown as a sentence to the player so that he can start thinking before pieces are actually moved.

#### xy table
The xy table has a theoretical accuracy of 0.017 cm.
The motor is accurate to 2 degrees. (1.022 * 3.14) /180 = 0.017 cm
But because the strings are stretchy and the lego base can also partially fold there is play on them and that accuracy cannot be achieved also the strings sometimes slip over the wheels because for large acceleration there is not enough resistance between the string and the wheel.

The magnet is self wound so it had the right shape for in my cart. The magnet has a metal top to better direct the field lines to the magnet inside the piece. I do this so that when 2 pieces pass each other only the correct piece moves with them. This does works, but it could use some improvement in the future.

The magnet is also equipped with a capacitor and a resistor to work away the voltage generated during swiching of so there is no spark in the switch. This is to extend the life of the switch.( in the future I might use a transistor)

#### Disclaimer!
Some function names and variables in the program are in the Dutch language (my native language) . But all commands entered by the user en responses are in English.
