// 定义弹球计数变量

const para = document.getElementById('score');
let count = 0;

// 设置画布

const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

const width = canvas.width = window.innerWidth;
const height = canvas.height = window.innerHeight;

// 生成随机数的函数

function random(min,max) {
  const num = Math.floor(Math.random() * (max - min)) + min;
  return num;
}

// 生成随机颜色值的函数

function randomColor() {
  return (
    "rgb(" +
    random(0, 255) +
    ", " +
    random(0, 255) +
    ", " +
    random(0, 255) +
    ")"
  );
}

// 定义 Shape 构造器

function Shape(x, y, velX, velY, exists) {
  this.x = x;
  this.y = y;
  this.velX = velX;
  this.velY = velY;
  this.exists = exists;
}

// 定义 Ball 构造器，继承自 Shape

function Ball(x, y, velX, velY, color, size, exists) {
  Shape.call(this, x, y, velX, velY, exists);  
  this.color = color;
  this.size = size;
}

/* 
设置 Ball 的原型为 Shape 的一个实例，这样 Ball 的实例就可以访问 Shape.prototype 上的方法
修正 constructor 属性，因为设置原型后其指向了 Shape
constructor属性是一个指向用于创建实例对象的构造函数的指针
在正常的构造函数定义中，constructor属性会自动设置为该构造函数。但是，当我们改变一个构造函数的prototype对象时，constructor属性不会自动更新
修改constructor允许我们在运行时准确地确定实例是由哪个构造函数创建的
*/
Ball.prototype = Object.create(Shape.prototype);
Ball.prototype.constructor = Ball; 

/* ES6语句
class Shape {  
  constructor(x, y, velX, velY, exists) {  
    this.x = x;  
    this.y = y;  
    this.velX = velX;  
    this.velY = velY;  
    this.exists = exists;  
  }  
}  
  
class Ball extends Shape {  
  constructor(x, y, velX, velY, exists, radius, color) {  
    super(x, y, velX, velY, exists); // 调用 Shape 的 constructor  
    this.radius = radius;  
    this.color = color;  
  
    // 可以在这里添加 Ball 特有的方法  
  }  
}  
  
// 现在可以创建 Ball 的实例了  
var ball = new Ball(10, 20, 1, 1, true, 5, 'red'); 
*/

// 定义彩球绘制函数

Ball.prototype.draw = function () {
  ctx.beginPath();
  ctx.fillStyle = this.color;
  ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
  ctx.fill();
};

// 定义彩球更新函数

Ball.prototype.update = function () {
  if (this.x + this.size >= width) {
    this.velX = -this.velX;
  }

  if (this.x - this.size <= 0) {
    this.velX = -this.velX;
  }

  if (this.y + this.size >= height) {
    this.velY = -this.velY;
  }

  if (this.y - this.size <= 0) {
    this.velY = -this.velY;
  }

  this.x += this.velX;
  this.y += this.velY;

};

// 定义碰撞检测函数

Ball.prototype.collisionDetect = function () {
  for (let j = 0; j < balls.length; j++) {
    if (this !== balls[j]) {
      const dx = this.x - balls[j].x;
      const dy = this.y - balls[j].y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < this.size + balls[j].size) {
        balls[j].color = this.color = randomColor();
      }
    }
  }
};

// 定义 EvilCircle 构造器，继承自 Shape

function EvilCircle(x, y, exists, color = 'white', size = 10, lineWidth = 5) {
  Shape.call(this, x, y, 20, 20, exists);  
  // 允许通过参数设置颜色，但默认为 'white'，是ES6的默认参数功能
  this.color = color; 
 // 直接将 color 设置为 'white'(this.color = 'white'; )时，去掉上面构造函数的参数color = 'white'  
  this.size = size;
  this.lineWidth = lineWidth;
}
EvilCircle.prototype = Object.create(Shape.prototype); 
EvilCircle.prototype.constructor = EvilCircle; 

// 定义 EvilCircle 绘制方法

EvilCircle.prototype.draw = function () {
	  ctx.beginPath();
	  ctx.lineWidth = this.lineWidth;
	  ctx.strokeStyle = this.color;
	  ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
	  ctx.stroke();
	};

// 定义 EvilCircle 的边缘检测（checkBounds）方法

EvilCircle.prototype.checkBounds = function () {
	  if (this.x + this.size >= width) {
		this.x = width - this.size - this.lineWidth;
	  }

	  if (this.x - this.size <= 0) {
		this.x = this.size + this.lineWidth;
	  }

	  if (this.y + this.size >= height) {
		this.y = height - this.size - this.lineWidth;
	  }

	  if (this.y - this.size <= 0) {
		this.y = this.size + this.lineWidth;
	  }
	};	
	
