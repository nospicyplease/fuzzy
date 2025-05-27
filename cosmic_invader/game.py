import curses
import random

PLAYER_CHAR = '^'
ALIEN_CHAR = 'W'
BULLET_CHAR = '|'
EMPTY_CHAR = ' '

class Game:
    def __init__(self, stdscr, width=40, height=20, num_aliens=8):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.bullets = []  # list of (x, y)
        self.aliens = []  # list of (x, y)
        self.alien_dir = 1
        self.create_aliens(num_aliens)
        self.running = True
        self.win = False

    def create_aliens(self, num):
        # create a single row of aliens near top
        padding = (self.width - num) // 2
        y = 2
        self.aliens = [(padding + i, y) for i in range(num)]

    def draw_border(self):
        for x in range(self.width):
            self.stdscr.addch(0, x, '#')
            self.stdscr.addch(self.height-1, x, '#')
        for y in range(self.height):
            self.stdscr.addch(y, 0, '#')
            self.stdscr.addch(y, self.width-1, '#')

    def draw(self):
        self.stdscr.clear()
        self.draw_border()
        # draw player
        self.stdscr.addch(self.height-2, self.player_x, PLAYER_CHAR)
        # draw aliens
        for (x, y) in self.aliens:
            self.stdscr.addch(y, x, ALIEN_CHAR)
        # draw bullets
        for (x, y) in self.bullets:
            self.stdscr.addch(y, x, BULLET_CHAR)
        self.stdscr.refresh()

    def update_bullets(self):
        new_bullets = []
        for x, y in self.bullets:
            y -= 1
            if y <= 1:
                continue
            if (x, y) in self.aliens:
                self.aliens.remove((x, y))
                continue
            new_bullets.append((x, y))
        self.bullets = new_bullets

    def update_aliens(self):
        # move horizontally
        moved = []
        edge_reached = False
        for x, y in self.aliens:
            nx = x + self.alien_dir
            if nx <= 1 or nx >= self.width - 1:
                edge_reached = True
            moved.append((nx, y))
        if edge_reached:
            # move down and reverse
            moved = [(x - self.alien_dir, y + 1) for (x, y) in self.aliens]
            self.alien_dir *= -1
        self.aliens = moved

        # check lose condition
        for x, y in self.aliens:
            if y >= self.height-2:
                self.running = False

    def process_input(self):
        try:
            key = self.stdscr.getch()
        except curses.error:
            key = -1
        if key == curses.KEY_LEFT and self.player_x > 1:
            self.player_x -= 1
        elif key == curses.KEY_RIGHT and self.player_x < self.width - 2:
            self.player_x += 1
        elif key == ord(' '):
            self.bullets.append((self.player_x, self.height-3))
        elif key == ord('q'):
            self.running = False

    def tick(self):
        self.process_input()
        self.update_bullets()
        self.update_aliens()
        self.draw()
        if not self.aliens:
            self.running = False
            self.win = True

    def run(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        while self.running:
            self.tick()
            curses.napms(100)
        self.stdscr.nodelay(False)
        self.stdscr.clear()
        if self.win:
            self.stdscr.addstr(self.height//2, self.width//2 - 4, 'YOU WIN!')
        else:
            self.stdscr.addstr(self.height//2, self.width//2 - 4, 'GAME OVER')
        self.stdscr.refresh()
        self.stdscr.getch()

def main(stdscr):
    game = Game(stdscr)
    game.draw()
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)
