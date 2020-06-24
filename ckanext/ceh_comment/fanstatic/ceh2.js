jQuery(document).ready(function() {
	$('#delModal').on('show.bs.modal', function(e) {
		//get data-id attribute of the clicked element
		var threadId = $(e.relatedTarget).data('thread-id');
		//populate the textbox
		$(e.currentTarget).find('input[name="tid"]').val(threadId);
	});
});

function delNotify(){
    let thread_id = $('#tid').val();
    let dataset_id = $('#tid').val();
    let $form = document.createElement('form');
    $form.setAttribute('id', 'data_form');
    $form.setAttribute('action', `/dataset/list/${thread_id}/${dataset_id}/delete`);
    $form.setAttribute('method', 'post');
    document.body.appendChild($form);
    $form.submit();
	document.body.removeChild($form);
}