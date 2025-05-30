import curses
import random

PLAYER_CHAR = '^'
BULLET_CHAR = '|'

# enemy shapes: 3 types, each 3 characters wide and 2 characters tall
ENEMY_SHAPES = [
    [" ^ ", "/_\\"],
    ["\\o/", "/ \\\\"],
    ["[*]", "/|\\\\"],
]

COLOR_PLAYER = 1
COLOR_BULLET = 2
COLOR_ENEMY1 = 3
COLOR_ENEMY2 = 4
COLOR_ENEMY3 = 5

class Game:
    def __init__(self, stdscr, width=40, height=20, num_aliens=8):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.bullets = []  # list of (x, y)
        self.aliens = []  # list of {'x':int,'y':int,'type':int}
        self.alien_dir = 1
        self.enemy_width = len(ENEMY_SHAPES[0][0])
        self.enemy_height = len(ENEMY_SHAPES[0])
        self.create_aliens(num_aliens)
        self.running = True
        self.win = False

    def create_aliens(self, num):
        # create a single row of aliens near top with various types
        total_width = num * self.enemy_width + (num - 1)
        padding = max(1, (self.width - total_width) // 2)
        y = 2
        self.aliens = []
        for i in range(num):
            x = padding + i * (self.enemy_width + 1)
            alien_type = i % 3
            self.aliens.append({'x': x, 'y': y, 'type': alien_type})

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
        self.stdscr.attron(curses.color_pair(COLOR_PLAYER))
        self.stdscr.addch(self.height-2, self.player_x, PLAYER_CHAR)
        self.stdscr.attroff(curses.color_pair(COLOR_PLAYER))

        # draw aliens
        for alien in self.aliens:
            shape = ENEMY_SHAPES[alien['type']]
            color = curses.color_pair(COLOR_ENEMY1 + alien['type'])
            for dy, line in enumerate(shape):
                for dx, ch in enumerate(line):
                    self.stdscr.attron(color)
                    self.stdscr.addch(alien['y'] + dy, alien['x'] + dx, ch)
                    self.stdscr.attroff(color)

        # draw bullets
        self.stdscr.attron(curses.color_pair(COLOR_BULLET))
        for (x, y) in self.bullets:
            self.stdscr.addch(y, x, BULLET_CHAR)
        self.stdscr.attroff(curses.color_pair(COLOR_BULLET))
        self.stdscr.refresh()

    def update_bullets(self):
        new_bullets = []
        for x, y in self.bullets:
            y -= 1
            if y <= 1:
                continue
            if self.check_bullet_hit(x, y):
                continue
            new_bullets.append((x, y))
        self.bullets = new_bullets

    def check_bullet_hit(self, bx, by):
        for alien in list(self.aliens):
            shape = ENEMY_SHAPES[alien['type']]
            for dy, line in enumerate(shape):
                for dx, _ in enumerate(line):
                    if bx == alien['x'] + dx and by == alien['y'] + dy:
                        self.aliens.remove(alien)
                        return True
        return False

    def update_aliens(self):
        # move horizontally
        moved = []
        edge_reached = False
        for alien in self.aliens:
            nx = alien['x'] + self.alien_dir
            if nx <= 1 or nx + self.enemy_width - 1 >= self.width - 1:
                edge_reached = True
            moved.append({'x': nx, 'y': alien['y'], 'type': alien['type']})
        if edge_reached:
            # move down and reverse
            moved = [
                {
                    'x': a['x'] - self.alien_dir,
                    'y': a['y'] + 1,
                    'type': a['type']
                }
                for a in self.aliens
            ]
            self.alien_dir *= -1
        self.aliens = moved

        # check lose condition
        for alien in self.aliens:
            if alien['y'] + self.enemy_height >= self.height - 2:
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
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(COLOR_PLAYER, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_BULLET, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_ENEMY1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_ENEMY2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(COLOR_ENEMY3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.stdscr.nodelay(True)
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
