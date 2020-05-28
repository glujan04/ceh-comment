var $j = jQuery.noConflict();
$j(document).ready(function(){
   $j('#cehCommentForm').validate({
           rules: {
                   cehname: {
                           required: true,
                           maxlength: 50
                   },
                   cehemail: {
                           required: true,
                           email: true,
                           maxlength: 50
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
                           //maxlength: $.format("{0} caracteres son demasiados!")
                   },
                   cehemail: {
                           required: "Ingrese un correo",
                           //maxlength: $.format("{0} caracteres son demasiados!")
                   },
                   cehcomment: {
                           required: "Ingrese un comentario",
                           //minlength: $.format("Necesitamos por lo menos {0} caracteres"),
                           //maxlength: $.format("{0} caracteres son demasiados!")
                   },
                   cehpolicy: {
                           required: "Debe aceptar las políticas"
                   }
           },
           submitHandler : function(_form) {
                   let form = $j(_form);
                   console.log('form',form);
                   //$.ajax({
                      // tu código ajax
                   //})
                   return false;
           }
   });
   
   //updateCountdownAll();
   $j('#cehcomment').live('input', updCountdown);
});

//function updateCountdownAll() {
//    $('.message').each(function () {
//        updCountdown(this);
//    });
//}

function updCountdown(e) {
    let currentElement;
    if (e.target) {
        currentElement = e.target;
    } else {
        currentElement = e;
    }
    let maxLengh = $j(currentElement).attr('maxlength');
    let remaining = maxLengh - $(currentElement).val().length;
    $j(currentElement).nextAll('.countdown:first').text(remaining + '/' + maxLengh);
}