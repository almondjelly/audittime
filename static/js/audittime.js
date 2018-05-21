// BY DEFAULT, WHEN PAGE IS LOADED, HIDE:
    // MANUAL MODE, 
    // CATEGORY DROPDOWN, 
    // EVENT EDIT SUBMIT BUTTON 

function initialize() {
    $(".form-register").hide();
    $(".span-goal-edit").hide();
    $(".span-goal-archive").hide();
    $(".event-edit-submit").hide();
    $(".category-edit-submit").hide();
    $(".time-input").hide();
    $(".span-category-save").hide();
    $(".span-category-archive").hide();

    // Apply select2 to dropdowns
    $(".category-dropdown").select2({placeholder: "select a category"});
    $("#new_category").select2({placeholder: "tv"});
    $(".goal-dropdown").select2();
    $("#category-goal-dropdown").select2({placeholder: "goals"});
    $(".td-input-category-goals").select2({placeholder: "goals"});
    $(".gcal-categories").select2({placeholder: "category"});

    // Set toastr options
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-center",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
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

        // When the mouse hovers over the list item, show the Edit button.
        $(".goal-input-field").parents("li").hover(function() {
            $(this).children().children(".goal-edit-submit").show();

        // When the mouse leaves the list item, hide the Edit button.
            $(this).mouseleave(function() {
                $(this).children().children(".goal-edit-submit").hide();
            });
        });

        // When the goal/task time is clicked, show the datetime picker.
        $(".time-text").click(function() {
            $(this).parents().children(".time-text").hide();
            $(this).parents("span").children(".time-input").show();
        });

    // Category

        // When the mouse hovers over the list item, show the Save button.
        $(".tr-category").hover(function() {
            console.log("i wolke up");
            $(this).children(".td-category-save").children("span").show();
            $(this).children(".td-category-archive").children("span").show();

        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
                $(this).children(".td-category-save").children("span").hide();
                $(this).children(".td-category-archive").children("span").hide();
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
    dateFormat: "M j \\at h:i K",
    allowInput: true,
    altFormat: "F j, Y"
});


// ENABLE TOGGLING BETWEEN STOPWATCH / MANUAL MODES
$("#mode-toggler").on("click", function() {
    $("#startStop").toggle();
    $("#datePickers").toggle();
});


// ---------------------------------- GOALS ----------------------------------

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

$("#goal-submit").on("click", function() {
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


// EDIT GOAL INFO AND SAVE
$(".goal-edit-save").click(function() {
    console.log("saving goal")
    let formInputs = {
        "goalId": $(this).parents(".form-goal-id").children(".input-goal-id").val(),
        "newGoalName": $(this).parents(".modal-form").children(".td-goal-type").val(),
        "newType": $(this).parents(".modal-form").children(".goal-input-type").val(),
        "newDays": $(this).parents(".modal-form").children(".days").val(),
        "newHours": $(this).parents(".modal-form").children(".hours").val(),
        "newMinutes": $(this).parents(".modal-form").children(".minutes").val(),
        "newStartTime": $(this).parents(".modal-form").children(".input-goal-start-time").val(),
        "newEndTime": $(this).parents(".modal-form").children(".input-goal-end-time").val(),
        "newCategoryGoals": $(this).parents(".modal-form").children(".input-goal-start-time").val()
    }

    $.post("/edit_goal_info", formInputs);

    toastr.success("Goal Saved")

});


// -------------------------------- CATEGORIES --------------------------------

// ADD NEW CATEGORY

    function addNewCategory(result) {
        $("tbody").prepend(result);
        $("#form-category").trigger('reset');
        initialize();

        toastr.success("New Category Added");
    }

    $("#category-submit").on("click", function() {    

        let categoryGoals = '';

        $(this).parents("form").children("select").change(function() {
            $(this).children("option:selected").each(function() {
                categoryGoals += $(this).text() + '|';
            });
        }).trigger("change");


        let formInputs = {
            "categoryName": $(".input-category-new").val(),
            "categoryGoals": categoryGoals
        };

        $.post("/add_category", formInputs, addNewCategory);

    });


// EDIT CATEGORY INFO AND SAVE

$(".category-input").parents("form").children(".category-edit-submit").on(
    "click", function() {
        let newCategoryGoals = '';

        $(this).parents("form").children(".category-goal-title").children("span").children("select").change(function() {
            $(this).children("option:selected").each(function() {
                newCategoryGoals += $(this).text() + '|';
            });
        }).trigger("change");
        console.log("saving category");
        let formInputs = {
            "categoryId": $(this).attr("name"),
            "newcategoryName": $(this).parents("form").children(".category-input").children("span").children(".category-name").val(),
            "newCategoryGoals": newCategoryGoals
        };

        $.post("/edit_category_info", formInputs);

        toastr.success("Category Saved")

    });


// ARCHIVE CATEGORY

    function displayArchiveCategoryResults(result) {
        console.log(result);
    }

    $(".btn-category-archive").click(function() {
        let formInputs = {
            "categoryId": $(this).parents("tr").children(".input-category-id").val()
        };

        toastr.success("Category Archived");

        $.post("archive_category", formInputs, displayArchiveCategoryResults);
        $(this).parents("tr").hide();
    });


// ------------------------------ TASKS + EVENTS ------------------------------

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


// UPDATE TASK (EVENT) NAME AND SAVE
$("span.task-input").parents("form").children("span.event-edit-submit").on(
    "click", function() {
        let formInputs = {
            "eventId": $(this).parents("form").children("span.task-input").children("span").children("input").attr("name"),
            "newTaskName": $(this).parents("form").children("span.task-input").children("span").children("input").val(),
            "newStartTime": $(this).parents("form").children(".start-end-times").children(".task-start-time").children("input").val(),
            "newStopTime": $(this).parents("form").children(".start-end-times").children(".task-end-time").children("input").val()
        }

        $.post("/edit_task", formInputs);
    });


// GOOGLE CALENDAR EVENT - DELETE PENDING EVENT
$("span.delete-gcal").click(function() {
    let formInputs = {
        gcalEventId: $(this).parents("form").children(".gcal-event-id").val()
    };

    toastr.success('Google Calendar Task Deleted');

    $(this).parents("li").hide();

    $.post("/delete_gcal_event", formInputs)
});


// GOOGLE CALENDAR EVENT - SAVE PENDING EVENT
$("span.save-gcal").click(function() {

    let formInputs = {
        gcalEventId: $(this).parents("form").children(".gcal-event-id").val(),
        categoryName: $(this).parents('form').children(".gcal-event-categories").children("span").children(".selection").children("span").children(".select2-selection__rendered").attr("title")
    };

    toastr.success('Task Saved');

    $(this).parents("li").hide();

    $.post("/save_gcal_event", formInputs)
});


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

function redirectToTasks(result) {
    toastr.success("You've successfully created your account.")
    window.location = "/tasks";
}

function signUp() {

    let formInputs = {
        "name": $("#registerName").val(),
        "email": $("#registerEmail").val(),
        "password": $("#registerPassword").val()
    };

    $.post("/signup_submit", 
           formInputs,
           redirectToTasks);
}

$(".form-signup").click(function() {
    signUp();
});


// LOG IN FLOW

function displayLogInResults(result) {
    if (result === "success") {
        toastr.success("You've successfully logged in.");
        window.location = "/tasks";
    }
    
    else {
        toastr.warning("Wrong email or password. Try again.")
    }

}

function logIn() {
    let formInputs = {
        "email": $("#inputEmail").val(),
        "password": $("#inputPassword").val()
    };

    console.log(formInputs)

    $.post("/login_submit", 
           formInputs,
           displayLogInResults);
}

$("#login-button").click(function() {
    logIn();
});