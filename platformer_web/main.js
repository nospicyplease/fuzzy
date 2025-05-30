const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const WIDTH = canvas.width;
const HEIGHT = canvas.height;
const TILE = 32;

// Simple map. . = empty
const MAP = [
  '................................................................',
  '................................................................',
  '............................P...................................',
  '.................................................E..............',
  '...............................P...............................F',
  '............................................................S...',
  'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
];

class Player {
  constructor(x, y) {
    this.x = x; this.y = y;
    this.w = TILE; this.h = TILE;
    this.vx = 0; this.vy = 0;
    this.speed = 3;
    this.jumpPower = 12;
    this.onGround = false;
  }

  update(keys, level) {
    // horizontal input
    if (keys['ArrowLeft'] || keys['a']) this.vx = -this.speed;
    else if (keys['ArrowRight'] || keys['d']) this.vx = this.speed;
    else this.vx = 0;

    // jump
    if ((keys[' '] || keys['Space'] || keys['ArrowUp']) && this.onGround) {
      this.vy = -this.jumpPower;
      this.onGround = false;
    }

    // horizontal movement
    this.x += this.vx;
    let colliders = level.getColliders(this);
    colliders.forEach(rect => {
      if (this.vx > 0 && this.x + this.w > rect.x && this.x < rect.x) {
        this.x = rect.x - this.w;
      } else if (this.vx < 0 && this.x < rect.x + rect.w && this.x + this.w > rect.x + rect.w) {
        this.x = rect.x + rect.w;
      }
    });

    // gravity
    this.vy += level.gravity;
    this.y += this.vy;
    colliders = level.getColliders(this);
    this.onGround = false;
    colliders.forEach(rect => {
      if (this.vy > 0 && this.y + this.h > rect.y && this.y < rect.y) {
        this.y = rect.y - this.h;
        this.vy = 0;
        this.onGround = true;
      } else if (this.vy < 0 && this.y < rect.y + rect.h && this.y + this.h > rect.y + rect.h) {
        this.y = rect.y + rect.h;
        this.vy = 0;
      }
    });
  }

  draw(offset) {
    ctx.fillStyle = '#00f';
    ctx.fillRect(this.x - offset, this.y, this.w, this.h);
  }
}

class Enemy {
  constructor(x, y) {
    this.x = x; this.y = y;
    this.w = TILE; this.h = TILE;
    this.vx = 1.5;
    this.vy = 0;
  }

  update(level) {
    this.x += this.vx;
    const ahead = {x: this.x + (this.vx > 0 ? this.w : -1), y: this.y, w: 1, h: this.h};
    if (level.isSolid(ahead)) {
      this.vx *= -1;
    }

    this.vy += level.gravity;
    this.y += this.vy;
    level.getColliders(this).forEach(r => {
      if (this.vy > 0 && this.y + this.h > r.y && this.y < r.y) {
        this.y = r.y - this.h;
        this.vy = 0;
      }
    });
  }

  draw(offset) {
    ctx.fillStyle = '#f00';
    ctx.fillRect(this.x - offset, this.y, this.w, this.h);
  }
}

class Level {
  constructor(map) {
    this.map = map;
    this.tiles = [];
    this.enemies = [];
    this.flag = null;
    this.start = {x:0,y:0};
    this.gravity = 0.5;
    this.width = map[0].length * TILE;
    this.parse();
  }

  parse() {
    for (let y=0; y<this.map.length; y++) {
      for (let x=0; x<this.map[y].length; x++) {
        const char = this.map[y][x];
        const rect = {x: x*TILE, y: y*TILE, w:TILE, h:TILE};
        if (char === 'G' || char === 'P') {
          this.tiles.push({...rect});
        } else if (char === 'E') {
          this.enemies.push(new Enemy(rect.x, rect.y));
        } else if (char === 'F') {
          this.flag = rect;
        } else if (char === 'S') {
          this.start = {x: rect.x, y: rect.y};
        }
      }
    }
  }

  getColliders(entity) {
    return this.tiles.filter(t =>
      entity.x < t.x + t.w &&
      entity.x + entity.w > t.x &&
      entity.y < t.y + t.h &&
      entity.y + entity.h > t.y
    );
  }

  isSolid(rect) {
    return this.tiles.some(t =>
      rect.x < t.x + t.w && rect.x + rect.w > t.x &&
      rect.y < t.y + t.h && rect.y + rect.h > t.y);
  }

  draw(offset) {
    ctx.fillStyle = '#654321';
    this.tiles.forEach(t => {
      ctx.fillRect(t.x - offset, t.y, t.w, t.h);
    });
    ctx.fillStyle = '#ff0';
    if (this.flag) {
      ctx.fillRect(this.flag.x - offset, this.flag.y, this.flag.w, this.flag.h);
    }
  }
}

const level = new Level(MAP);
const player = new Player(level.start.x, level.start.y);
const keys = {};
let win = false;

window.addEventListener('keydown', e => { keys[e.key] = true; });
window.addEventListener('keyup', e => { keys[e.key] = false; });

function update() {
  player.update(keys, level);
  level.enemies.forEach(e => e.update(level));
  level.enemies.forEach(e => {
    if (
      player.x < e.x + e.w && player.x + player.w > e.x &&
      player.y < e.y + e.h && player.y + player.h > e.y
    ) {
      // simple reset on collision
      player.x = level.start.x;
      player.y = level.start.y;
      player.vx = player.vy = 0;
    }
  });
  if (level.flag &&
      player.x < level.flag.x + level.flag.w && player.x + player.w > level.flag.x &&
      player.y < level.flag.y + level.flag.h && player.y + player.h > level.flag.y) {
    win = true;
  }
}

function draw() {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);
  const offset = Math.min(Math.max(0, player.x - WIDTH / 2), level.width - WIDTH);
  level.draw(offset);
  level.enemies.forEach(e => e.draw(offset));
  player.draw(offset);
  if (win) {
    ctx.fillStyle = '#fff';
    ctx.font = '40px sans-serif';
    const msg = 'You Win!';
    ctx.fillText(msg, WIDTH/2 - ctx.measureText(msg).width/2, HEIGHT/2);
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();
