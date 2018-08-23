function initialize() {
    $("input.new-timer-manual").hide();
    $("button.timer-mode-stopwatch").hide();
    $("span.timer-archive").hide();
}

function addEventListeners() {
	$("button.timer-mode-manual").click(function() {
        $(this).hide();
        $("button.timer-mode-stopwatch").show();
        $("input.new-timer-running").hide();
        $("input.new-timer-manual").show();
        $("div.start-button").hide();
        $("div.mid-spacer").removeClass("col-sm-4").addClass("col-sm-2");
        $("div.running-time").removeClass("col-sm-3").addClass("col-sm-6");
    });

    $("button.timer-mode-stopwatch").click(function() {
        $(this).hide();
        $("button.timer-mode-manual").show();
        $("input.new-timer-manual").hide();
        $("input.new-timer-running").show();
        $("div.start-button").show();
        $("div.mid-spacer").removeClass("col-sm-2").addClass("col-sm-4");
        $("div.running-time").removeClass("col-sm-6").addClass("col-sm-3"); 
    });

    $("div.timer-row").hover(function() {
        $(this).children("div.timer-archive").children("span.timer-archive").show();
        $(this).mouseleave(function() {
            $(this).children("div.timer-archive").children("span.timer-archive").hide();
        });
    });
    
    $("i.start-button").click(function() {
        console.log('what')
        $(this).hide();
        $("i.stop-button").show();
    });

    $("i.stop-button").click(function() {
        $(this).hide();
        $("i.start-button").show();
    });

}

$(document).ready(function() {
   initialize(); 
   addEventListeners();
});





// --------------- HELPER FUNCTIONS ------------------

// UPDATE INFO IN TIMER LOG

	// >> Update timer name
	$("input.timer-name").focusout(function() {
		let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"newTimerName": $(this).val()
		};

		$.post("/edit_timer", formInputs);
	});

	// >> Update timer category
	$("select.timer-category").change(function() {
		let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"newTimerCategory": $(this).val()
		};

		$.post("/edit_timer", formInputs);
	});








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
