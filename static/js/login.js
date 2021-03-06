// -------------- LOGIN / REGISTRATION FORM TOGGLE --------------

$(".signup-button").hover(function() {
    $(".signup-button").removeClass(".signup-button").addClass(".signup-button-hover")
});

$(".register-login-button").hover(function() {
    $(".register-login-button").removeClass(".register-login-button").addClass(".login-button-hover")
});

$(".signup-button").click(function() {
    $(".form-login").slideUp();
    $(".form-register").slideDown();
});

$(".register-login-button").click(function() {
    $(".form-login").slideDown();
    $(".form-register").slideUp();

});

// LOG IN FLOW

function displayLogInResults(result) {
    if (result === "success") {
        window.location = "/tasks";
    }
    
    else {
        toastr.warning("Wrong email or password. Try again.")
    }

}

function logIn() {
    let formInputs = {
        "email": $("#input-email").val(),
        "password": $("#input-password").val()
    };

    console.log(formInputs)

    $.post("/login_submit", 
           formInputs,
           displayLogInResults);
}

$("#login-button").click(function(event) {
    event.preventDefault();
    logIn();
});


// REGISTRATION

function redirectToTasks(result) {
    if (result === 'success') {
        toastr.success("You've successfully created your account.");
        window.location = "/tasks";
    }

    else if (result === 'already_exists') {
        toastr.warning("Someone's already signed up with that email address.")
    }

    else {
        toastr.warning("Whaaaaa cowabunga, dude!")
    }
}

function signUp() {

    let formInputs = {
        "name": $("#register-name").val(),
        "email": $("#register-email").val(),
        "password": $("#register-password").val()
    };

    $.post("/signup_submit", 
           formInputs,
           redirectToTasks);
}

$("#register-button").click(function(event) {
    event.preventDefault();
    signUp();
});