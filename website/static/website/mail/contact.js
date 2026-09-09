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

        // -----------------------------------------
        // Client-side validation
        // -----------------------------------------

        if (!name || !email || !subject || !message) {
            showMessage(
                "danger",
                "<strong>Message not sent.</strong> Please complete all required fields."
            );
            return;
        }

        if (!consent) {
            showMessage(
                "danger",
                "<strong>Message not sent.</strong> Please agree to the Privacy Policy before sending your message."
            );
            return;
        }

        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            showMessage(
                "danger",
                "<strong>Message not sent.</strong> Please enter a valid email address."
            );
            return;
        }

        // -----------------------------------------
        // Get CSRF token directly from Django form
        // -----------------------------------------

        var csrftoken = $form
            .find('input[name="csrfmiddlewaretoken"]')
            .val();

        if (!csrftoken) {
            showMessage(
                "danger",
                "<strong>Message not sent.</strong> Security verification failed. Please refresh the page and try again."
            );
            return;
        }

        // -----------------------------------------
        // Disable button
        // -----------------------------------------

        $button.prop("disabled", true);
        $button.html("Sending...");

        // -----------------------------------------
        // Send message to Django
        // -----------------------------------------

        $.ajax({
            url: "/contact/send/",
            type: "POST",

            data: {
                name: name,
                email: email,
                subject: subject,
                message: message,
                consent: consent ? "true" : "false",
                csrfmiddlewaretoken: csrftoken
            },

            headers: {
                "X-CSRFToken": csrftoken
            },

            success: function (response) {

                showMessage(
                    "success",
                    "<strong>Thank you!</strong> We have received your message. " +
                    "We will get back to you within a few hours."
                );

                // Clear form
                $form.trigger("reset");

                // Scroll to confirmation
                scrollToMessage();
            },

            error: function (xhr) {

                var errorMessage =
                    "We couldn't send your message right now. Please try again in a few minutes.";

                // -----------------------------------------
                // Django returned a clean error
                // -----------------------------------------

                if (
                    xhr.responseJSON &&
                    xhr.responseJSON.message
                ) {
                    errorMessage = xhr.responseJSON.message;
                }

                showMessage(
                    "danger",
                    "<strong>Message not sent.</strong> " +
                    escapeHtml(errorMessage)
                );

                scrollToMessage();
            },

            complete: function () {

                // Always restore button
                $button.prop("disabled", false);
                $button.html("Send Message");
            }
        });
    });


    // -----------------------------------------
    // Display message
    // -----------------------------------------

    function showMessage(type, message) {

        var closeButton =
            "<button type='button' " +
            "class='close' " +
            "data-dismiss='alert' " +
            "aria-hidden='true'>" +
            "&times;" +
            "</button>";

        $("#success").html(
            "<div class='alert alert-" +
            type +
            "'>" +
            closeButton +
            message +
            "</div>"
        );
    }


    // -----------------------------------------
    // Scroll to message
    // -----------------------------------------

    function scrollToMessage() {

        var $message = $("#success");

        if ($message.length) {
            $("html, body").animate(
                {
                    scrollTop: $message.offset().top - 100
                },
                400
            );
        }
    }


    // -----------------------------------------
    // Escape backend text before displaying it
    // -----------------------------------------

    function escapeHtml(text) {

        return $("<div>")
            .text(text)
            .html();
    }


    // -----------------------------------------
    // Clear old message when user starts typing
    // -----------------------------------------

    $("#name, #email, #subject, #message").on(
        "focus",
        function () {
            $("#success").html("");
        }
    );

});