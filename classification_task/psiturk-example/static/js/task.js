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
	//"instructions/instruct-3.html",
	"instructions/instruct-ready.html",
	"stage.html",
	"postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	"instructions/instruct-1.html",
	"instructions/instruct-2.html",
	//"instructions/instruct-3.html",
	"instructions/instruct-ready.html"
];


/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/

/********************
* STROOP TEST       *
********************/
var StroopExperiment = function() {

	var wordon, // time word is presented
	    listening = false;


	// Stimuli for a basic Stroop experiment
	/*var stims = [
			["SHIP", "red", "unrelated"],
		];*/

	//stims = _.shuffle(stims);

	/*var next = function() {
		if (stims.length===0) {
			finish();
		}
		else {
			stim = stims.shift();
			show_word( stim[0], stim[1] );
			wordon = new Date().getTime();
			listening = true;
			d3.select("#query").html('<p id="prompt">Press q to submit info.</p>');
		}
	};*/


	recordData = function() {
		el1 = document.getElementById("body1");
		el2 = document.getElementById("body2");
		h1 = el1.style.height;
		w1 = el1.style.width;
		h2 = el2.style.height;
		w2 = el2.style.width;
		var type;
		if (el1.offsetHeight > el1.offsetWidth) {
			t1 = "vespula";
		}
		else {
			t1 = "weevil";
		}

		if (el2.offsetHeight > el2.offsetWidth) {
			t2 = "vespula";
		}
		else {
			t2 = "weevil";
		}
		psiTurk.recordTrialData({'phase':"TEST",
		                 	     'bug one height': h1,
		                         'bug one width': w1,
		                         'bug one type': t1,
		                         'weevil height': h2,
		                         'weevil width': w2,
		                         'bug two type': t2,
		                      	  }
		                       );
		finish();
	}
	
	/*var response_handler = function(e) {
		if (!listening) return;

		var keyCode = e.keyCode,
			response;
		var enter;

		switch (keyCode) {
			case 81:
			//'q'
				enter = "quit";

			case 82:
				// "R"
				response="red";
				break;
			case 71:
				// "G"
				response="green";
				break;
			case 66:
				// "B"
				response="blue";
				break;
			default:
				response = "";
				break;
		}
		if (response.length>0) {
			listening = false;
			var hit = response == stim[1];
			var rt = new Date().getTime() - wordon;

			psiTurk.recordTrialData({'phase':"TEST",
                                     'word':stim[0],
                                     'color':stim[1],
                                     'relation':stim[2],
                                     'response':response,
                                     'hit':hit,
                                     'rt':rt}
                                   );
			remove_word();
			next();
		}
	};*/

	var button = document.createElement("button");
	button.innerHTML = "Do Something";

	// 2. Append somewhere
	var body = document.getElementsByTagName("body")[0];
	body.appendChild(button);

	// 3. Add event handler
	button.addEventListener ("click", function() {
	  next();
	});

	
	var finish = function() {
	    //$("body").unbind("keydown", response_handler); // Unbind keys
	    currentview = new Questionnaire();
	};
	
	/*var show_word = function(text, color) {
		d3.select("#stim")
			.append("div")
			.attr("id","word")
			.style("color",color)
			.style("text-align","center")
			.style("font-size","150px")
			.style("font-weight","400")
			.style("margin","20px")
			.text(text);
	};*/

	/*var remove_word = function() {
		d3.select("#word").remove();
	};*/

	
	// Load the stage.html snippet into the body of the page
	psiTurk.showPage('stage.html');

	// Register the response handler that is defined above to handle any
	// key down events.
	//$("body").focus().keydown(response_handler); 

	// Start the test
	//next();
};


/****************
* Questionnaire *
****************/

var Questionnaire = function() {

	var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

	record_responses = function() {

		psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'submit'});

		var feedback = document.getElementById("info").value;
		psiTurk.recordTrialData({'phase':'postquestionnaire', 'feedback':feedback});
		/*$('textarea').each( function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);
		});
		$('select').each( function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);		
		});*/

	};

	prompt_resubmit = function() {
		document.body.innerHTML = error_message;
		$("#resubmit").click(resubmit);
	};

	resubmit = function() {
		document.body.innerHTML = "<h1>Trying to resubmit...</h1>";
		reprompt = setTimeout(prompt_resubmit, 10000);
		
		psiTurk.saveData({
			success: function() {
			    clearInterval(reprompt); 
                psiTurk.computeBonus('compute_bonus', function(){
                	psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                }); 


			}, 
			error: prompt_resubmit
		});
	};

	// Load the questionnaire snippet 
	psiTurk.showPage('postquestionnaire.html');
	//psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'begin'});
	
	finish = function() {
        psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'submit'});

		var feedback = document.getElementById("info").value;
		psiTurk.recordTrialData({'phase':'postquestionnaire', 'feedback':feedback});
        psiTurk.completeHIT(); // when finished saving compute bonus, the quit
             
	}

	$("#next").click(function () {
	    record_responses();
	    psiTurk.saveData({
            success: function(){
                psiTurk.computeBonus('compute_bonus', function() { 
                	psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                }); 
            }, 
            error: prompt_resubmit});
	});
    
	
};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { currentview = new StroopExperiment(); } // what you want to do when you are done with instructions
    );
});
