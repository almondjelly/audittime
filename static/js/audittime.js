// BY DEFAULT, WHEN PAGE IS LOADED, HIDE:
    // MANUAL MODE, 
    // CATEGORY DROPDOWN, 
    // EVENT EDIT SUBMIT BUTTON 

function initialize() {
    $(".form-register").hide();
    $(".span-goal-archive").hide();
    $(".span-category-save").hide();
    $(".span-category-archive").hide();
    $(".span-event-task-save").hide();
    $(".span-event-task-remove").hide();
    $(".span-toggl-entry-save").hide();
    $(".span-toggl-entry-remove").hide();
    $(".span-gcal-event-save").hide();
    $(".span-gcal-event-remove").hide();
    $("#manual-dates").hide();
    $("#stop-button").hide();
    $(".input-task-start-date-time-picker").hide();
    $(".input-task-end-date-time-picker").hide(); 
    $("#category-new").hide();
    $(".div-goal-event-log").hide();
    $(".expand-less").hide();

    // Apply tablesorter to tables
    // $("table").tablesorter();

    // Apply selectize.js
    $("#goal-category-select").selectize({
        delimiter: ',',
        persist: false,
        create: function(input) {
            return {
                value: input,
                text: input
            }
        },
    });

    $(".td-select-goal-categories").multiselect({
        enableFiltering: true,
        filterBehavior: 'value',
        includeSelectAllOption: true,
        buttonText: function(options, select) {
            if (options.length === 0) { return 'No Categories'; } 
            else if (options.length > 1) { return options.length + ' Categories'; } 
            else {
                var labels = [];
                options.each(function() {
                    if ($(this).attr('label') !== undefined) {
                        labels.push($(this).attr('label'));
                    } else {
                        labels.push($(this).html());
                    }
                });
                
                return labels.join(', ') + '';
            }  
        }
    });

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

    // Set goal range datetime pickers
    $('input[name="newgoal-datetimes"]').daterangepicker({
        timePicker: true,
        autoUpdateInput: false,
        opens: 'left',
        locale: {
            format: 'YYYY-MM-DD hh:mm A',
            // cancelLabel: 'Clear'
        },
        ranges: {
            'Today': [moment().startOf('day'), moment().endOf('day')],
            'Next 7 Days': [moment().startOf('day'), moment().add(7, 'days')],
            'Next 30 Days': [moment().startOf('day'), moment().add(30, 'days')],
            'This Week': [moment().startOf('week'), moment().endOf('week')],
            'This Month': [moment().startOf('month'), moment().endOf('month')]
        },
        alwaysShowCalendars: true,
    });

    $('input[name="newgoal-datetimes"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD hh:mm A') + ' - ' + picker.endDate.format('YYYY-MM-DD hh:mm A'));
    });

    $('input[name="newgoal-datetimes"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

    $('input[name="datetimes"]').each(function(i) {
        let startDateTime = $(this).parents("td").children(".td-goal-range-start").val();
        let endDateTime = $(this).parents("td").children(".td-goal-range-end").val();

        $(this).daterangepicker({
            timePicker: true,
            autoUpdateInput: true,
            startDate: startDateTime,
            endDate: endDateTime,
            opens: 'center',
            locale: {
                format: 'M/DD'
            },
            ranges: {
            'Today': [moment().startOf('day'), moment().endOf('day')],
            'Next 7 Days': [moment().startOf('day'), moment().add(7, 'days')],
            'Next 30 Days': [moment().startOf('day'), moment().add(30, 'days')],
            'This Week': [moment().startOf('week'), moment().endOf('week')],
            'This Month': [moment().startOf('month'), moment().endOf('month')]
            },
            alwaysShowCalendars: true
        }
            
        );
    });

};
    
function addEventListeners(){

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
            $(this).children(".td-goal-archive").children("span").show();

        // When the mouse leaves the list item, hide the Save button.
            $(this).mouseleave(function() {
                $(this).children(".td-goal-archive").children("span").hide();
            });
        });  

        // Expand goal to display associated tasks
        $(".td-goal-expand").click(function() {
            $(this).children(".expand-more").toggle();
            $(this).children(".expand-less").toggle();
            $(this).parents("table").next().slideToggle();
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
   addEventListeners();
});



// ---------------------------------- GOALS ----------------------------------

