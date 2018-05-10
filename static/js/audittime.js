// MANUAL ENTRY

$("#manualSubmit").on("click", function() {
    $("#event-log").load("userhome.html #event-log");    
})


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