// START + STOP STOPWATCH, THEN DISPLAY DURATION.

function displayDuration(result) {
    $("#duration").html(result)
}

function useStopwatch(evt) {
    evt.preventDefault();
    console.log("starting stopwatch...")

    let startTime = Date.now();

    $("#stopButton").on("click", function() {
        evt.preventDefault();

        let stopTime = Date.now();

        let formInputs = {
            "start_time": startTime,
            "stop_time": stopTime,
            "task": $("#task").val(),
            "category": $("#category").val(),
        };

        $.post("/add_event", 
               formInputs,
               displayDuration);
    });

    
}

$("#startButton").on("click", useStopwatch);


// REGISTRATION

function displayRegisterResults(result) {
    $("#butter").html("your account has been created.")
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