// ADD NEW GOAL
    function addNewGoal(result){
        $("#div-goal-log").prepend(result);
        $("#form-goal").trigger('reset');
        $("#goal-category-select")[0].selectize.clear();   
    }

    $("#goal-submit").on("click", function() {

        if ($("#input-new-goal-name").val() === "") {
            toastr.error("Enter a title for your goal")
        } 

        if ($("#select-goal-type").val() === null) {
            toastr.error("Choose a type of goal")
        } 

        if (Number.isInteger(parseInt($("#hours").val())) === false) {
            toastr.error("Enter number of hours")
        }

        if (Number.isInteger(parseInt($("#minutes").val())) === false) {
            toastr.error("Enter number of minutes")
        }

        if ($("#newgoal-range").val() === "") {
            toastr.error("Pick a time range")
        }

        if ($("#goal-category-select").val().length === 0) {
            toastr.error("Add at least one category")
        }

        if (
            ($("#input-new-goal-name").val() != "") &&
            ($("#select-goal-type").val() != null) &&
            (Number.isInteger(parseInt($("#hours").val())) != false) && 
            (Number.isInteger(parseInt($("#minutes").val())) != false) &&
            ($("#newgoal-range").val() != "") &&
            ($("#goal-category-select").val().length > 0)
        ) {

            let goalCategories = '';

            for (let category of $("#goal-category-select").val()) {
                goalCategories += category;
                goalCategories += "|";
            }

            let formInputs = {
            "goalName": $("#input-new-goal-name").val(),
            "goalType": $("#select-goal-type").val(),
            "hours": $("#hours").val(),
            "minutes": $("#minutes").val(), 
            "timeRange": $("#newgoal-range").val(),
            "goalCategories": goalCategories
            };

            console.log(formInputs)

            $.post("/add_goal", formInputs, addNewGoal);

            toastr.success("New Goal Added")
        }

    });




// EDIT GOAL INFO AND SAVE

    // Update goal name
    $(".td-input-goal-name").focusout(function() {
        let formInputs = {
            "goalId": $(this).parents("tr").children(".input-goal-id").val(),
            "newGoalName": $(this).val()
        }

        $.post("/edit_goal_info", formInputs);
    });

    // Update goal type
    $(".select-goal-type").change(function() {
        let formInputs = {
            "goalId": $(this).parents("tr").children(".input-goal-id").val(),
            "newType": $(this).val()
        }

        $.post("/edit_goal_info", formInputs);
    });

    // Update goal time range
    $("input[name='datetimes']").on('apply.daterangepicker', function(ev, picker) {
        console.log('whatevss')
        let formInputs = {
            "goalId": $(this).parents("tr").children(".input-goal-id").val(),
            "newStart": picker.startDate.format('YYYY-MM-DD hh:mm A'),
            "newEnd": picker.endDate.format('YYYY-MM-DD hh:mm A')
        };
        
        $.post("/edit_goal_info", formInputs);
    });
 
    // Update goal target duration
    $(".td-input-goal-target").focusout(function() {
        let formInputs = {
            "goalId": $(this).parents("tr").children(".input-goal-id").val(),
            "newTarget": $(this).val()
        }

        $.post("/edit_goal_info", formInputs);
    });


// $(".td-goal-save").click(function() {
//     console.log("saving goal")

//     $(this).parents("tr").children(".td-goal-range").children(".td-input-goal-range").on('apply.daterangepicker', function(ev, picker) {
//         console.log(picker.startDate.format('YYYY-MM-DD hh:mm A'));
//         console.log(picker.endDate.format('YYYY-MM-DD hh:mm A'));
//     });

//     let formInputs = {
//         "goalId": $(this).parents("tr").children(".input-goal-id").val(),
//         "newType": $(this).parents("tr").children(".td-goal-type").children("select").val(),
//         "newTarget": $(this).parents("tr").children(".td-goal-duration").children("input").val(),
//         "newTimeRange": $(this).parents("tr").children(".td-goal-range").children(".td-input-goal-range").val()    
//     }

//     $.post("/edit_goal_info", formInputs);

//     toastr.success("Goal Updated")

// });

// ARCHIVE Goal

    function displayArchiveGoalResults(result) {
        console.log(result);
    }

    $(".span-goal-archive").click(function() {
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
    // $("#mode-stopwatch").click(function() {
    //     $("#startStop").show();
    //     $("#datePickers").hide();
    //     $(this).hide();
    //     $('#mode-manual').show();
    // });

    // $("#mode-manual").click(function() {
    //     $("#startStop").hide();
    //     $("#datePickers").show();
    //     $(this).hide();
    //     $('#mode-stopwatch').show();
    // });

    $("#running-time").click(function() {
        $("#manual-dates").toggle();
    })


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

    $(".span-event-task-save").click(function() {
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

    $(".span-event-task-remove").click(function() {
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


$(".sidenav .row").hover(function() {
    $(this).css("background-color", "#9B9B9B")
    $(this).mouseleave(function() {
        $(this).css("background-color", "#393A4C")
    });
});

$(".sidenav .row").click(function() {
    window.location = $(this).children("a").attr("href");
});






