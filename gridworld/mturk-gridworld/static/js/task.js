/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to
// they are not used in the stroop code but may be useful to you

// All pages to be loaded
var pages = [
    "instructions/instruct-1.html",
    "demonstrations.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
    "instructions/instruct-1.html"
];

function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// example for pictures
// colors1 = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
//           [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
//           [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
//           [0.6, 0.8, 0.6, 0.5, 0.5, 0.3, 0.5],
//           [0.8, 1.0, 0.8, 0.5, 0.3, 0.0, 0.3],
//           [0.6, 0.8, 0.6, 0.5, 0.5, 0.3, 0.5]];
// old, hand-designed
// colors1= [[0.5, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5],
//           [0.6, 1.0, 0.6, 0.5, 0.6, 1.0, 0.6],
//           [0.5, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5],
//           [0.5, 0.5, 0.5, 0.3, 0.5, 0.5, 0.5],
//           [0.5, 0.5, 0.3, 0.0, 0.3, 0.5, 0.5],
//           [0.5, 0.5, 0.5, 0.3, 0.5, 0.5, 0.5]];

// colors2= [[0.5, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5],
//           [0.6, 1.0, 0.6, 0.5, 0.6, 0.8, 0.6],
//           [0.5, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5],
//           [0.5, 0.5, 0.5, 0.3, 0.5, 0.5, 0.5],
//           [0.5, 0.5, 0.3, 0.0, 0.3, 0.5, 0.5],
//           [0.5, 0.5, 0.5, 0.3, 0.5, 0.5, 0.5]];

// colors3= [[0.5, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5],
//           [0.6, 0.8, 0.6, 0.5, 0.6, 1.0, 0.6],
//           [0.5, 0.6, 0.5, 0.5, 0.5, 0.6, 0.5],
//           [0.5, 0.5, 0.5, 0.3, 0.5, 0.5, 0.5],
//           [0.5, 0.5, 0.3, 0.0, 0.3, 0.5, 0.5],
//           [0.5, 0.5, 0.5, 0.3, 0.5, 0.5, 0.5]];

