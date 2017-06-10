$(function() {
    // Sign up onclick function
    $('#btnSignUp').click(function() {
        // Sign up ajax with request form.
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
              // Set alert for success.
              $('.alert').show()
              $('.alert-success').removeData()
              $('.alert-success').append('<strong>Well done!</strong>' + response.message )
            },
            error: function(errorResponse) {
              // Set alert for error.
              $('.alert').show()
              $('.alert-success').removeData()
              $('.alert').removeClass('alert-success')
              $('.alert').addClass('alert-warning')
              $('.alert-warning').append('<strong>Well done!</strong> ' + errorResponse.responseJSON.message )
            }
        });
    });

    // Sign in onclick function
    $('#btnSignIn').click(function() {
      // Sign up ajax with request form.
      $.ajax({
          url: '/signIn',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
            // Set alert for success.
            $('.alert').show()
            $('.alert-success').removeData()
            $('.alert-success').append('<strong>Well done!</strong>' + response.message )
            var url  =  window.location.protocol + "//" + window.location.host + response.Url;
            window.location = url;

          },
          error: function(errorResponse) {
            // Set alert for error.
            $('.alert').show()
            $('.alert-success').removeData()
            $('.alert').removeClass('alert-success')
            $('.alert').addClass('alert-warning')
            $('.alert-warning').append('<strong> Alert!</strong> ' + errorResponse.responseJSON.message )
          }
      });
    });
});
