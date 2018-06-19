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
    "instructions/instruct-2.html",
    "practice.html",
    "demonstrations.html",
    "postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
    "instructions/instruct-1.html",
    "instructions/instruct-2.html"
];

// orders a according to order
function match_shuffle(a, order) {
    var ret = [];
    for (i = 0; i < order.length; i++) {
        ret.push(a[order[i]]);
    }
    return ret;
}
function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// currently both practice scenarios are the same
practice_colors1 = [[ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.]];
practice_rewards1= [[ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.]];

practice_colors2 = [[ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.]];
practice_rewards2= [[ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1., -1.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0., 0.5, 0.5,  0.,  0.,  0.,  0.,  0.]];

practice_grids = [practice_colors1, practice_colors2];
practice_rewards = [practice_rewards1, practice_rewards2];

//Make sure color and reward are shuffled the same way
var shuffle_order = shuffle(_.range(grids.length));
psiTurk.recordUnstructuredData("grid_order", shuffle_order);

grids = match_shuffle(grids, shuffle_order);
all_rewards = match_shuffle(all_rewards, shuffle_order);

var TOTAL_MOVES = 50; //arbitrary for now
var m = grids[0].length; // grid height
var n = grids[0][0].length; // grid width

var indexToij = function(idx) {
    // idx: 0-indexed cell number of m by n grid (left to right top to bottom)
    i = Math.floor(idx / m);
    j = idx % n;
    return [i, j];
}

var ijToIndex = function(i, j) {
    // takes in matrix indices, returns 0-indexed cell number
    return (i * n) + j;
}

var indexToxy = function(idx) {
    // gets x, y position of center of square on grid given by idx
    element = document.getElementById("square-" + idx);
    var rect = element.getBoundingClientRect();
    x = (parseFloat(rect.left) + parseFloat(rect.right)) / 2;
    y = (parseFloat(rect.top) + parseFloat(rect.bottom)) / 2;
    return [x, y];
}

var getNeighbors = function(idx) {
    // gets indices of 4 neighboring squares
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

var numToColorRBF = function(grid) {
    // for values generated by cirl_example/rbf_testing.py
    // converts decimal to hex color
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
            } else if (val == 0.4 || val == 0.41 || val == 0.42) {
                color = '#505050';
            } else if (val == 0.48 || val == 0.49 || val == 0.5) {
                // medium gray
                color = '#888991';
            } else if (val == 0.51 || val == 0.52) {
                color = '#909090';
            } else if (val == 0.54 || val == 0.55) {
                color = '#a0a0a0'
            } else if (val == 0.6 || val == 0.61) {
                // light gray
                color = '#b0b1b7';
            } else if (val == 0.7 || val == 0.72) {
                //nearly white
                color = '#d6d7d8'
            } else if (val == 0.75) {
                color = '#e2e2e2'
            }
            grid[i][j] = color;
        }
    }
}

var start_loc = ijToIndex(5, 0);
var goal_loc = ijToIndex(5, 9);

var numToColor = function(grid) {
    // for grids created by create_grid.py script
    // changes grid to contain strings with hex colors based on reward values
    for (var i = 0; i < grid.length; i++) {
        for (var j = 0; j < grid[0].length; j++) {
            val = grid[i][j];
            if (val == -1.0) {
                // black
                color = "#000000";
            } else if (val == -0.5) {
                // dark gray
                color = "#404040";
            } else if (val == 0.0) {
                // neutral, default gray
                color = "#7f7f7f";
            } else if (val == 0.5) {
                // light gray
                color = "#bfbfbf";
            } else if (val == 1.0) {
                // white
                color = "#ffffff";
            }

            if (ijToIndex(i, j) == goal_loc) {
                // red goal
                color = "#ff0000";
            } else if (ijToIndex(i, j) == start_loc) {
                // blue start
                color = "#0000ff";
            }
            grid[i][j] = color;
        }
    }
} 
// code to read from json file for grids, instead of hard-coding at top
// still needs to be implemented in Practice and Experiment
var grids = [];
var all_rewards = [];
var starts = [];
var goals = [];
var reward_parameters = [];
var living_rewards = [];

