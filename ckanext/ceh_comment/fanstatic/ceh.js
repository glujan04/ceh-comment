// Comment list
function hideFormErrors()
{
    jQuery('.form_errors').addClass('hidden');
    jQuery('.form_errors li').addClass('hidden');
}

jQuery(document).ready(function() {
     validReplyForm();
     // jQuery('.module-content input[type="submit"]').on('click', function(e) {
         // if (jQuery(this).hasClass('btn-primary')) {
             // var form = jQuery(this).closest('form');
             // var comment = form.find('textarea[name="comment"]').val();
             // var display_errors = false;

             // hideFormErrors();

             // if (!comment || !comment.replace(/\s/g, '').length) {
                 // form.find('.error-comment').removeClass('hidden');
                 // display_errors = true;
             // }
             // if (display_errors) {
                 // form.find('.form-errors').removeClass('hidden');
                 // return false;
             // }
         // }
     // });
});

function validReplyForm(){
   $('.ceh-comments-reply').each(function(e){
			$( this ).find('form').validate({
			   errorElement: 'span',
			   rules: {
					   subject: {
							   required: true,
							   maxlength: 50
					   },
					   email: {
							   required: true,
							   email: true,
							   maxlength: 30
					   },
					   comment: {
							   required: true,
							   maxlength: 500
					   },
					   cehpolicy: {
							   required: true
					   }
			   },
			   messages: {
					   subject: {
							   required: "Ingrese un nombre",
							   maxlength: $.format("máximo {0} caracteres")
					   },
					   email: {
							   required: "Ingrese un correo",
							   email: "Ingrese un correo válido",
							   maxlength: $.format("máximo {0} caracteres")
					   },
					   comment: {
							   required: "Ingrese un comentario"
					   },
					   cehpolicy: {
							   required: "Debe aceptar los términos"
					   }
			   },
			   errorPlacement: function(label, element) {
					   label.addClass('ceh-error');
					   element.parent().append(label);
			   }
	   });
   });
   // COMENTARIOS RESPUESTA
   resetCounterReply();
}
// Comments
function ShowCommentForm(id){
	if ($("#" + id).hasClass('hidden'))
        $("#" + id).removeClass('hidden');
	else{
		$("#" + id).addClass('hidden');
		$("#form_" + id).validate().resetForm();
		//$("#form_" + id).trigger("reset");
	}
}

function resetCounterReply() {
    let ta = $('.ceh_comment_reply').each( function( index, el ) {
		updCountdown( el );
		$(el).on('input', updCountdown);
    });
}

$(document).ready(function(){
   $('#cehCommentForm').validate({
           errorElement: 'span',
           rules: {
                   subject: {
                           required: true,
                           maxlength: 50
                   },
                   email: {
                           required: true,
                           email: true,
                           maxlength: 30
                   },
                   comment: {
                           required: true,
                           maxlength: 500
                   },
                   cehpolicy: {
                           required: true
                   }
           },
           messages: {
                   subject: {
                           required: "Ingrese un nombre",
                           //minlength: $.format("Mínimo {0} caracteres"),
                           maxlength: $.format("máximo {0} caracteres")
                   },
                   email: {
                           required: "Ingrese un correo",
                           email: "Ingrese un correo válido",
                           maxlength: $.format("máximo {0} caracteres")
                   },
                   comment: {
                           required: "Ingrese un comentario",
                           //minlength: $.format("Necesitamos por lo menos {0} caracteres"),
                           //maxlength: $.format("{0} caracteres son demasiados!")
                   },
                   cehpolicy: {
                           required: "Debe aceptar los términos"
                   }
           },
           errorPlacement: function(label, element) {
                   label.addClass('ceh-error');
                   element.parent().append(label);
           },
           // submitHandler : function(_form) {
                   // let form = $(_form);
                   // console.log('form',form.serialize());
				   // console.log('formArray',form.serializeArray());
                   // $.ajax({
						// type: form.attr('method'),
						// url: form.attr('action'),
						// data: form.serializeArray(),
						// cache: false, 
						// success: function (data) {
							// console.log('correcto',data);
						// },
						// error: function(data) {
							// console.log('error',data);
						// }
					// });
				   // $('#cehCommentForm').trigger("reset");
                   // $('#alertComment').fadeIn();
				   // resetCounter();
                   // return false;
           // }
   });
   // COMENTARIOS
   // popup
   $('.ceh-close-calert').click(function(){
      $('#alertComment').fadeOut();
   });
   let ta = resetCounter();
   ta.on('input', updCountdown);
});

function resetCounter() {
    let ta = $('#comment');
   updCountdown(ta);
   return ta;
}

function updCountdown(e) {
    let currentElement;
    if (e.target) {
        currentElement = e.target;
    } else {
        currentElement = e;
    }
    let maxLengh = $(currentElement).attr('maxlength');
    let remaining = maxLengh - $(currentElement).text().length;
	console.log($(currentElement).nextAll('.countdown:first'));
    //$(currentElement).nextAll('.countdown:first').text(remaining + '/' + maxLengh);
}