//new, rbf based
colors2= [[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.51,  0.52,  0.51,  0.5,   0.51,  0.52,  0.51,  0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.6,   0.52,  0.6,   0.72,  0.6,   0.51],
          [ 0.5,   0.52,  0.72,  1.,    0.72,  0.52,  0.72,  1.,    0.72,  0.52],
          [ 0.5,   0.51,  0.6,   0.72,  0.5,   0.29,  0.5,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.51,  0.5,   0.28,  0.,    0.28,  0.5,   0.51,  0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]
rewards= [[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.51,  0.52,  0.51,  0.5,   0.51,  0.52,  0.51,  0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.6,   0.52,  0.6,   0.72,  0.6,   0.51],
          [ 0.5,   0.52,  0.72,  1.,    0.72,  0.52,  0.72,  1.,    0.72,  0.52],
          [ 0.5,   0.51,  0.6,   0.72,  0.5,   0.29,  0.5,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.51,  0.5,   0.28,  0.,    0.28,  0.5,   0.51,  0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]

grids = [colors2];
shuffle(grids);

var TOTAL_MOVES = 15; //arbitrary for now
var m = colors2.length; // grid height
var n = colors2[0].length; // grid width
var indexToij = function(idx) {
    i = Math.floor(idx / m);
    j = idx % n;
    return [i, j];
}

var ijToIndex = function(i, j) {
    return (i * n) + j;
}

var indexToxy = function(idx) {
    element = document.getElementById("square-" + idx);
    var rect = element.getBoundingClientRect();
    x = (parseFloat(rect.left) + parseFloat(rect.right)) / 2;
    y = (parseFloat(rect.top) + parseFloat(rect.bottom)) / 2;
    return [x, y];
}

var getNeighbors = function(idx) {
    let neigh = new Set();
    if (idx % n != 0) { // if idx % n == 0, then at left side
        neigh.add(idx - 1);
    }
    if (idx % n != n-1) { // if idx % n == n-1, then at right side
        neigh.add(idx + 1);
    }
    if (Math.floor(idx / n) != 0) { // if floor(idx/n) == 0, then at top
        neigh.add(idx - n);
    }
    if (Math.floor(idx / n) != m-1) { // if floor(idx/n) == m-1, then at bottom
        neigh.add(idx + n);
    }
    return neigh;
}

var isNeighbor = function(idx1, idx2) {
    var neighbors = getNeighbors(idx1);
    return neighbors.has(idx2);
}

var numToColor = function(grid) {
    for (var i = 0; i < grid.length; i++) {
        for (var j = 0; j < grid[0].length; j++) {
            val = grid[i][j];
            // default white
            color = '#ffffff';
            if (val == 0.0) {
                // black
                color = '#000000';
            } else if (val == 0.27 || val == 0.28 || val == 0.29 || val == 0.3) {
                // dark gray
                color = '#444447';
            } else if (val == 0.4) {
                color = '#505050';
            } else if (val == 0.48 || val == 0.49 || val == 0.5) {
                // medium gray
                color = '#888991';
            } else if (val == 0.51 || val == 0.52) {
                color = '#909090';
            } else if (val == 0.6) {
                // light gray
                color = '#b0b1b7';
            } else if (val == 0.7 || val == 0.72) {
                //nearly white
                color = '#d6d7d8'
            }
            grid[i][j] = color;
        }
    }
}

/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/

var Experiment = function() {
    psiTurk.showPage('demonstrations.html');

    var reward = 0;
    var moves_left = TOTAL_MOVES;
    turns_finished = false;
    var grid_idx = 0;
    var colors;

    function colorGridSquares() {
        colors = grids[grid_idx];
        numToColor(colors);
        for (var i = 0; i < colors.length; i++) {
            for (var j = 0; j < colors[0].length; j++) {
                square = document.getElementById("square-" + ijToIndex(i, j));
                square.setAttribute('style', 'background-color: ' + colors[i][j] + ';');
            }
        }
    }

    function createLineElement(x, y, length, angle) {
        var line = document.createElement("line");
        var styles = 'border: 1px solid blue; '
                   + 'width: ' + length + 'px; '
                   + 'height: 0px; '
                   + '-moz-transform: rotate(' + angle + 'rad); '
                   + '-webkit-transform: rotate(' + angle + 'rad); '
                   + '-o-transform: rotate(' + angle + 'rad); '  
                   + '-ms-transform: rotate(' + angle + 'rad); '  
                   + 'position: absolute; '
                   + 'top: ' + y + 'px; '
                   + 'left: ' + x + 'px; ';
        line.setAttribute('style', styles);
        line.setAttribute('name', 'line');  
        return line;
    }

    function createLine(x1, y1, x2, y2) {
        var a = x1 - x2,
            b = y1 - y2,
            c = Math.sqrt(a * a + b * b);

        var sx = (x1 + x2) / 2,
            sy = (y1 + y2) / 2;

        var x = sx - c / 2,
            y = sy;

        var alpha = Math.PI - Math.atan2(-b, a);

        return createLineElement(x, y, c, alpha);
    }

    path = [55];

    prev_idx = 55;
    diameter = 20;
    var circle = document.createElement("circle");
    document.body.appendChild(circle);
    circle.classList.add("circle");
    circle.style.height = diameter + "px";
    circle.style.width = diameter + "px";
    circle.style.background = "blue";
    circle.style.position = "absolute";
    let [x, y] = indexToxy(prev_idx);
    circle.style.left = (x - diameter/2) + "px";
    circle.style.top = (y - diameter/2) + "px";

    updateScore = function() {
        d3.select("#score").text(reward.toFixed(2));
    }

    updateMoves = function() {
        if (moves_left <= 0) {
            turns_finished = true;
            document.getElementById("next").classList.remove("disabled");
            if (grid_idx == grids.length -1) {
                document.getElementById("finish").classList.remove("disabled");
            }
        }
        d3.select("#moves-left").text(moves_left);
    }

    resetScore = function() {
        reward = 0;
        updateScore();
    }

    resetMoves = function() {
        moves_left = TOTAL_MOVES;
        updateMoves();
    }


    connectPath = function(idx) {
        if (isNeighbor(prev_idx, idx) && !turns_finished) {
            let [i, j] = indexToij(idx);
            reward += rewards[i][j];
            moves_left -= 1;
            updateMoves();
            updateScore();
            path.push(idx);
            let [x, y] = indexToxy(idx);
            let [x1, y1] = indexToxy(prev_idx);
            document.body.appendChild(createLine(x, y, x1, y1));
            prev_idx = idx;
        }
    }

    standStill = function() {
        if (!turns_finished) {
            let [i, j] = indexToij(prev_idx);
            path.push(prev_idx);
            reward += rewards[i][j];
            moves_left -= 1;
            updateMoves();
            updateScore();
        }
    }

    clearAll = function() {
        var lines = document.getElementsByTagName("line");
        for (var i = 0, len = lines.length; i != len; ++i) {
            lines[0].parentNode.removeChild(lines[0]);
        }
        prev_idx = 55;
        path = [55];
        turns_finished = false;
        document.getElementById("next").classList.add("disabled");
        document.getElementById("finish").classList.add("disabled");
        resetMoves();
        resetScore();
    };

    next = function() {
        psiTurk.recordUnstructuredData('grid_' + grid_idx, colors);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        clearAll();
        grid_idx += 1;
        colorGridSquares();
        if (grid_idx == grids.length) {
            document.getElementById("finish").classList.remove("disabled");
            document.getElementById("next").classList.add("disabled");
        }
    }

    finish = function() {
        psiTurk.recordUnstructuredData('grid_' + grid_idx, colors);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        psiTurk.saveData();
        psiTurk.completeHIT();
    }

    colorGridSquares();
    updateScore();
    updateMoves();
};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
        instructionPages, // a list of pages you want to display in sequence
        function() { currentview = new Experiment(); } // what you want to do when you are done with instructions
    );
});
