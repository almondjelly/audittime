// ----------------- UPDATE SETTINGS -----------------

// Update Your Info
$("button.update-info").on("click", function() {
	if ($("input.update-password").val() != $("input.retype-password").val()) {
		toastr.error("Passwords must match");
	} 

	else {
		let formInputs = {
			"newFullName": $("input.update-fullname").val(),
			"newEmail": $("input.update-email").val(),
			"newPassword": $("input.update-password").val()
		};

		$.post("/save_settings", formInputs);
		toastr.success("Info successfully updated");
		$("input.update-password").val('');
		$("input.retype-password").val('');
	}
});


// Update Toggl integration
$("button.update-toggl").on("click", function() {
	let formInputs = {
		"togglToken": $("input.update-toggl").val(),
	};

	console.log(formInputs)

	$.post("/save_settings", formInputs);
	toastr.success("Info successfully updated");
});


// // Integrate with Google Calendar
// $("button.update-gcal").on("click", function() {
// 	$.post("/gcal");
// });
