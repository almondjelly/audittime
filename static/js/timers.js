// TIMER HELPER FUNCTIONS -----------------------------------------------

	// NEW TIMER ACTIONS ------------------------------------------------

	// >> Switch to manual mode -----------------------------------------
	$("button.timer-mode-manual").click(function() {
        $(this).hide();
        $("button.timer-mode-stopwatch").show();
        $("input.new-timer-running").hide();
        $("input.new-timer-manual").show();
        $("div.start-button").hide();
        $("div.mid-spacer").removeClass("col-sm-4").addClass("col-sm-2");
        $("div.running-time").removeClass("col-sm-3").addClass("col-sm-6");
    });

	// >> Switch to stopwatch mode --------------------------------------
    $("button.timer-mode-stopwatch").click(function() {
        $(this).hide();
        $("button.timer-mode-manual").show();
        $("input.new-timer-manual").hide();
        $("input.new-timer-running").show();
        $("div.start-button").show();
        $("div.mid-spacer").removeClass("col-sm-2").addClass("col-sm-4");
        $("div.running-time").removeClass("col-sm-6").addClass("col-sm-3"); 
    });
    
    // >> Toggle between start and stop timer buttons -------------------
    $("i.start-button").click(function() {
        console.log('what')
        $(this).hide();
        $("i.stop-button").show();
    });

    $("i.stop-button").click(function() {
        $(this).hide();
        $("i.start-button").show();
    });


	// UPDATE INFO IN TIMER LOG -------------------------------------------

	// >> Update timer name -----------------------------------------------
	$("input.timer-name").focusout(function() {
		let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"newTimerName": $(this).val()
		};

		$.post("/edit_timer", formInputs);
	});

	// >> Update timer category -----------------------------------------------
	$("select.timer-category").change(function() {
		let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"newTimerCategory": $(this).val()
		};

		$.post("/edit_timer", formInputs);
	});


	// >> Update timer range -----------------------------------------------
    $("input[name='timer-datetimes']").on('apply.daterangepicker', function(ev, picker) {
        let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"newStart": picker.startDate.format('YYYY-MM-DD hh:mm A'),
            "newEnd": picker.endDate.format('YYYY-MM-DD hh:mm A')
        };
        
        $.post("/edit_timer", formInputs);
    });


	// >> Show timer archive button -----------------------------------------
    $("div.timer-row").hover(function() {
        $(this).children("div.timer-archive").children("span.timer-archive").show();
        $(this).mouseleave(function() {
            $(this).children("div.timer-archive").children("span.timer-archive").hide();
        });
    });

    // >> Archive timer event -------------------------------------------------
    $("span.timer-archive").click(function() {
    	let formInputs = {
			"eventId": $(this).parents("div.timer-row").children("input.event-id").val(),
			"timerId": $(this).parents("div.timer-row").children("input.timer-id").val(),
			"archiveTimer": "archiveTimer"
        };
        
        $.post("/edit_timer", formInputs);
        $(this).parents("div.timer-row").hide();
    	toastr.success("Timer archived");
    });