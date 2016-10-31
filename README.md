# ascii-art-editor
**To Run**
    ./paint.py
creates a new file (default 80 characters wide, 40 characters high)

./paint.py existingfile.txt
loads an already existing file.  You should probably be careful with this.

**Layout**
The file you're editing is in the center.  This is called the CANVAS. 
The CANVAS is within a CONTAINER which is comprised of small dots.  This lets you know
the borders of the CANVAS when it easily fits into your screen.
The border around the CONTAINER is colored either green or orange.  Green means you're in 
WRITE mode, whereas orange means you're in MOVEMENT mode.
One side is in a bold color.  This is the direction of movement
you're traveling in when you type in a single character in WRITE mode
(and, obviously, it's the opposite direction when you backspace).
If there is no bold-colored border, you have NO direction (cursor
does not advance).  By default, direction is left to right, as you're likely used to.
Below the container is the current PALETTE.  It shows 16 foreground-background color-combinations.
Your currently selected color-combination is underlined.  

**Commands**
***Either Mode***
TAB - switch between WRITE and MOVEMENT modes
HOME - go to beginning of row
END - go to end of row
SHIFT+HOME - go to top of column
SHIFT+END - go to bottom of column
Arrow Keys - move one cursor that direction
***Movement Mode***
hjkl - left, down, up, right
01234567 -
8!@#$%^& - select the color-combination associated with this number/symbol
D - change direction.  After pressing D, type either hjkl or an arrow key to indicate which DIRECTION you want to go, or type "n" to choose no direction
W - Write file
Q - Quit

**To-Do**
Copy-paste
Change palettes
256-color support
default-color support
unicode
many other things


    