/*在JavaScript中，如果你在一个对象的方法中设置一个事件监听器（如window.onkeydown），并且在该事件监听器的回调函数中使用了this关键字，
  那么this通常不会指向你期望的对象（即调用该方法的对象EvilCircle）。
  相反，它通常会指向触发事件的对象（在这种情况下是window对象）*/
/*为了解决这个问题，一种常见的做法是在方法内部创建一个变量（如_this）来保存对外部this的引用，这样你就可以在回调函数内部使用这个变量来访问外部this
  EvilCircle.prototype.setControls = function () {  
  var _this = this;保存对外部this的引用
  window.onkeydown = function(e) {  
  后续使用_this来访问EvilCircle实例的属性    */
/*为了解决这个问题，另一种做法是使用箭头函数，可以简化这个过程，因为箭头函数不会绑定自己的this，它会捕获其所在上下文的this值。
  确保箭头函数在setControls方法的作用域内定*/
 
// 定义 EvilCircle 控制设置（setControls）方法
 
EvilCircle.prototype.setControls = function () {
  window.onkeydown = (e) => {
  const key = e.key.toUpperCase();  
  switch (key) {
    case "A":
	case "ARROWLEFT":
      this.x -= this.velX;
      break;
    case "D":
	case "ARROWRIGHT":
      this.x += this.velX;
      break;
    case "W":
	case "ARROWUP": 
      this.y -= this.velY;
      break;
    case "S":
	case "ARROWDOWN":
      this.y += this.velY;
      break;
	}
  };
};

// 定义 EvilCircle 冲突检测函数

EvilCircle.prototype.collisionDetect = function () {
  for (let j = 0; j < balls.length; j++) {
    if (balls[j].exists) {
      const dx = this.x - balls[j].x;
      const dy = this.y - balls[j].y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < this.size + balls[j].size) {
        balls[j].exists = false;
		count--;
		para.textContent = '剩余' + count + '个球';
      }
    } 
  }
  if (balls.every(ball => !ball.exists)) {  
    showGameOverAndRestartButtons();  
  }  
};

//定义游戏结束逻辑

function showGameOverAndRestartButtons() {  
  const gameOverElement = document.createElement('p');  
  gameOverElement.textContent = '游戏结束';  
  gameOverElement.style.position = 'fixed'; 
  gameOverElement.style.top = '50%'; 
  gameOverElement.style.left = '50%'; 
  gameOverElement.style.transform = 'translate(-50%, -50%)';  
  gameOverElement.style.color = '#aaa'; 
  gameOverElement.style.zIndex = 1000;  
  gameOverElement.style.display = 'block'; 
  
  const restartButton = document.createElement('button');  
  restartButton.textContent = '重新开始';  
  restartButton.style.position = 'fixed'; 
  restartButton.style.bottom = '10px'; 
  restartButton.style.right = '10px'; 
  restartButton.style.zIndex = 1000; 
  restartButton.style.display = 'block'; 
  
  document.body.appendChild(gameOverElement);  
  document.body.appendChild(restartButton);  
  
  restartButton.addEventListener('click', function() {  
    resetGame();  
    gameOverElement.style.display = 'none';  
    restartButton.style.display = 'none'; 
  });
}  
  
function resetGame() {  
  balls.forEach(ball => ball.exists = true);  
}

// 定义一个数组，生成并保存所有的球

let balls = [];

while (balls.length < 3) {
  let size = random(10, 20);
  let ball = new Ball(
    // 为避免绘制错误，球至少离画布边缘球本身一倍宽度的距离
    random(0 + size, width - size),
    random(0 + size, height - size),
    random(-7, 7),
    random(-7, 7),
    randomColor(),
    size,
	true
  );
  balls.push(ball);
  count++;
  para.textContent = '剩余' + count + '个球';
}

let evilCircle = new EvilCircle(width/2, height - 15, true);
  
evilCircle.setControls();

// 定义一个循环来不停地播放

function loop() {
  ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
  ctx.fillRect(0, 0, width, height);

  for (let i = 0; i < balls.length; i++) {
	if(balls[i].exists){
      balls[i].draw();
      balls[i].update();
	  balls[i].collisionDetect();
	  evilCircle.collisionDetect();
	}
  }
  evilCircle.draw();
  evilCircle.checkBounds();

  requestAnimationFrame(loop);
}
loop();

