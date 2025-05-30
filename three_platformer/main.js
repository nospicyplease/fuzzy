import * as THREE from 'https://unpkg.com/three@0.162.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.162.0/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb); // sky blue

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 5);
light.castShadow = true;
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// player
const playerSize = 1;
const playerGeo = new THREE.BoxGeometry(playerSize, playerSize * 2, playerSize);
const playerMat = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const player = new THREE.Mesh(playerGeo, playerMat);
player.castShadow = true;
player.position.set(0, 1, 0);
scene.add(player);

// ground
const groundGeo = new THREE.BoxGeometry(20, 1, 20);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x228b22 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.receiveShadow = true;
ground.position.set(0, -0.5, 0);
scene.add(ground);

// platforms
const platforms = [];
function addPlatform(x, y, z) {
  const geo = new THREE.BoxGeometry(4, 0.5, 4);
  const mat = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(x, y, z);
  mesh.receiveShadow = true;
  scene.add(mesh);
  platforms.push(mesh);
}
addPlatform(5, 2, -2);
addPlatform(-4, 4, -5);
addPlatform(8, 6, -8);

// flagpole
const flagGeo = new THREE.CylinderGeometry(0.1, 0.1, 3);
const flagMat = new THREE.MeshStandardMaterial({ color: 0xffff00 });
const flag = new THREE.Mesh(flagGeo, flagMat);
flag.position.set(10, 1.5, -10);
scene.add(flag);

const keys = {};
window.addEventListener('keydown', e => keys[e.code] = true);
window.addEventListener('keyup', e => keys[e.code] = false);

const velocity = new THREE.Vector3();
let onGround = false;
const speed = 5;
const jumpSpeed = 8;
const gravity = 20;

const ui = document.getElementById('ui');
let won = false;

function updatePlayer(delta) {
  // horizontal movement
  const dir = new THREE.Vector3();
  if (keys['KeyW']) dir.z -= 1;
  if (keys['KeyS']) dir.z += 1;
  if (keys['KeyA']) dir.x -= 1;
  if (keys['KeyD']) dir.x += 1;
  dir.normalize();
  dir.applyAxisAngle(new THREE.Vector3(0,1,0), camera.rotation.y);
  player.position.addScaledVector(dir, speed * delta);

  // jump
  if (keys['Space'] && onGround) {
    velocity.y = jumpSpeed;
    onGround = false;
  }

  // apply gravity
  velocity.y -= gravity * delta;
  player.position.y += velocity.y * delta;

  // ground collision
  if (player.position.y <= 1) {
    player.position.y = 1;
    velocity.y = 0;
    onGround = true;
  }

  // platform collisions
  const box = new THREE.Box3().setFromObject(player);
  platforms.forEach(p => {
    const pBox = new THREE.Box3().setFromObject(p);
    if (box.intersectsBox(pBox) && velocity.y <= 0 && player.position.y >= p.position.y) {
      player.position.y = p.position.y + 1.25;
      velocity.y = 0;
      onGround = true;
    }
  });

  // reset if fall off
  if (player.position.y < -10) {
    player.position.set(0, 1, 0);
    velocity.set(0,0,0);
  }

  // check win
  if (!won) {
    const flagBox = new THREE.Box3().setFromObject(flag);
    if (box.intersectsBox(flagBox)) {
      won = true;
      ui.textContent = 'You Win!';
    }
  }
}

function updateCamera() {
  const offset = new THREE.Vector3(0, 5, 10);
  offset.applyAxisAngle(new THREE.Vector3(0,1,0), player.rotation.y);
  camera.position.copy(player.position).add(offset);
  camera.lookAt(player.position);
}

let prev = performance.now();
function animate() {
  const now = performance.now();
  const delta = (now - prev) / 1000;
  prev = now;
  updatePlayer(delta);
  updateCamera();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
