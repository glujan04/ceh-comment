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
                           maxlength: 1000
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
                   //$.ajax({
                      // tu código ajax
                   //})
				   $('#cehCommentForm').trigger("reset");
                   $('#alertComment').fadeIn();
				   resetCounter();
                   return false;
           }
   });
   
   $('.ceh-close').click(function(){
      $('#alertComment').fadeOut();
   });
   let ta = resetCounter();
   ta.on('input', updCountdown);
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