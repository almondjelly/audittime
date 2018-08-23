// --------------- TIMER HELPER FUNCTIONS ------------------

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


	// >> Update timer range
    $("input[name='timer-datetimes']").on('apply.daterangepicker', function(ev, picker) {
    	console.log('sdlfkjsdlkfjsdklj')

        let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"newStart": picker.startDate.format('YYYY-MM-DD hh:mm A'),
            "newEnd": picker.endDate.format('YYYY-MM-DD hh:mm A')
        };

        console.log(formInputs)
        
        $.post("/edit_timer", formInputs);
    });





	// // UPDATE TASK (EVENT) NAME AND SAVE
	//     $(".td-event-start-time").click(function (){
	//         $(this).parents("tr").children(".td-event-start-time").children("input").show();
	//         let currentStart = $(this).val();
	//         $(this).parents("tr").children(".td-event-start-time").children("input").attr("placeholder",
	//             currentStart);
	//     });
	    
	//     $(".td-event-end-time").click(function (){
	//         $(this).parents("tr").children(".td-event-end-time").children("input").show();
	//         $(this).parents("tr").mouseleave(function() {
	//             $(this).parents("tr").children(".td-event-start-time").children("input").hide();
	//         });
	//     });

	//     $(".span-event-task-save").click(function() {
	//         console.log('saving task');

	//         let formInputs = {
	//             "eventId": $(this).parents("tr").children(".input-event-id").val(),
	//             "newTaskName": $(this).parents("tr").children(".td-event-task").children("input").val(),
	//             "newStartTime": $(this).parents("tr").children(".td-event-start-time").children("input").val(),
	//             "newStopTime": $(this).parents("tr").children(".td-event-end-time").children("input").val()
	//         };

	//         $.post("/edit_task", formInputs);

	//         toastr.success("Task Updated");
	//     });


	// // ARCHIVE EVENT

	//     function displayArchiveEventResults(result) {
	//         console.log(result);
	//     }

	//     $(".span-event-task-remove").click(function() {
	//         let formInputs = {
	//             "eventId": $(this).parents("tr").children(".input-event-id").val()
	//         };

	//         toastr.success("Task Archived");

	//         $.post("archive_event", formInputs, displayArchiveEventResults);
	//         $(this).parents("tr").hide();
	//     });
