// BY DEFAULT, WHEN PAGE IS LOADED, HIDE:
    // MANUAL MODE, 
    // CATEGORY DROPDOWN, 
    // EVENT EDIT SUBMIT BUTTON 

function initialize() {
    $(".form-register").hide();
    $(".category-dropdown").hide();
    $(".event-edit-submit").hide();
}
   

function addEventListeners(){

    // SHOW/HIDE SAVE BUTTON WHEN EDITING/NOT EDITING EVENT TASK
    $("span.task-input > span").on("click", function() {
        $(this).parents("form").children("span.event-edit-submit").show();

        $(this).parents("form").children("span.task-input").children(
            "span").children("input").on("focusout", function(event) {
                $(this).parents("form").children("span.event-edit-submit").hide();
        });
    
    });

    console.log("save button event listener has been added");

    // EXPAND CATEGORY DROPDOWN WHEN CATEGORY IS CLICKED ON TASK LOG
    $("span.category-title > span").on("click", function() {
        $(this).children("div").toggle();
    });

    console.log("category dropdown event listener has been added");
}

$(document).ready(function() {
   initialize(); 
   $("#datePickers").hide();
   addEventListeners();
});

// UPDATE TASK NAME AND SAVE
$("span.task-input").parents("form").children("span.event-edit-submit").on(
    "click", function() {
        let formInputs = {
            "eventId": $(this).parents("form").children("span.task-input").children("span").children("input").attr("name"),
            "newTaskName": $(this).parents("form").children("span.task-input").children("span").children("input").val()
        }

        $.post("/edit_task_name", formInputs);
    });

// ENABLE TOGGLING BETWEEN STOPWATCH / MANUAL MODES

$("#mode-toggler").on("click", function() {
    $("#startStop").toggle();
    $("#datePickers").toggle();
});


// UPDATE GOAL LOG UPON ADDING NEW GOAL

$("#goalSubmit").on("click", function() {
    $("#goal-log").load("goals.html #goal-log");
});


// UPDATE CATEGORY LOG UPON ADDING NEW CATEGORY

$("#categorySubmit").on("click", function() {
    $("#category-log").load("goals.html #category-log");
});


// ADD NEW EVENT
function addNewEvent(result) {   
    $("#event-log-ul").prepend(result);
    $("#task").removeAttr("value");
    $("#category").removeAttr("value");
    $("#m-start").removeAttr("value");
    $("#m-stop").removeAttr("value");
    $("#form-stopwatch").trigger("reset");
    initialize();
    $("#event-log-ul > li:first-child .category-title > span").on("click", function() {
        $(this).children().toggle();    
    });

    $("#event-log-ul > li:first-child .task-input > span").on("click", function() {
        $(this).parents("form").children("span.event-edit-submit").show();
        $(this).parents("form").children("span.task-input").children(
            "span").children("input").on("focusout", function(event) {
                $(this).parents("form").children("span.event-edit-submit").hide();
        });
    
    });

    console.log(result)
}

// SUBMIT EVENT - MANUAL
$("#manualSubmit").on("click", function() {
    event.preventDefault();
        let stopTime = Date.now();

        let formInputs = {
            "task": $("#task").val(),
            "category": $("#category").val(),
            "startTime": $("#m-start").val(),
            "stopTime": $("#m-stop").val()
        };

        $.post("/add_event", 
               formInputs,
               addNewEvent);
});

// SUBMIT EVENT - STOPWATCH

function startStopwatch(event) {
    event.preventDefault();
    let startTime = Date.now();
    console.log('Starting stopwatch...');
    console.log(startTime);

    $("#stopButton").on("click", function() {
        event.preventDefault();
        let stopTime = Date.now();

        let formInputs = {
            "task": $("#task").val(),
            "category": $("#category").val(),
            "startTime": startTime,
            "stopTime": stopTime
        };

        $.post("/add_event", 
               formInputs,
               addNewEvent);
    });
}

$("#startButton").on("click", startStopwatch);


// ENABLE TOGGLING BETWEEN LOGIN AND REGISTRATION FORMS

$("#signin-toggler").on("click", function() {
    $(".form-signin").toggle();
    $(".form-register").toggle();

    if ($("#signin-toggler").text() == "REGISTER") {
        $("#signin-toggler").text("SIGN IN");
    } else if ($("#signin-toggler").text() == "SIGN IN") {
        $("#signin-toggler").text("REGISTER");
    }
});


// REGISTRATION

function displayRegisterResults(result) {
    $("#butter").html("your account has been created. you are now logged in.")
    $("#login").hide()
    $("#register").hide()
}

function register(evt) {
    evt.preventDefault();
    console.log('hes')

    let formInputs = {
        "name": $("#registerName").val(),
        "email": $("#registerEmail").val(),
        "password": $("#registerPassword").val()
    };

    $.post("/register", 
           formInputs,
           displayRegisterResults);
}

$(".form-register").on("submit", register);


// SIGN IN FLOW

function displaySignInResults(result) {
    if (result === "success") {
        $("#butter").html("you've successfully signed in.")
        $("#login").hide()
        $("#register").hide()
    }
    
    else {
        $('form :input').val('');
        $("#butter").html("wrong email or password. try again.")
    }

}

function signIn(evt) {
    evt.preventDefault();
    console.log('heasdfasfsafs')

    var formInputs = {
        "email": $("#inputEmail").val(),
        "password": $("#inputPassword").val()
    };

    console.log(formInputs)

    $.post("/signin", 
           formInputs,
           displaySignInResults);
}

$(".form-signin").on("submit", signIn);