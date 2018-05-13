// BY DEFAULT, WHEN PAGE IS LOADED, HIDE:
    // MANUAL MODE, 
    // CATEGORY DROPDOWN, 
    // EVENT EDIT SUBMIT BUTTON 

function initialize() {
    $(".form-register").hide();
    $(".goal-edit-submit").hide();
    $(".event-edit-submit").hide();
    $(".category-edit-submit").hide();
    $(".time-input").hide();

    // Apply select2 to dropdowns
    $(".category-dropdown").select2({placeholder: "select a category"});
    $("#new_category").select2({placeholder: "tv"});
    $(".goal-dropdown").select2();
    $("#category-goal-dropdown").select2({placeholder: "goals"});
    $(".goal-type-dropdown").select2();
}

function addEventListeners(){

    // SHOW/HIDE SAVE BUTTONS

    // Task
    // When the mouse hovers over the list item, show the Save button.
    $(".event-input-field").parents("li").hover(function() {
        $(this).children().children(".event-edit-submit").show();

    // When the mouse leaves the list item, hide the Save button.
        $(this).mouseleave(function() {
            $(this).children().children(".event-edit-submit").hide();
        });    
    });

    // Goal

        // When the mouse hovers over the list item, show the Save button.
        $(".goal-input-field").parents("li").hover(function() {
            $(this).children().children(".goal-edit-submit").show();

        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
                $(this).children().children(".goal-edit-submit").hide();
            });
        });

        // When the goal start time is clicked, show the datetime picker.
        $(".time-text").click(function() {
            $(this).parents().children(".time-text").hide()
            $(this).parents("span").children(".time-input").show();


            $(this).parents("li").mouseleave(function(){
                $(this).children(".time-input").hide();
                $(this).children(".time-text").show();
            })
        });


    // Category
    // When the mouse hovers over the list item, show the Save button.
    $(".category-input-field").parents("li").hover(function() {
        $(this).children().children(".category-edit-submit").show();

    // When the mouse leaves the list item, hide the Save button.
        $(this).mouseleave(function() {
            $(this).children().children(".category-edit-submit").hide();
        });
    });    

}

$(document).ready(function() {
   initialize(); 
   $("#datePickers").hide();
   addEventListeners();
});



// CUSTOMIZE DATEPICKERS WITH FLATPICKR
flatpickr(".date-time-picker", {
    enableTime: true,
    dateFormat: "Y-m-d h:i K",
    allowInput: true,
    altFormat: "F j, Y"
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


// UPDATE GOAL INFO AND SAVE
$(".goal-input").parents("form").children(".goal-edit-submit").on(
    "click", function() {
        console.log("saving goal")
        let formInputs = {
            "goalId": $(this).attr("name"),
            "newGoalName": $(this).parents("form").children("span.goal-input").children("span").children(".goal-name").val(),
            "newDays": $(this).parents("form").children("span.goal-input").children("span").children(".days").val(),
            "newHours":$(this).parents("form").children("span.goal-input").children("span").children(".hours").val(),
            "newMinutes":$(this).parents("form").children("span.goal-input").children("span").children(".minutes").val()
        }

        $.post("/edit_goal_info", formInputs);
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


// UPDATE CATEGORY LOG UPON ADDING NEW CATEGORY

$("#new_categorySubmit").on("click", function() {
        // fix this -- just add one new bullet instead of reloading the whole sheemer sheemer

    $("#new_category-log").load("goals.html #new_category-log");
});


// ADD NEW GOAL
function addNewGoal(result){
    $("#goal-log-ul").prepend(result);

    $("#goalName").removeAttr("value");
    $("#hours").removeAttr("value");
    $("#minutes").removeAttr("value");
    $("#startDate").removeAttr("value");
    $("#endDate").removeAttr("value");
    initialize();

}

$("#goalSubmit").on("click", function() {
    event.preventDefault();
    
    let formInputs = {
        "goalName": $("#goalName").val(),
        "goalType": $("#goalType").val(),
        "hours": $("#hours").val(),
        "minutes": $("#minutes").val(),
        "startDate": $("#startDate").val(),
        "endDate": $("#endDate").val()
    };

    $.post("/add_goal", formInputs, addNewGoal);
});


// ADD NEW EVENT
function addNewEvent(result) {   
    $("#event-log-ul").prepend(result);
    $("#new_task").removeAttr("value");
    $("#new_category").removeAttr("value");
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
            "task": $("#new_task").val(),
            "category": $("#new_category").val(),
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
            "task": $("#new_task").val(),
            "category": $("#new_category").val(),
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