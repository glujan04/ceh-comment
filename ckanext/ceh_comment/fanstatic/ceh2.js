jQuery(document).ready(function() {
	$('#delModal').on('show.bs.modal', function(e) {
		//get data-id attribute of the clicked element
		var threadId = $(e.relatedTarget).data('thread-id');
		//populate the textbox
		$(e.currentTarget).find('input[name="tid"]').val(threadId);
	});
});

function delNotify(){
	let threadId = $('#tid').val();
	console.log('threadId',threadId);
}
