#!/usr/bin/env python3
import curses
from curses import wrapper
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
                
class Main:
    def __init__(self, screen):
        self.screen = screen
        #curses.use_default_colors()
        self.init_colors()
        self.height = 40
        self.width = 80
        self.x = 0
        self.y = 0
        self.canvas_top = 0
        self.canvas_left = 0
        
        self.direction = 0
        self.quit = False
        self.writemode = False
        self.maxy, self.maxx = self.screen.getmaxyx()
        self.cont_left = 3
        self.cont_top = 3
        self.canvas = curses.newpad(self.height, self.width)
        self.resize()
        self.refresh_canvas()

        self.draw_border()
        self.screen.refresh()
        self.mainloop()
    def resize(self):
        self.screen.clear()
        self.maxy, self.maxx = self.screen.getmaxyx()
        self.cont_bottom = self.maxy - 4 
        self.cont_right = self.maxx - 4
        self.canvas_container = self.screen.derwin(self.cont_bottom, \
            self.cont_right, 2, 2)
        self.canvas_container.bkgd(".")

        self.draw_border()
        self.refresh_canvas()
        self.screen.refresh()
    def iimport(self):
        self.screen.move(0,0)
        with open("output2") as f:
            data = f.readlines()
        longest = len(max(data, key=len))
        self.width = longest
        self.height = len(data)
        self.canvas = curses.newpad(self.height, self.width)
        allstrings = []
        allescapes = []
        allcolors = []
        escape = "0"
        for el, line in enumerate(data):
            #line = line.strip("\n")
            string = ""
            i = 0
            colordata = ""
            while True:
                try: ch = line[i]
                except IndexError: break
                if ord(ch) == 27:
                    i += 1
                    if line[i] == "[":
                        i+= 1
                        csi = ""
                        sgr = False
                        while True:
                            nextch = line[i]
                            if nextch == "m": 
                                sgr = True

                                break
                            elif nextch.lower() in \
                                "abcdefghijklmnopqrstuvwxyz":
                                sgr = False
                                break
                            csi += nextch
                            i += 1
                        if sgr:
                            allescapes.append(repr(csi))
                            escape = csi
                else:
                    colordata += escape + "#"
                    string += ch
                i += 1

            allstrings.append(string)
            allcolors.append(colordata)
        self.screen.refresh()
        fg = 0
        bg = 0
        underline = False
        reverse = False
        bold = False # 1
        self.refresh_canvas()
        self.screen.move(0,0)
        for el, l in enumerate(allcolors):
            words = l.split("#")
            for ew, w in enumerate(words):
                attrs = []
                parts = w.split(";")
                for p in parts:
                    try:
                        p = int(p)
                    except: continue
                    if int(p/10) == 3:
                        fg = p % 10

                    elif int(p/10) == 4:
                        bg = p % 10

                    elif p == 24:
                        underline = 0
                    elif p == 4:
                        underline = curses.A_UNDERLINE
                    elif p == 22:
                        bold = 0
                    elif p == 1:
                        bold = curses.A_BOLD
                    elif p == 27:
                        reverse = 0
                    elif p == 7:
                        reverse = curses.A_REVERSE
                color = (bg * curses.COLORS) + fg
                attr = underline | bold | reverse | curses.color_pair(color)
                to_print_attr = attr

                if ew >= self.width: continue
                try: ch = allstrings[el][ew]
                except: 
                    ch = " "
                    to_print_attr = 0
                    
              
                try: self.canvas.addstr( ch, to_print_attr)
                except: continue
            self.screen.refresh()
        self.canvas.move(0, 0)



                    
                    