function callback() {
  grids = match_shuffle(grids, shuffle_order);
  all_rewards = match_shuffle(all_rewards, shuffle_order);
  starts = match_shuffle(starts, shuffle_order);
  goals = match_shuffle(goals, shuffle_order);
  reward_parameters = match_shuffle(reward_parameters, shuffle_order);
  living_rewards = match_shuffle(living_rewards, shuffle_order);
}

var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var obj = JSON.parse(this.responseText);
        colors_test = obj["colors_0"];
        for (i = 0; i < 16; i++) {
          grids.push(obj["colors_" + String(i)]);
          all_rewards.push(obj["rewards_" + String(i)]);
          starts.push(obj["start_" + String(i)]);
          goals.push(obj["goal_" + String(i)]);
          reward_parameters.push(obj["reward_values_" + String(i)]);
          living_rewards.push(obj["living_rewards_" + String(i)]);
        }
        callback();
    }
};
// flask looks in templates/ by default, so test.txt lives there
xmlhttp.open("GET", "test.txt", true);
xmlhttp.send();
/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/

var Practice = function() {
    psiTurk.showPage('practice.html');

    var reward = 0.0;
    var moves_made = 0;
    var turns_finished = false;
    var goal_reached = false;
    var grid_idx = 0;
    var colors;
    var rewards;

    function colorGridSquares() {
        colors = practice_grids[grid_idx];
        rewards = practice_rewards[grid_idx];
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

    path = [start_loc];
    prev_idx = start_loc;

    updateScore = function() {
        // displays current score with 2 decimal places
        d3.select("#score").text(reward.toFixed(2));
    }

    updateMoves = function() {
        // d3.select("#moves-made").text(moves_made);
        return true;
    }

    resetScore = function() {
        reward = 0.0;
        updateScore();
    }

    resetMoves = function() {
        moves_made = 0;
        updateMoves();
    }

    goalReached = function() {
        goal_reached = true;
        if (grid_idx == practice_grids.length -1) {
            alert("You've reached the goal! Click 'Finish Practice' to continue or 'Clear All' to retry this scenario.");
            document.getElementById("finish").classList.remove("disabled");
        } else {
            alert("You've reached the goal! Click 'Next' to continue or 'Clear All' to retry this scenario.");
            document.getElementById("next").classList.remove("disabled");
        }
    }

    moveCircletoPosition = function(idx) {
      let [x, y] = indexToxy(idx);
      circle.style.left = (x - width/2) + "px";
      circle.style.top = (y - height/2) + "px";
    }

    connectPath = function(idx) {
        // checks if the index clicked is a neighbor of the previous index (ie is valid next move) 
        // and the goal hasn't been reached 
        // turns_finished is no longer used, but is always false so does not matter
        if (isNeighbor(prev_idx, idx) && !turns_finished && !goal_reached) {
            if (idx == goal_loc) {
                goalReached();
            }
            let [i, j] = indexToij(idx);
            reward += rewards[i][j];
            moves_made += 1;
            if (updateMoves()) {
                updateScore();
                path.push(idx);
                let [x, y] = indexToxy(idx);
                let [x1, y1] = indexToxy(prev_idx);
                document.body.appendChild(createLine(x, y, x1, y1));
                // draw circle at current idx
                moveCircletoPosition(idx);
                prev_idx = idx;
            }
        }
    }

    standStill = function() {
        // allows user to collect reward for current tile without moving
        if (!turns_finished) {
            let [i, j] = indexToij(prev_idx);
            path.push(prev_idx);
            reward += rewards[i][j];
            moves_made += 1;
            updateMoves();
            updateScore();
        }
    }

    clearAll = function() {
        // removes all blue lines
        var lines = document.getElementsByTagName("line");
        for (var i = 0, len = lines.length; i != len; ++i) {
            lines[0].parentNode.removeChild(lines[0]);
        }
        // resets path to only include start location
        prev_idx = start_loc;
        path = [start_loc];
        turns_finished = false;
        goal_reached = false;
        // disable both next and finish buttons, one will be enabled once goal is reached
        document.getElementById("next").classList.add("disabled");
        document.getElementById("finish").classList.add("disabled");
        resetMoves();
        resetScore();
        moveCircletoPosition(start_loc);
    };

    next = function() {
        // save current practice grid, user's path and their total reward
        psiTurk.recordUnstructuredData('practice_grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('practice_path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('practice_reward_' + grid_idx, reward);
        grid_idx += 1;
        colorGridSquares();
        if (grid_idx == practice_grids.length) {
            // if no more grids, enable finish button and disable next button
            document.getElementById("finish").classList.remove("disabled");
            document.getElementById("next").classList.add("disabled");
        } else {
            // after first scenario
            alert("In the next scenario, imagine someone observes where you move but " + 
                  "can't see your score and does not know how much each color is worth. " + 
                  "How might you move so that it becomes clear what value each color " +
                  "square has? You want to teach them what these values are so that they " + 
                  "could do the task even when the squares are arranged very differently.");
            // change instructions text on the page
            d3.select("#instructions").text("Show someone who can't see the score and doesn't " +
                                            "know how much colors are worth the value of each color.");
        }
        // reset the view and recolor the grid with the environment
        clearAll();
    }

    finish = function() {
        // ask probing questions about putting themselves in observer's shoes
        answer1 = confirm("Do you think an observer would know which colors are good and which are bad?");
        answer2 = confirm("Do you think an observer could tell the relative value of each individual color?");
        // save answers, current practice grid, user's path and their total reward
        psiTurk.recordUnstructuredData('good_bad_colors_answer', answer1);
        psiTurk.recordUnstructuredData('relative_value_answer', answer2);
        psiTurk.recordUnstructuredData('practice_grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('practice_path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('practice_reward_' + grid_idx, reward);
        // switch view to actual experiment
        currentview = new Experiment();
        alert("Next, you will see " + String(grids.length) + " different scenarios. Again imagine " +
              "someone observes where you move but can't see your score and does not know " + 
              "how much each color is worth. Move in a way that it becomes clear what value each color " + 
              "square has. You want to teach them what these values are so that they could do the " + 
              "task even when the squares are arranged very differently.");
    }

    // initialzation, this is only run once

    colorGridSquares();
    updateScore();
    updateMoves();

    var circle = document.createElement("circle");
    circle.id = "current-position";
    document.body.appendChild(circle);
    circle.classList.add("circle");
    circle.style.background = "#f48942";
    circle.style.position = "absolute";
    let [x, y] = indexToxy(prev_idx);
    var width = circle.clientWidth;
    var height = circle.clientHeight;
    circle.style.left = (x - width/2) + "px";
    circle.style.top = (y - height/2) + "px";
}

var Experiment = function() {
    psiTurk.showPage('demonstrations.html');

    var reward = 0.0;
    var moves_made = 0;
    var turns_finished = false;
    var goal_reached = false;
    var grid_idx = 0;
    var colors;
    var rewards;

    function colorGridSquares() {
        colors = grids[grid_idx];
        rewards = all_rewards[grid_idx];
        start_loc = ijToIndex(starts[grid_idx][0], starts[grid_idx][1]);
        goal_loc = ijToIndex(goals[grid_idx][0], goals[grid_idx][1]);
        reward_values = reward_parameters[grid_idx];
        numToColor(colors);
        for (var i = 0; i < colors.length; i++) {
            for (var j = 0; j < colors[0].length; j++) {
                square = document.getElementById("square-" + ijToIndex(i, j));
                square.setAttribute('style', 'background-color: ' + colors[i][j] + ';');
            }
        }
        document.getElementById("black-value").innerText = String(reward_values[0]) + ",";
        document.getElementById("dark-gray-value").innerText = String(reward_values[1]) + ",";
        document.getElementById("gray-value").innerText = String(reward_values[2]) + ",";
        document.getElementById("light-gray-value").innerText = String(reward_values[3]) + ",";
        document.getElementById("white-value").innerText = String(reward_values[4]);
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

    path = [start_loc];
    prev_idx = start_loc;

    updateScore = function() {
        d3.select("#score").text(reward.toFixed(2));
    }

    updateMoves = function() {
        // d3.select("#moves-made").text(moves_made);
        return true;
    }

    resetScore = function() {
        reward = 0.0;
        updateScore();
    }

    resetMoves = function() {
        moves_made = 0;
        updateMoves();
    }

    goalReached = function() {
        goal_reached = true;
        if (grid_idx == grids.length -1) {
            alert("You've reached the goal! Click 'Finish' to finish the HIT or 'Clear All' to retry this scenario.");
            document.getElementById("finish").classList.remove("disabled");
        } else {
            alert("You've reached the goal! Click 'Next' to continue or 'Clear All' to retry this scenario.");
            document.getElementById("next").classList.remove("disabled");
        }
    }

    moveCircletoPosition = function(idx) {
      let [x, y] = indexToxy(idx);
      circle.style.left = (x - width/2) + "px";
      circle.style.top = (y - height/2) + "px";
    }

    connectPath = function(idx) {
        if (isNeighbor(prev_idx, idx) && !turns_finished && !goal_reached) {
            if (idx == goal_loc) {
                goalReached();
            }
            let [i, j] = indexToij(idx);
            reward += rewards[i][j];
            moves_made += 1;
            if (updateMoves()) {
                updateScore();
                path.push(idx);
                let [x, y] = indexToxy(idx);
                let [x1, y1] = indexToxy(prev_idx);
                document.body.appendChild(createLine(x, y, x1, y1));
                // draw circle at current idx
                moveCircletoPosition(idx);
                prev_idx = idx;
            }
        }
    }

    standStill = function() {
        if (!turns_finished) {
            let [i, j] = indexToij(prev_idx);
            path.push(prev_idx);
            reward += rewards[i][j];
            moves_made += 1;
            updateMoves();
            updateScore();
        }
    }

    clearAll = function() {
        var lines = document.getElementsByTagName("line");
        for (var i = 0, len = lines.length; i != len; ++i) {
            lines[0].parentNode.removeChild(lines[0]);
        }
        prev_idx = start_loc;
        path = [start_loc];
        turns_finished = false;
        goal_reached = false;
        document.getElementById("next").classList.add("disabled");
        document.getElementById("finish").classList.add("disabled");
        resetMoves();
        resetScore();
        moveCircletoPosition(start_loc);
    };

    next = function() {
        var strategy = prompt("Describe your strategy for teaching the value of the colors in this scenario.");
        psiTurk.recordUnstructuredData('strategy_' + grid_idx, strategy);
        psiTurk.recordUnstructuredData('grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('reward_' + grid_idx, reward);
        
        grid_idx += 1;
        colorGridSquares();
        if (grid_idx == grids.length) {
            document.getElementById("finish").classList.remove("disabled");
            document.getElementById("next").classList.add("disabled");
        }
        clearAll();
    }

    finish = function() {
        var strategy = prompt("Describe your strategy for teaching the value of the colors in this scenario.");
        psiTurk.recordUnstructuredData('strategy_' + grid_idx, strategy);
        psiTurk.recordUnstructuredData('grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('reward_' + grid_idx, reward);
        currentview = new Questionnaire();
    }

    colorGridSquares();
    updateScore();
    updateMoves();

    var circle = document.createElement("circle");
    circle.id = "current-position";
    document.body.appendChild(circle);
    circle.classList.add("circle");
    circle.style.background = "#f48942";
    circle.style.position = "absolute";
    let [x, y] = indexToxy(prev_idx);
    var width = circle.clientWidth;
    var height = circle.clientHeight;
    circle.style.left = (x - width/2) + "px";
    circle.style.top = (y - height/2) + "px";
};

var Questionnaire = function() {
    psiTurk.showPage('postquestionnaire.html');

    finish = function() {
        var comments = document.getElementById("comments").value;
        psiTurk.recordUnstructuredData('comments', comments);
        psiTurk.saveData({
            success: function() {
                psiTurk.completeHIT();
            }
        });
    }
}

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
        instructionPages, // a list of pages you want to display in sequence
        function() { currentview = new Practice(); } // what you want to do when you are done with instructions
    );
});
