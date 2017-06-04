$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
              
              $('.alert').show()
              $('.alert-success').removeData()
              $('.alert-success').append('<strong>Well done!</strong>' + response )
            },
            error: function(error) {

            }
        });
    });
});