#            escape = False
#            string = ""
#            escape_str = ""
#            for char in line:
#                if escape:
#                    escape_str += char
#                    if char != "[" and len(escape_str) != 1:
#                        escape_str = ""
#                        escape = False
#                        
#                if ord(char) == 27:
#                    escape = True

    def copy(self):
        win = curses.newwin(self.cont_bottom, self.cont_right, self.cont_top-1, self.cont_left-1)
        self.copywin = win
        self.canvas.overwrite(win)
        for i in range(10):
            try:
                win.vline(0, i*10, "|", 30)
            except: break
        win.box()
        win.overlay(self.canvas)
        
        win.refresh()
        self.screen.refresh()
        
    def draw_border(self):
        
        border = [
            curses.ACS_VLINE, 
            curses.ACS_VLINE, 
            curses.ACS_HLINE, 
            curses.ACS_HLINE,

            curses.ACS_ULCORNER,
            curses.ACS_URCORNER,
            curses.ACS_LLCORNER,
            curses.ACS_LRCORNER
            ]
        color_borders = []
        dir_fix = [1, 0, 3, 2]
        for e, i in enumerate(border):
            if self.writemode:
                i |= curses.color_pair(2)
            else:
                i |= curses.color_pair(3)
            if e < 4 and dir_fix.index(e) == self.direction: 
                i |= curses.A_BOLD
            color_borders.append(i)
        
        self.canvas_container.border(*color_borders)
        self.canvas_container.refresh()
    def color_wheel(self):
        colors = "012345678!@#$%^&"
        for e, i in enumerate(self.palette):
            if i == self.current_pair: i |= curses.A_UNDERLINE
            self.screen.addch(self.cont_bottom + 2 + int(e/8), 3 + (e%8)*2, colors[e], i)
        self.screen.refresh()
        
    def refresh_canvas(self):
        self.canvas_container.refresh()
        self.canvas.refresh(self.canvas_top, self.canvas_left, self.cont_top, self.cont_left, \
            self.cont_bottom, self.cont_right)
    #    self.canvas_container.refresh()
    def mainloop(self):
        self.x, self.y = 0, 0
        self.canvas.move(self.y, self.x)
        self.color_wheel()
        i = 0
        while not self.quit:
            i += 1
            self.y, self.x = self.canvas.getyx()
            width_container = self.cont_right - self.cont_left
            height_container = self.cont_bottom - self.cont_top
            dist_from_right = self.canvas_left + width_container - self.x
            dist_from_left = self.x - self.canvas_left
            dist_from_bottom = self.canvas_top + height_container - self.y
            dist_from_top = self.y - self.canvas_top
            if dist_from_right < 3:
                self.canvas_left = self.x - width_container + 3
                self.draw_border() 
            if dist_from_left < 3:
                self.canvas_left = max(self.x - 3, 0)
            if dist_from_bottom < 3:
                self.canvas_top = self.y - height_container + 3
                self.draw_border() 
            if dist_from_top < 3:
                self.canvas_top = max(self.y - 3, 0)
            self.refresh_canvas()
            self.canvas.cursyncup()
            key = self.screen.getkey()

            if not self.writemode and key == "Q":
                break
            if not self.writemode and key == "W":
                self.export()
            if not self.writemode and key == "C":
                self.copy()
                self.screen.getkey()
                self.copywin.erase()
                del self.copywin
                self.screen.refresh()
                continue
            if not self.writemode and key == "I":
                self.iimport()
                 
            if key == "\t":
                self.writemode = not self.writemode
                self.draw_border()
                continue
            if key == "KEY_RESIZE":
                self.resize()
                continue
            if key == "\n" and self.writemode:
                if self.direction in range(-1, 1):
                    newcoords = (self.y+1, 0)
                elif self.direction == 1:
                    newcoords = (self.y + 1, self.width-1)
                elif self.direction == 2:
                    newcoords = (0, self.x + 1)
                elif self.direction == 3:
                    newcoords = (self.height-1, self.x + 1)
                try: self.canvas.move(*newcoords)
                except: pass
                
                continue
            if self.writemode and len(key) == 1:# and self.x < self.width:
                
                try: self.canvas.addstr(key, self.current_pair)
                except: continue
                if self.direction == -1: # no movement
                    self.canvas.move(self.y, self.x)
                if self.direction == 0: # ->
                    self.canvas.move(self.y, min(self.width-1, self.x+1))
                elif self.direction == 1: #<-
                    self.canvas.move(self.y, max(0, self.x-1))
                elif self.direction == 2: # \/
                    self.canvas.move(min(self.y+1, self.height-1), self.x)
                elif self.direction == 3: # /\
                    self.canvas.move(max(self.y-1, 0), self.x)

                self.refresh_canvas()
                #self.canvas.refresh()
                continue
            if key == "KEY_BACKSPACE":
                y, x = self.canvas.getyx()
                ch = " "
                if self.direction in range(-1, 1):
                    x = max(x-1, 0)
                    
                elif self.direction == 1:
                    x = min(self.width-1, self.x+1)
                elif self.direction == 2:
                    y = max(self.y - 1, 0)
                elif self.direction == 3:
                    y = min(self.height-1, self.y+1)
                self.canvas.addstr(y, x, ch)
                self.canvas.move(y, x)
                continue
            vim_like = {"h": "KEY_LEFT", "j": "KEY_DOWN", "k": "KEY_UP", \
                "l": "KEY_RIGHT"}
            
            movements = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT",\
                "KEY_HOME", "KEY_SHOME", "KEY_END", "KEY_SEND"]
            if key.lower() in vim_like.keys():
                key = vim_like[key.lower()]
            update_position = False
            if key in movements:
                update_position = True
            
            y, x = self.y, self.x 
            if key == "KEY_UP":
                y = max(0, self.y -1)
            elif key == "KEY_DOWN":
                y = min(self.height-1, self.y + 1)
            elif key == "KEY_LEFT":
                x = max(0, self.x - 1)
            elif key == "KEY_RIGHT":
                x = min(self.width-1, self.x + 1)
            elif key == "KEY_HOME":
                x = 0
            elif key == "KEY_SHOME":
                y = 0
            elif key == "KEY_END":
                x = self.width - 1
            elif key == "KEY_SEND":
                y = self.height - 1
            if update_position:
                self.canvas.move(y, x)
            if key.isdigit() or key in "!@#$%^&":
                keys = "012345678!@#$%^&"
                index = keys.index(key)
                self.current_pair = self.palette[index]
                self.color_wheel()
            if key == "d":
                direction = self.screen.getkey()
                if direction in ["l", "KEY_RIGHT"]:
                    self.direction = 0
                elif direction in ["h", "KEY_LEFT"]:
                    self.direction = 1
                elif direction in ["j", "KEY_DOWN"]:
                    self.direction = 2
                elif direction in ["k", "KEY_UP"]:
                    self.direction = 3
                elif direction == "n":
                    self.direction = -1
                self.draw_border()

                
            

            
    def init_colors(self):
        default_fg = 7
        default_bg = 0
        i = 0
        for b in range(curses.COLORS):
            for f in range(curses.COLORS):
                if (f, b) == (0, 0): 
                    i += 1
                    continue

                try:
                    curses.init_pair(i, f, b)
                except: pass
                i += 1
        self.palette = []
        for c in [64, 1, 2, 3, 4, 5, 6, 7]:
            self.palette.append(curses.color_pair(c))
        for c in [64, 1, 2, 3, 4, 5, 6, 7]:
            
            self.palette.append(curses.color_pair(c)|curses.A_BOLD)
        self.current_pair = self.palette[7]
    def export(self):
        lines = []
        
        with open("output", "w") as f:
            for y in range(self.height):
                line = ""
                oldattrs = [24,22,27,130,140]
                for x in range(self.width):
                    inchar = self.canvas.inch(y, x)
                    char = inchar & 255
                    pair_num = (inchar >> 8) & 63
                    fg = pair_num % curses.COLORS
                    bg = int(pair_num / curses.COLORS)
                    is_underline = bool(inchar & curses.A_UNDERLINE)
                    is_bold = bool(inchar & curses.A_BOLD)
                    is_reverse = bool(inchar & curses.A_REVERSE)
                    escape = "\033["
                    attrs = []
                    if is_underline:
                        attrs.append(4)
                    else: attrs.append(24)
                    if is_bold:
                        attrs.append(1)
                    else:
                        attrs.append(22)
                    if is_reverse:
                        attrs.append(7)
                    else:
                        attrs.append(27)
                    attrs.append(30+fg)
                    attrs.append(40+bg)
                    if inchar == 32:
                        attrs = [24,22,27,30,40]
                    attrs_to_write = []
                    for a in attrs:
                        if a not in oldattrs:
                            attrs_to_write.append(a)
                    oldattrs = attrs
                    if attrs_to_write:
                        escape += ";".join([str(a) for a in attrs_to_write])
                        escape += "m"
                    
                        line += escape
                    line += chr(char)
                lines.append(line)
            for line in lines: 
                f.write(line)
                f.write("\033[0m\n")
            self.canvas.move(self.y, self.x)
            

                    

def main(screen):
    screen = Main(screen)

if __name__ == "__main__":
    curses.wrapper(main)
