$(function () {
    "use strict";

    $("#contactForm").on("submit", function (event) {
        event.preventDefault();

        var $form = $(this);
        var $button = $("#sendMessageButton");
        var $success = $("#success");

        var name = $.trim($("#name").val());
        var email = $.trim($("#email").val());
        var subject = $.trim($("#subject").val());
        var message = $.trim($("#message").val());
        var consent = $("#contactConsent").is(":checked");

        // Clear previous message
        $success.html("");

        // Basic validation
        if (!name || !email || !subject || !message) {
            $success.html(
                "<div class='alert alert-danger'>" +
                "Please complete all required fields." +
                "</div>"
            );
            return;
        }

        if (!consent) {
            $success.html(
                "<div class='alert alert-danger'>" +
                "Please agree to the Privacy Policy before sending your message." +
                "</div>"
            );
            return;
        }

        // Basic email validation
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            $success.html(
                "<div class='alert alert-danger'>" +
                "Please enter a valid email address." +
                "</div>"
            );
            return;
        }

        // Disable button while sending
        $button.prop("disabled", true);
        $button.html("Sending...");

        // Get Django CSRF token
        var csrftoken = getCookie("csrftoken");

        $.ajax({
            url: "/contact/send/",
            type: "POST",
            data: {
                name: name,
                email: email,
                subject: subject,
                message: message,
                consent: consent
            },
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {

                $success.html(
                    "<div class='alert alert-success'>" +
                    "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                    "<strong>Thank you!</strong> We have received your message. " +
                    "We will get back to you within a few hours." +
                    "</div>"
                );

                $form.trigger("reset");

                // Scroll user to confirmation
                $("html, body").animate({
                    scrollTop: $success.offset().top - 100
                }, 400);
            },

            error: function (xhr) {

                var errorMessage =
                    "Sorry, we couldn't send your message right now. Please try again later.";

                if (
                    xhr.responseJSON &&
                    xhr.responseJSON.message
                ) {
                    errorMessage = xhr.responseJSON.message;
                }

                $success.html(
                    "<div class='alert alert-danger'>" +
                    "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
                    "<strong>Message not sent.</strong> " +
                    errorMessage +
                    "</div>"
                );

                $("html, body").animate({
                    scrollTop: $success.offset().top - 100
                }, 400);
            },

            complete: function () {

                $button.prop("disabled", false);
                $button.html("Send Message");

            }
        });
    });

    /*
     * Get Django CSRF cookie
     */
    function getCookie(name) {

        var cookieValue = null;

        if (document.cookie && document.cookie !== "") {

            var cookies = document.cookie.split(";");

            for (var i = 0; i < cookies.length; i++) {

                var cookie = $.trim(cookies[i]);

                if (cookie.substring(0, name.length + 1) === (name + "=")) {

                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;
                }
            }
        }

        return cookieValue;
    }

    /*
     * Clear confirmation/error message when user starts typing again.
     */
    $("#name, #email, #subject, #message").on("focus", function () {
        $("#success").html("");
    });

});