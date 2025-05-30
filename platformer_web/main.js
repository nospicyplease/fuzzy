import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.152.0/build/three.module.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);

const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

const ambient = new THREE.AmbientLight(0xffffff, 0.3);
scene.add(ambient);
const light = new THREE.DirectionalLight(0xffffff, 0.8);
light.position.set(5, 10, 7);
light.castShadow = true;
scene.add(light);

const groundGeo = new THREE.BoxGeometry(40, 1, 40);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x228B22 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.receiveShadow = true;
ground.position.y = -0.5;
scene.add(ground);

const platformGeo = new THREE.BoxGeometry(4, 1, 4);
const platformMat = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
const platforms = [];
function addPlatform(x, y, z) {
  const mesh = new THREE.Mesh(platformGeo, platformMat);
  mesh.position.set(x, y, z);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  scene.add(mesh);
  platforms.push(mesh);
}
addPlatform(5, 2, 0);
addPlatform(10, 4, 0);
addPlatform(15, 6, 0);

const flagGeo = new THREE.BoxGeometry(0.2, 3, 0.2);
const flagMat = new THREE.MeshStandardMaterial({ color: 0xffff00 });
const flag = new THREE.Mesh(flagGeo, flagMat);
flag.position.set(20, 1.5, 0);
flag.castShadow = true;
scene.add(flag);

const playerGeo = new THREE.BoxGeometry(1, 2, 1);
const playerMat = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const player = new THREE.Mesh(playerGeo, playerMat);
player.castShadow = true;
player.position.set(0, 1, 0);
scene.add(player);

camera.position.set(-5, 3, 5);

const keys = {};
window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

const velocity = new THREE.Vector3();
let onGround = false;
const SPEED = 0.15;
const JUMP = 0.3;
const GRAVITY = 0.01;

function checkCollisions() {
  const playerBox = new THREE.Box3().setFromObject(player);
  onGround = false;
  platforms.concat([ground]).forEach(obj => {
    const box = new THREE.Box3().setFromObject(obj);
    if (playerBox.intersectsBox(box) && velocity.y <= 0) {
      player.position.y = box.max.y + 1;
      velocity.y = 0;
      onGround = true;
    }
  });
}

function checkWin() {
  const playerBox = new THREE.Box3().setFromObject(player);
  const flagBox = new THREE.Box3().setFromObject(flag);
  if (playerBox.intersectsBox(flagBox)) {
    alert('You win!');
    window.location.reload();
  }
}

function update() {
  if (keys['w']) player.position.z -= SPEED;
  if (keys['s']) player.position.z += SPEED;
  if (keys['a']) player.position.x -= SPEED;
  if (keys['d']) player.position.x += SPEED;
  if (keys[' '] && onGround) velocity.y = JUMP;

  velocity.y -= GRAVITY;
  player.position.y += velocity.y;

  checkCollisions();
  checkWin();

  const camTarget = new THREE.Vector3(player.position.x - 5, player.position.y + 4, player.position.z + 5);
  camera.position.lerp(camTarget, 0.1);
  camera.lookAt(player.position);
}

function animate() {
  requestAnimationFrame(animate);
  update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
