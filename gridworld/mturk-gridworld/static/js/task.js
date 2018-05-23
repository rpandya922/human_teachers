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
    "instructions/instruct-3.html",
    "practice.html",
    "demonstrations.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
    "instructions/instruct-1.html",
    "instructions/instruct-2.html",
    "instructions/instruct-3.html"
];

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
rbf_colors1= [[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.51,  0.52,  0.51,  0.5 ],
          [ 0.5,   0.5,   0.52,  0.54,  0.52,  0.51,  0.6,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.54,  0.6,   0.54,  0.5,   0.72,  1.,    0.72,  0.52],
          [ 0.5,   0.5,   0.52,  0.54,  0.42,  0.29,  0.5,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.5,   0.48,  0.28,  0.,    0.28,  0.5,   0.51,  0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]
rbf_rewards1=[[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.51,  0.52,  0.51,  0.5 ],
          [ 0.5,   0.5,   0.52,  0.54,  0.52,  0.51,  0.6,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.54,  0.6,   0.54,  0.5,   0.72,  1.,    0.72,  0.52],
          [ 0.5,   0.5,   0.52,  0.54,  0.42,  0.29,  0.5,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.5,   0.48,  0.28,  0.,    0.28,  0.5,   0.51,  0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]

rbf_colors2= [[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.51,  0.52,  0.51,  0.5,   0.51,  0.52,  0.51,  0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.6,   0.52,  0.6,   0.72,  0.6,   0.51],
          [ 0.5,   0.52,  0.72,  1.,    0.72,  0.52,  0.72,  1.,    0.72,  0.52],
          [ 0.5,   0.51,  0.6,   0.72,  0.5,   0.29,  0.5,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.51,  0.5,   0.28,  0.,    0.28,  0.5,   0.51,  0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]
rbf_rewards2=[[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.51,  0.52,  0.51,  0.5,   0.51,  0.52,  0.51,  0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.6,   0.52,  0.6,   0.72,  0.6,   0.51],
          [ 0.5,   0.52,  0.72,  1.,    0.72,  0.52,  0.72,  1.,    0.72,  0.52],
          [ 0.5,   0.51,  0.6,   0.72,  0.5,   0.29,  0.5,   0.72,  0.6,   0.51],
          [ 0.5,   0.5,   0.51,  0.5,   0.28,  0.,    0.28,  0.5,   0.51,  0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]

rbf_colors3= [[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.51,  0.52,  0.51,  0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.6,   0.51,  0.52,  0.54,  0.52,  0.5 ],
          [ 0.5,   0.52,  0.72,  1.,    0.72,  0.5,   0.54,  0.6,   0.54,  0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.5,   0.29,  0.42,  0.54,  0.52,  0.5 ],
          [ 0.5,   0.5,   0.51,  0.5,   0.28,  0.,    0.28,  0.48,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]
rbf_rewards3=[[ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.51,  0.52,  0.51,  0.5,   0.5,   0.5,   0.5,   0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.6,   0.51,  0.52,  0.54,  0.52,  0.5 ],
          [ 0.5,   0.52,  0.72,  1.,    0.72,  0.5,   0.54,  0.6,   0.54,  0.5 ],
          [ 0.5,   0.51,  0.6,   0.72,  0.5,   0.29,  0.42,  0.54,  0.52,  0.5 ],
          [ 0.5,   0.5,   0.51,  0.5,   0.28,  0.,    0.28,  0.48,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.49,  0.4,   0.27,  0.4,   0.49,  0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.49,  0.48,  0.49,  0.5,   0.5,   0.5 ],
          [ 0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5 ]]

colors_ex = [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  1.,  1.,  0., -1., -1.,  0.,  0.,  0.],
             [ 0.,  0.,  1.,  1.,  0., -1., -1.,  0.,  0.,  0.],
             [ 0.,  0.,  1.,  1.,  0., -1., -1.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];
rewards_ex= [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  1.,  1.,  0., -1., -1.,  0.,  0.,  0.],
             [ 0.,  0.,  1.,  1.,  0., -1., -1.,  0.,  0.,  0.],
             [ 0.,  0.,  1.,  1.,  0., -1., -1.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
             [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];

colors1 = [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];
rewards1 =[[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];

colors2 = [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  1. ,  1. ,  1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  1. ,  1. ,  1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];
rewards2= [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  1. ,  1. ,  1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  1. ,  1. ,  1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];

colors3 = [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.]];
rewards3= [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1., -1., -1.,  0.,  0.,  0.,  0.]];

colors4 = [[ 0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ,  0. ]];
rewards4= [[ 0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ,  0. ]];

colors5 = [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];
rewards5= [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];

colors6 = [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. ,  0. , -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. ,  0. , -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. ,  0. , -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];
rewards6= [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. ,  0. , -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. ,  0. , -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. , -1. , -1. ,  0. , -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];

colors7 = [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. , -1. , -1. , -1. ,  1. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. , -1. , -1. , -1. ,  1. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5, -0.5, -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5, -0.5, -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];
rewards7= [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. , -1. , -1. , -1. ,  1. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. , -1. , -1. , -1. ,  1. ,  1. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5, -0.5, -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5, -0.5, -0.5, -0.5,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];

colors8 = [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];
rewards8= [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -0.5, -0.5, -0.5,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];

colors9 = [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  1. ,  1. ,  1. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  1. ,  1. ,  1. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];
rewards9= [[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  1. ,  1. ,  1. ,  0. ],
           [ 0. ,  0. ,  0.5,  0.5,  0.5,  0. ,  1. ,  1. ,  1. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. , -1. , -1. , -1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ]];

// currently both practice scenarios are the same
practice_colors1 = [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];
practice_rewards1= [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];

practice_colors2 = [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];
practice_rewards2= [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0., -1., -1.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                    [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]];

practice_grids = [practice_colors1, practice_colors2];
practice_rewards = [practice_rewards1, practice_rewards2];

grids = [colors1, colors2, colors3, colors4, colors5, colors6, colors7, colors8, colors9];
all_rewards = [rewards1, rewards2, rewards3, rewards4, rewards5, rewards6, rewards7, rewards8, rewards9];

//Make sure color and reward are shuffled the same way
var shuffle_order = shuffle(_.range(grids.length));
// var shuffle_order = _.range(grids.length)  // TODO: change back to actual shuffle for experiments
grids = match_shuffle(grids, shuffle_order);
all_rewards = match_shuffle(all_rewards, shuffle_order);

var TOTAL_MOVES = 50; //arbitrary for now
var m = grids[0].length; // grid height
var n = grids[0][0].length; // grid width
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

var numToColorRBF = function(grid) {
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
        d3.select("#score").text(reward.toFixed(2));
    }

    updateMoves = function() {
        d3.select("#moves-made").text(moves_made);
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
    };

    next = function() {
        psiTurk.recordUnstructuredData('grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('reward_' + grid_idx, reward);
        clearAll();
        grid_idx += 1;
        colorGridSquares();
        if (grid_idx == practice_grids.length) {
            document.getElementById("finish").classList.remove("disabled");
            document.getElementById("next").classList.add("disabled");
        } else {
            alert("In the next scenario, imagine someone observes where you move but " + 
                  "cannot see the colors on the grid. How would you show them how to get " +
                  "the highest score?");
            d3.select("#instructions").text("Show someone how to get a high score");
        }
    }

    finish = function() {
        psiTurk.recordUnstructuredData('practice_grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('practice_path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('practice_reward_' + grid_idx, reward);
        currentview = new Experiment();
        alert("Next, you will see " + String(grids.length) + " different scenarios. Again imagine " +
              "someone observes where you move but cannot see the colors on the grid. Move in a way " +
              "that would show them how to get a high score.");
    }

    colorGridSquares();
    updateScore();
    updateMoves();
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
        d3.select("#score").text(reward.toFixed(2));
    }

    updateMoves = function() {
        // if (moves_left <= 0 && !goal_reached) {
        //     alert("You need to reach the goal within " + String(TOTAL_MOVES) + " turns! Click 'Ok' to restart.");
        //     clearAll();
        //     // need to signal to conectPath not to actually add idx to path
        //     return false;
        // }
        // if (moves_left <= 0) {
        //     turns_finished = true;
        //     if (grid_idx == grids.length -1) {
        //         document.getElementById("finish").classList.remove("disabled");
        //     } else {
        //         document.getElementById("next").classList.remove("disabled");
        //     }
        // }
        d3.select("#moves-made").text(moves_made);
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
    };

    next = function() {
        psiTurk.recordUnstructuredData('grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('reward_' + grid_idx, reward);
        clearAll();
        grid_idx += 1;
        colorGridSquares();
        if (grid_idx == grids.length) {
            document.getElementById("finish").classList.remove("disabled");
            document.getElementById("next").classList.add("disabled");
        }
    }

    finish = function() {
        psiTurk.recordUnstructuredData('grid_' + grid_idx, rewards);
        psiTurk.recordUnstructuredData('path_' + grid_idx, path);
        psiTurk.recordUnstructuredData('reward_' + grid_idx, reward);
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
        function() { currentview = new Practice(); } // what you want to do when you are done with instructions
    );
});
