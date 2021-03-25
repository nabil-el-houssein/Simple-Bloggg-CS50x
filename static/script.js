$(document).ready(function() {

    // Runs only in /login or /register
    if (top.location.pathname === '/login' || top.location.pathname === '/register') {
        // Open reigster tab when "not a member" is clicked (login.html)
        $("#reg").click(function(e) {
            e.preventDefault();
            $('.nav-pills .nav-item a[href="#pills-register"]').tab("show");
        });

        // Open login tab when "already a member" is clicked (login.html)
        $("#log").click(function(e) {
            e.preventDefault();
            $('.nav-pills .nav-item a[href="#pills-login"]').tab("show");
        });

        // Enabling the log in button only when the login fields are not empty
        $(".login input").keyup(function() {
            var empty = false;
            $(".login input").each(function() {
                if ($(this).val().length == 0) {
                    empty = true;
                }
            });

            if (empty) {
                $("#login").attr("disabled", "disabled");
            } else {
                $("#login").removeAttr("disabled");
            }
        });

        // Enabling the register button only when the register fields are not empty and the checkbox checked
        $(document).ready(() => {
            $("input[type=text]").keyup(onFormUpdate);
            $("input[type=password]").keyup(onFormUpdate);
            $("input[type=checkbox]").change(onFormUpdate);
        });


        // Manipulating the password fields in register
        $("#registerPassword").keydown(function() {
            $("#registerPassword, #registerConfirmPassword").keyup(function() {
                $("#registerPassword, #registerConfirmPassword").each(function() {
                    // Checks password length
                    if ($("#registerPassword").val().length < 8 || $("#registerPassword").val()
                        .length > 25) {
                        $("#passwordHelp").html("Must be 8-25 characters long.");
                        $('#pass').attr('class', 'form-outline mb-2 register');
                    } else if ($("#registerPassword").val().length > 8 || $("#registerPassword")
                        .val().length < 25) {
                        $('#pass').attr('class', 'form-outline mb-4 register');
                        $("#passwordHelp").empty();
                    }

                    // Checks if passwords match when confirmPassword is not null
                    if ($("#registerPassword").val() !== $("#registerConfirmPassword").val() && $(
                            "#registerConfirmPassword").val()) {
                        // Perform error style and add an error text
                        $('#confirm-pass').attr('class', 'form-outline mb-2 register');
                        $("#registerPassword").addClass("form-control is-invalid");
                        $("#registerConfirmPassword").addClass("form-control is-invalid");
                        $("#confirmPasswordHelp").html("Passwords do not match");
                    } else {
                        // return style to normal and remove error text
                        $('#confirm-pass').attr('class', 'form-outline mb-4 register');
                        $("#registerPassword").removeClass("is-invalid");
                        $("#registerConfirmPassword").removeClass("is-invalid");
                        $("#confirmPasswordHelp").empty();
                    }
                });
            });
        });

        // Removes special characters in username at register
        $("#registerUsername").keyup(function() {
            $(this).val($(this).val().replace(/[^a-zA-Z0-9-_]/g, ''));
        })
    }

    // Runs only in /profile
    if (top.location.pathname === '/profile') {
        // Shows modal whenever a button is clicked except the changePassword button and the navbar-toggler
        $("button:not('#changePassword, .navbar-toggler')").click(function() {
            $('#editProfile').modal('show');
        })

        // Closes the modal when the close button is clicked
        $("#closeModal").click(function() {
            $('#editProfile').modal('hide')
        })

        // Datepicker format
        $('.date .datepicker').datepicker({
            'format': 'dd-mm-yyyy',
            'autoclose': true,
        });

        // Allow only numbers, hyphen and plus in phone number
        $("[name='phone']").keyup(function() {
            $(this).val($(this).val().replace(/[^0-9-+()]/g, ''));
        })


        // Link manipulating
        $('#website').keyup(function() {
            $('#website').val(getValidUrl($(this).val()))
        })

        $('#github').keyup(function() {
            $('#github').val(getValidUrl($(this).val()))
        })

        $('#twitter').keyup(function() {
            $('#twitter').val(getValidUrl($(this).val()))
        })

        $('#instagram').keyup(function() {
            $('#instagram').val(getValidUrl($(this).val()))
        })

        $('#facebook').keyup(function() {
            $('#facebook').val(getValidUrl($(this).val()))
        })

    }

    // Runs only in /changePassword
    if (top.location.pathname === '/changePassword') {

        // Checks if fields are empty
        $("input").keyup(function() {
            var empty = false;
            $("input").each(function() {
                if ($(this).val().length == 0) {
                    empty = true;
                }
            });

            if (empty) {
                $("button").attr("disabled", "disabled");
            } else {
                $("button").removeAttr("disabled");
            }
        });
    }

    // Runs only in /createBlog
    if (top.location.pathname === '/createBlog') {
        $("input, textarea").keyup(function() {
            var empty = false;
            $("input, textarea").each(function() {
                if ($(this).val().length == 0) {
                    empty = true;
                }
            });

            if (empty) {
                $("button").attr("disabled", "disabled");
            } else {
                $("button").removeAttr("disabled");
            }
        });
    }

});

/*
    onFormUpdate() is implemented for a corner case
    https://stackoverflow.com/q/66707517/15432055
*/

function onFormUpdate() {
    const registerName = $("#registerName").val();
    const registerUsername = $("#registerUsername").val();
    const registerEmail = $("#registerEmail").val();
    const registerPassword = $("#registerPassword").val();
    const registerConfirmPassword = $("#registerConfirmPassword").val();
    const registerCheck = $("#registerCheck").prop("checked");

    if (registerPassword !== registerConfirmPassword || registerPassword.length < 8 || registerPassword.length > 25) {
        $("#register").attr("disabled", "disabled");
    } else if (registerName && registerUsername && registerEmail && registerPassword && registerConfirmPassword && registerCheck) {
        $("#register").removeAttr("disabled");
    } else {
        $("#register").attr("disabled", "disabled");
    }
}

/*
  https://stackoverflow.com/questions/16485012/jquery-update-textbox-value-while-typing-on-another-textbox
*/

// A function to append "http" or "https" to a url
function getValidUrl(url) {
    let newUrl = window.decodeURIComponent(url);
    newUrl = newUrl.trim().replace(/\s/g, "");

    if (/^(:\/\/)/.test(newUrl)) {
        return `http${newUrl}`;
    }
    if (!/^(f|ht)tps?:\/\//i.test(newUrl)) {
        return `http://${newUrl}`;
    }

    return newUrl;
};
