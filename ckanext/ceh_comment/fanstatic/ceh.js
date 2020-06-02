$(document).ready(function(){
   $('#cehCommentForm').validate({
           errorElement: 'span',
           rules: {
                   cehname: {
                           required: true,
                           maxlength: 50
                   },
                   cehemail: {
                           required: true,
                           email: true,
                           maxlength: 30
                   },
                   cehcomment: {
                           required: true,
                           maxlength: 500
                   },
                   cehpolicy: {
                           required: true
                   }
           },
           messages: {
                   cehname: {
                           required: "Ingrese un nombre",
                           //minlength: $.format("Mínimo {0} caracteres"),
                           maxlength: $.format("máximo {0} caracteres")
                   },
                   cehemail: {
                           required: "Ingrese un correo",
                           email: "Ingrese un correo válido",
                           maxlength: $.format("máximo {0} caracteres")
                   },
                   cehcomment: {
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
           submitHandler : function(_form) {
                   let form = $(_form);
                   console.log('form',form.serialize());
				   console.log('formArray',form.serializeArray());
                   $.ajax({
						type: form.attr('method'),
						url: form.attr('action'),
						data: form.serializeArray(),
						cache: false, 
						success: function (data) {
							console.log('correcto',data);
						},
						error: function(data) {
							console.log('error',data);
						}
					});
				   $('#cehCommentForm').trigger("reset");
                   $('#alertComment').fadeIn();
				   resetCounter();
                   return false;
           }
   });
   // Comentarios
   $('.ceh-close-calert').click(function(){
      $('#alertComment').fadeOut();
   });
   let ta = resetCounter();
   ta.on('input', updCountdown);

   // Gestion de comentarios
   //$('.ceh-close-cmalert').click(function(){
   //   $('#publishComment').fadeOut();
   //});
});

function resetCounter() {
    let ta = $('#cehcomment');
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
    let remaining = maxLengh - $(currentElement).val().length;
    $(currentElement).nextAll('.countdown:first').text(remaining + '/' + maxLengh);
}