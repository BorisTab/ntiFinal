var cols, rows;
var w = 40;
var grid = [];
var matrix = [];

var mx = new Array(10);
for (var i = 0; i < mx.length; i++) {
    mx[i] = new Array(10);
}

for (var i = 0; i < 10; i++) {
    for (var j = 0; j < 10; j++) {
        mx[i][j] = 0;
    }
}

var current;
var stack = [];

function setup() {
    createCanvas(400, 400);

    cols = floor(width/w);
    rows = floor(height/w);

    for (let j = 0; j < rows; j++){
        for (let i = 0; i < cols; i++){
            var cell = new Cell(i, j);
            grid.push(cell);
        }
    }

    matrix = grid;
    current = grid[0];
}

current = grid[0];

function draw() {
    background(51);
    for (let i =0; i < grid.length; i++) {
        grid[i].show();
    }

    current.visited = true;
    current.highlight();
    var next = current.checkNeighbors();
    if (next){
        next.visited = true;
        stack.push(current);
        removeWalls(current, next);
        current = next;
    } else if (stack.length > 0){
        current = stack.pop();
    }
}

function index(i, j) {
    if (i < 0 || j < 0 || i > cols - 1 || j > rows -1){
        return -1;
    }
    return i + j * cols;
}

function Cell(i, j) {
    this.i = i;
    this.j = j;
    this.walls = [true, true, true, true];
    this.visited = false;

    this.checkNeighbors = function () {
        var neighbors = [];

        var top = grid[index(i, j - 1)];
        var right = grid[index(i + 1, j )];
        var bottom = grid[index(i, j + 1)];
        var left = grid[index(i - 1, j)];

        if (top && !top.visited) {
            neighbors.push(top);
        }
        if (right && !right.visited) {
            neighbors.push(right);
        }
        if (bottom && !bottom.visited) {
            neighbors.push(bottom);
        }
        if (left && !left.visited) {
            neighbors.push(left);
        }

        if (neighbors.length > 0){
            var r = floor(random(0, neighbors.length));
            return neighbors[r];
        } else {
            return undefined;
        }
    };

    this.checkNeighbors2 = function () {
        var neighbors = [];

        var top = matrix[index(i, j - 1)];
        var right = matrix[index(i + 1, j )];
        var bottom = matrix[index(i, j + 1)];
        var left = matrix[index(i - 1, j)];

        if (top && !top.visited) {
            neighbors.push(top);
        }
        if (right && !right.visited) {
            neighbors.push(right);
        }
        if (bottom && !bottom.visited) {
            neighbors.push(bottom);
        }
        if (left && !left.visited) {
            neighbors.push(left);
        }

        if (neighbors.length > 0){
            var r = floor(random(0, neighbors.length));
            return neighbors[r];
        } else {
            return undefined;
        }
    };

    this.highlight = function () {
        var x = this.i * w;
        var y = this.j * w;
        stroke(255);
        fill(0, 0, 255, 100);
        rect(x, y, w, w);
    };

    this.show = function () {
        var x = this.i * w;
        var y = this.j * w;
        stroke(255);

        if (this.walls[0]){
            line(x, y, x + w, y);
        }
        if (this.walls[1]) {
            line(x + w, y, x + w, y + w);
        }
        if (this.walls[2]) {
            line(x + w, y + w, x, y + w);
        }
        if (this.walls[3]) {
            line(x, y + w, x, y);
        }

        if (this.visited) {
            noStroke();
            fill(255, 0, 255, 100);
            rect(x, y, w, w);
        }
    }
}

function removeWalls(a, b) {
    var x = a.i - b.i;
    if (x === 1){
        a.walls[3] = false;
        b.walls[1] = false;
    } else if (x === -1){
        a.walls[1] = false;
        b.walls[3] = false;
    }

    var y = a.j - b.j;
    if (y === 1){
        a.walls[0] = false;
        b.walls[2] = false;
    } else if (y === -1){
        a.walls[2] = false;
        b.walls[0] = false;
    }
}

/*setTimeout(
function createMX() {

    for (var i = 0; i < 100; i++) {
        for (var k = 0; k < 4; k++) {
            if (grid[i].walls[k] === false) {
                mx[grid[i].i][grid[j].j] = 1;
            }
        }
    }
}, 5000);


console.log(mx);
console.log('cac');
*/

function findExit() {
    console.log('11');
    current = matrix[0];
    current.visited = true;

    var final = matrix[99];

    while (final !== current) {
        var next = current.checkNeighbors2();
        current.highlight();
        if (next){
            next.visited = true;
            stack.push(current);
            current = next;
        } else if (stack.length > 0){
            current = stack.pop();
        }
        console.log('ss');
    }
}


setTimeout(findExit, 5000);