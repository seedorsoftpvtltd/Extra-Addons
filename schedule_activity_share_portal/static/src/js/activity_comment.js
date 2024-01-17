odoo.define('schedule_activity_share_portal.activity_comment', function (require) {
'use strict';

	$(document).on("click", ".update_calendar_details", function () {
		$('.custom_activity_comment').val('');
	});
	$(".hide_activity_wizard").click(function () {
		$('.MyCustomActivityModal').modal('hide');
    });
});