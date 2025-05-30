import curses
import random
from dataclasses import dataclass

PLAYER_CHAR = '^'
ALIEN_CHAR = 'W'
MONSTER_CHAR = 'M'
BULLET_CHAR = '|'
EMPTY_CHAR = ' '

# color pairs
COLOR_PLAYER = 1
COLOR_ALIEN = 2
COLOR_MONSTER = 3
COLOR_BULLET = 4
COLOR_INFO = 5

@dataclass
class Alien:
    x: int
    y: int
    hp: int
    char: str
    color: int


class Game:
    def __init__(self, stdscr, width=40, height=20, num_aliens=8):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.bullets = []  # list of (x, y)
        self.aliens = []  # list of Alien
        self.alien_dir = 1
        self.create_aliens(num_aliens)
        self.running = True
        self.win = False
        self.bombs = 3

    def create_aliens(self, num):
        # create a single row of aliens near top with a few monsters
        padding = (self.width - num) // 2
        y = 2
        self.aliens = []
        for i in range(num):
            x = padding + i
            if random.random() < 0.2:
                self.aliens.append(Alien(x, y, 2, MONSTER_CHAR, COLOR_MONSTER))
            else:
                self.aliens.append(Alien(x, y, 1, ALIEN_CHAR, COLOR_ALIEN))

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
        # info line
        info = f"Bombs:{self.bombs}  Enemies:{len(self.aliens)}"
        self.stdscr.addstr(0, 2, info, curses.color_pair(COLOR_INFO))

        # draw player
        self.stdscr.addch(self.height-2, self.player_x, PLAYER_CHAR, curses.color_pair(COLOR_PLAYER))

        # draw aliens
        for alien in self.aliens:
            self.stdscr.addch(alien.y, alien.x, alien.char, curses.color_pair(alien.color))

        # draw bullets
        for (x, y) in self.bullets:
            self.stdscr.addch(y, x, BULLET_CHAR, curses.color_pair(COLOR_BULLET))

        self.stdscr.refresh()

    def update_bullets(self):
        new_bullets = []
        for x, y in self.bullets:
            y -= 1
            if y <= 1:
                continue
            hit = None
            for alien in self.aliens:
                if alien.x == x and alien.y == y:
                    hit = alien
                    break
            if hit:
                hit.hp -= 1
                if hit.hp <= 0:
                    self.aliens.remove(hit)
                continue
            new_bullets.append((x, y))
        self.bullets = new_bullets

    def update_aliens(self):
        # move horizontally
        moved = []
        edge_reached = False
        for alien in self.aliens:
            nx = alien.x + self.alien_dir
            if nx <= 1 or nx >= self.width - 2:
                edge_reached = True
            moved.append(Alien(nx, alien.y, alien.hp, alien.char, alien.color))
        if edge_reached:
            # move down and reverse
            moved = [Alien(a.x - self.alien_dir, a.y + 1, a.hp, a.char, a.color) for a in self.aliens]
            self.alien_dir *= -1
        self.aliens = moved

        # check lose condition
        for alien in self.aliens:
            if alien.y >= self.height-2:
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
        elif key == ord('b') and self.bombs > 0:
            self.bombs -= 1
            # destroy aliens in player's column
            self.aliens = [a for a in self.aliens if a.x != self.player_x]
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
    curses.start_color()
    curses.init_pair(COLOR_PLAYER, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_ALIEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_MONSTER, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BULLET, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_INFO, curses.COLOR_WHITE, curses.COLOR_BLACK)
    game = Game(stdscr)
    game.draw()
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)
