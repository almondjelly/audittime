// BY DEFAULT, WHEN PAGE IS LOADED, HIDE:
    // MANUAL MODE, 
    // CATEGORY DROPDOWN, 
    // EVENT EDIT SUBMIT BUTTON 

function initialize() {
    $(".form-register").hide();
    $(".span-goal-edit").hide();
    $(".span-goal-archive").hide();
    $(".span-category-save").hide();
    $(".span-category-archive").hide();
    $(".span-event-task-save").hide();
    $(".span-event-task-remove").hide();
    $(".span-toggl-entry-save").hide();
    $(".span-toggl-entry-remove").hide();
    $(".span-gcal-event-save").hide();
    $(".span-gcal-event-remove").hide();
    $("#mode-stopwatch").hide();
    $("#stop-button").hide();
    $(".input-task-start-date-time-picker").hide();
    $(".input-task-end-date-time-picker").hide(); 
    $("#category-new").hide();
    $("#goal-new").hide();

    // Apply tablesorter to tables
    $("table").tablesorter();

    

    // Apply selectize.js to dropdowns
    $("#select-category-goal").selectize({placeholder: "select your goals"});
    $("#select-task-category").selectize({placeholder: "tv"});
    $(".goal-modal-input-goal-categories").selectize();
    $(".goal-modal-input-type").selectize();
    $(".td-input-category-goals").selectize();



    // Remove Bootstrap's hideous blue glow
    function handleFirstTab(e) {
        if (e.keyCode === 9) { // the "I am a keyboard user" key
            document.body.classList.add('user-is-tabbing');
            window.removeEventListener('keydown', handleFirstTab);
        }
    }

    window.addEventListener('keydown', handleFirstTab);



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

    // ADD NEW STUFF

        $("#add-new-category").click(function() {
            $("#category-new").slideToggle();
        });

        $("#add-new-goal").click(function() {
            $("#goal-new").slideToggle();
        });

    // SETTINGS

        $("#show-password").click(function() {
            console.log('what on earth')
            let pass = $("#input-new-password");
            if (pass.attr("type") === "password") {
                pass.attr("type", "text");
            } else {
                pass.attr("type", "password");
            }
        });

    // SHOW/HIDE SAVE BUTTONS

    // Google Calendar
        // When the mouse hovers over the list item, show the Save button.
        $(".tr-gcal-event").hover(function() {
            $(this).children(".td-gcal-event-save").children("span").show();
            $(this).children(".td-gcal-event-remove").children("span").show();


        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
            $(this).children(".td-gcal-event-save").children("span").hide();
            $(this).children(".td-gcal-event-remove").children("span").hide();
            });    
        });

    // Toggl
        // When the mouse hovers over the list item, show the Save button.
        $(".tr-toggl-entry").hover(function() {
            $(this).children(".td-toggl-entry-save").children("span").show();
            $(this).children(".td-toggl-entry-remove").children("span").show();


        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
            $(this).children(".td-toggl-entry-save").children("span").hide();
            $(this).children(".td-toggl-entry-remove").children("span").hide();
            });    
        });


    // Task

        // When the stopwatch START button is clicked, hide the start button
        // and expose the stop button.
        $("#start-button").click(function() {
            $(this).hide();
            $("#stop-button").show();
        });

         $("#stop-button").click(function() {
            $(this).hide();
            $("#start-button").show();
        });

        // When the mouse hovers over the list item, show the Save button.
        $(".tr-event-task").hover(function() {
            $(this).children(".td-event-task-save").children("span").show();
            $(this).children(".td-event-task-remove").children("span").show();


        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
            $(this).children(".td-event-task-save").children("span").hide();
            $(this).children(".td-event-task-remove").children("span").hide();
            });    
        });

        $("#login-button").keyup(function(event) {
            event.preventDefault();
  
            // Number 13 is the "Enter" key on the keyboard
            if (event.keyCode === 13) {
            
                // Trigger the button element with a click
                $("#login-button").click();
            }
        });

    // Goal

        // When the mouse hovers over the list item, show the Save button.
        $(".tr-goal").hover(function() {
            console.log("i wolke up");
            $(this).children(".td-goal-edit").children("span").show();
            $(this).children(".td-goal-archive").children("span").show();

        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
                $(this).children(".td-goal-edit").children("span").hide();
                $(this).children(".td-goal-archive").children("span").hide();
            });
        });  

    // Category

        // When the mouse hovers over the list item, show the Save button.
        $(".tr-category").hover(function() {
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
flatpickr(".input-goal-date-time-picker", {
    enableTime: true,
    dateFormat: "M j \\at h:i K",
    allowInput: true,
    altFormat: "F j, Y"
});

flatpickr(".input-task-start-date-time-picker", {
    enableTime: true,
    dateFormat: "m/d \\at h:i K",
    allowInput: true,
    altFormat: "F j, Y"
});

flatpickr(".modal-input-goal-date-time-picker", {
    enableTime: true,
    dateFormat: "m/d \\at h:i K",
    allowInput: true,
    altFormat: "F j, Y"
});

flatpickr(".input-task-end-date-time-picker", {
    enableTime: true,
    dateFormat: "m/d \\at h:i K",
    allowInput: true,
    altFormat: "F j, Y"
});

flatpickr(".date-time-picker", {
    enableTime: true,
    dateFormat: "m/d \\at h:i K",
    allowInput: true,
    altFormat: "F j, Y"
});


// ---------------------------------- GOALS ----------------------------------

// ADD NEW GOAL
    function addNewGoal(result){
        $("#tbody-goal-log").prepend(result);
        $("#form-goal").trigger('reset');
    }

    $("#goal-submit").on("click", function() {
        let formInputs = {
            "goalName": $("#input-goal-name").val(),
            "goalType": $("#select-goal-type").val(),
            "hours": $("#hours").val(),
            "minutes": $("#minutes").val(),
            "startDate": $("#start-date").val(),
            "endDate": $("#end-date").val()
        };

        $.post("/add_goal", formInputs, addNewGoal);

        toastr.success("New Goal Added")
    });


// EDIT GOAL INFO AND SAVE
$(".goal-edit-save").click(function() {
    console.log("saving goal")

    let newCategoryGoalsArr = $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-categories").children(".td-goal-modal-input").children("select").val()
    let newCategoryGoals = '';

    for (let category of newCategoryGoalsArr) {
        newCategoryGoals += (category + '|');
    }

    let formInputs = {
        "goalId": $(this).parents("tr").children(".input-goal-id").val(),
        "newGoalName": $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-name").children(".td-goal-modal-input").children("input").val(),
        "newType": $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-type").children(".td-goal-modal-input").children("select").val(),
        "newDays": $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-target").children(".td-goal-modal-input").children(".goal-modal-input-duration.days").val(),
        "newHours": $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-target").children(".td-goal-modal-input").children(".goal-modal-input-duration.hours").val(),
        "newMinutes": $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-target").children(".td-goal-modal-input").children(".goal-modal-input-duration.minutes").val(),
        "newStartTime": $(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-start").children(".td-goal-modal-input").children(".input-goal-start-time.time-input").children(".modal-input-goal-date-time-picker.flatpickr-input").val(),
        "newEndTime":$(this).parents(".modal-content").children(".modal-body").children("form").children("table").children("tbody").children(".tr-goal-modal-end").children(".td-goal-modal-input").children(".input-goal-end-time.time-input").children(".modal-input-goal-date-time-picker.flatpickr-input").val(),
        "newCategoryGoals": newCategoryGoals 
    }

    $.post("/edit_goal_info", formInputs);

    toastr.success("Goal Updated")

});

// ARCHIVE Goal

    function displayArchiveGoalResults(result) {
        console.log(result);
    }

    $(".btn-goal-archive").click(function() {
        let formInputs = {
            "goalId": $(this).parents("tr").children(".input-goal-id").val()
        };

        toastr.success("Goal Archived");

        $.post("archive_goal", formInputs, displayArchiveGoalResults);
        $(this).parents("tr").hide();
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

        $("#select-category-goal").change(function() {
            $(this).children("option:selected").each(function() {
                categoryGoals += $(this).text() + '|';
            });
        }).trigger("change");


        let formInputs = {
            "categoryName": $("#input-category-new").val(),
            "categoryGoals": categoryGoals
        };

        $.post("/add_category", formInputs, addNewCategory);

    });


// EDIT CATEGORY INFO AND SAVE

function displayEditCategoryResults(result) {
    toastr.success("Category Saved");
}


$(".btn-category-save").click(function() {
        let newCategoryGoals = '';

        
        $(this).parents("tr").children(".td-category-goals").children("select").change(function() {
            $(this).children("option:selected").each(function() {
                newCategoryGoals += $(this).text() + '|';
            });
        }).trigger("change");
    
        console.log("saving category");
    
        let formInputs = {
            "categoryId": $(this).parents("tr").children(".input-category-id").val(),
            "newcategoryName": $(this).parents("tr").children(".td-category").children(".td-input-category").val(),
            "newCategoryGoals": newCategoryGoals
        };

        $.post("/edit_category_info", formInputs, displayEditCategoryResults);

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

// ENABLE TOGGLING BETWEEN STOPWATCH / MANUAL MODES
    $("#mode-stopwatch").click(function() {
        $("#startStop").show();
        $("#datePickers").hide();
        $(this).hide();
        $('#mode-manual').show();
    });

    $("#mode-manual").click(function() {
        $("#startStop").hide();
        $("#datePickers").show();
        $(this).hide();
        $('#mode-stopwatch').show();
    });


// ADD NEW EVENT
    function addNewEvent(result) {
        toastr.success("New task added")
        $("#event-log").prepend(result);
        $("#form-stopwatch").trigger("reset");
        initialize();
        $("#event-log-ul > li:first-child .category-title > span").on("click", function() {
            $(this).children().toggle();    
        });

        // $("#event-log").children(".on("hover", function() {
        //     $(this).parents("form").children("span.event-edit-submit").show();
        //     $(this).parents("form").children("span.task-input").children(
        //         "span").children("input").on("focusout", function(event) {
        //             $(this).parents("form").children("span.event-edit-submit").hide();
        //     });
        
        // });

        console.log(result)
    }

// SUBMIT EVENT - MANUAL
$("#manual-submit").click(function() {

        let formInputs = {
            "task": $("#input-new-task-name").val(),
            "category": $("#select-task-category").val(),
            "startTime": $("#m-start").val(),
            "stopTime": $("#m-stop").val()
        };

        $.post("/add_event", 
               formInputs,
               addNewEvent);

});

// SUBMIT EVENT - STOPWATCH

class Stopwatch {
    constructor(display, results) {
        this.running = false;
        this.display = display;
        this.results = results;
        this.laps = [];
        this.reset();
        this.print(this.times);
    }
    
    reset() {
        this.times = [ 0, 0, 0 ];
    }
    
    start() {
        if (!this.time) this.time = performance.now();
        if (!this.running) {
            this.running = true;
            requestAnimationFrame(this.step.bind(this));
        }
    }
   
    stop() {
        this.running = false;
        this.time = null;
    }
    
    clear() {
        clearChildren(this.results);
    }
    
    step(timestamp) {
        if (!this.running) return;
        this.calculate(timestamp);
        this.time = timestamp;
        this.print();
        requestAnimationFrame(this.step.bind(this));
    }
    
    calculate(timestamp) {
        var diff = timestamp - this.time;
        // Hundredths of a second are 100 ms
        this.times[2] += diff / 10;
        // Seconds are 100 hundredths of a second
        if (this.times[2] >= 100) {
            this.times[1] += 1;
            this.times[2] -= 100;
        }
        // Minutes are 60 seconds
        if (this.times[1] >= 60) {
            this.times[0] += 1;
            this.times[1] -= 60;
        }
    }
    
    print() {
        this.display.innerText = this.format(this.times);
    }
    
    format(times) {
        return `\
            ${pad0(times[0], 2)}:${pad0(times[1], 2)}:${pad0(Math.floor(times[2]), 2)}`;
    }
}

function pad0(value, count) {
    var result = value.toString();
    for (; result.length < count; --count)
        result = '0' + result;
    return result;
}

function clearChildren(node) {
    while (node.lastChild)
        node.removeChild(node.lastChild);
}


function startStopwatch(event) {

    let stopwatch = new Stopwatch(
        document.querySelector('#running-time'),
        document.querySelector('#running-time-results'));

    // Start the #running-time stopwatch
    stopwatch.start()

    // Store the current timestamp
    let startTime = Date.now();

    console.log('Starting stopwatch...');
    console.log(startTime);

    $("#stop-button").click(function() {

        // Stop the #running-time stopwatch
        stopwatch.stop();

        // Store the current timestamp
        let stopTime = Date.now();

        $("#running-time").html("00:00:00");

        let formInputs = {
            "task": $("#input-new-task-name").val(),
            "category": $("#select-task-category").val(),
            "startTime": startTime,
            "stopTime": stopTime
        };

        $.post("/add_event", 
               formInputs,
               addNewEvent);
    });
}

$("#start-button").on("click", startStopwatch);


// UPDATE TASK (EVENT) NAME AND SAVE
    $(".td-event-start-time").click(function (){
        $(this).parents("tr").children(".td-event-start-time").children("input").show();
        let currentStart = $(this).val();
        $(this).parents("tr").children(".td-event-start-time").children("input").attr("placeholder",
            currentStart);
    });
    
    $(".td-event-end-time").click(function (){
        $(this).parents("tr").children(".td-event-end-time").children("input").show();
        $(this).parents("tr").mouseleave(function() {
            $(this).parents("tr").children(".td-event-start-time").children("input").hide();
        });
    });

    $(".btn-event-task-save").click(function() {
        console.log('saving task');

        let formInputs = {
            "eventId": $(this).parents("tr").children(".input-event-id").val(),
            "newTaskName": $(this).parents("tr").children(".td-event-task").children("input").val(),
            "newStartTime": $(this).parents("tr").children(".td-event-start-time").children("input").val(),
            "newStopTime": $(this).parents("tr").children(".td-event-end-time").children("input").val()
        };

        $.post("/edit_task", formInputs);

        toastr.success("Task Updated");
    });


// ARCHIVE EVENT

    function displayArchiveEventResults(result) {
        console.log(result);
    }

    $(".btn-event-task-remove").click(function() {
        let formInputs = {
            "eventId": $(this).parents("tr").children(".input-event-id").val()
        };

        toastr.success("Task Archived");

        $.post("archive_event", formInputs, displayArchiveEventResults);
        $(this).parents("tr").hide();
    });

// TOGGL ENTRY - DELETE PENDING ENTRY
$("button.btn-toggl-entry-remove").click(function() {
    let formInputs = {
        togglEntryId: $(this).parents("tr").children(".toggl-entry-id").val()
    };

    toastr.success('Task Removed');

    $(this).parents("tr").hide();

    $.post("/delete_toggl_entry", formInputs)
});


// TOGGL ENTRY - SAVE PENDING ENTRY
$("button.btn-toggl-entry-save").click(function() {

    let formInputs = {
        togglEntryId: $(this).parents("tr").children(".toggl-entry-id").val(),
        categoryName: $(this).parents('tr').children('.td-toggl-entry-categories').children('select').val()
    };

    toastr.success('Task Saved');

    $(this).parents("tr").hide();

    $.post("/save_toggl_entry", formInputs)
});



// GOOGLE CALENDAR EVENT - DELETE PENDING EVENT
$("button.btn-gcal-event-remove").click(function() {
    let formInputs = {
        gcalEventId: $(this).parents("tr").children(".gcal-event-id").val(),
    };

    toastr.success('Task Removed');

    $(this).parents("tr").hide();

    $.post("/delete_gcal_event", formInputs)
});


// GOOGLE CALENDAR EVENT - SAVE PENDING EVENT
$("button.btn-gcal-event-save").click(function() {

    let formInputs = {
        gcalEventId: $(this).parents("tr").children(".gcal-event-id").val(),
        categoryName: $(this).parents("tr").children(".td-gcal-event-categories").children("select").val()
    };

    toastr.success('Task Saved');

    $(this).parents("tr").hide();

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
        "name": $("#register-name").val(),
        "email": $("#register-email").val(),
        "password": $("#register-password").val()
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

$("#login-button").click(function() {
    logIn();
});




