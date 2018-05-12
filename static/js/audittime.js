
// SHOW SAVE BUTTON WHEN EDITING EVENT TASK
// HIDE SAVE BUTTON WHEN NOT EDITING EVENT TASK
$("span.task-input > span").on("click", function() {
    $(this).parents("form").children("button").show();
    $(this).on("focusout", function(event) {
        $(this).parents("form").children("button").hide();
    })
});


// EXPAND CATEGORY DROPDOWN WHEN CATEGORY IS CLICKED ON TASK LOG
$("span.category-title > span").on("click", function() {
    // $(".category-dropdown").toggle();
    $(this).children().toggle();
});


// BY DEFAULT, WHEN PAGE IS LOADED, HIDE:
    // MANUAL MODE, 
    // CATEGORY DROPDOWN, 
    // EVENT EDIT SUBMIT BUTTON 

$(document).ready(function() {
    $("#form-manual").hide();
    $(".form-register").hide();
    $(".category-dropdown").hide();
    $(".event-edit-submit").hide();
});


// ENABLE TOGGLING BETWEEN STOPWATCH / MANUAL MODES

$("#mode-toggler").on("click", function() {
    $("#form-stopwatch").toggle();
    $("#form-manual").toggle();
});


// UPDATE GOAL LOG UPON ADDING NEW GOAL

$("#goalSubmit").on("click", function() {
    $("#goal-log").load("goals.html #goal-log");
});


// UPDATE CATEGORY LOG UPON ADDING NEW CATEGORY

$("#categorySubmit").on("click", function() {
    $("#category-log").load("goals.html #category-log");
});

// MANUAL ENTRY

$("#manualSubmit").on("click", function() {
    $("#event-log").load("userhome.html #event-log");    
});


// STOPWATCH

function addNewEvent(result) {    
    $("#event-log").load("/user #event-log");
    $('#task').removeAttr('value');
    $('#category').removeAttr('value');
    $('#form-stopwatch').trigger('reset');

}

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

        console.log('i like to oat oat oat oples and banonos');

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