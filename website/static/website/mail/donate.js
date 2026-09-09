$(function () {
    "use strict";

    $("#donateForm").on("submit", function (event) {
        event.preventDefault();

        var $form = $(this);
        var $button = $("#donateButton");
        var $success = $("#donateMessage");

        var email = $.trim($("#donateEmail").val());
        var phone = $.trim($("#donatePhone").val());
        var message = $.trim($("#donateMessageText").val());
        var consent = $("#donateConsent").is(":checked");

        // Clear previous message
        $success.html("");

        // -----------------------------------------
        // Client-side validation
        // -----------------------------------------

        if (!email || !phone) {
            showMessage(
                "danger",
                "<strong>Not sent.</strong> Please complete all required fields."
            );
            return;
        }

        if (!consent) {
            showMessage(
                "danger",
                "<strong>Not sent.</strong> Please agree to the Privacy Policy before continuing."
            );
            return;
        }

        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            showMessage(
                "danger",
                "<strong>Not sent.</strong> Please enter a valid email address."
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
                "<strong>Not sent.</strong> Security verification failed. Please refresh the page and try again."
            );
            return;
        }

        // -----------------------------------------
        // Disable button
        // -----------------------------------------

        $button.prop("disabled", true);
        $button.html("Sending...");

        // -----------------------------------------
        // Send enquiry to Django
        // -----------------------------------------

        $.ajax({
            url: $form.attr("action"),
            type: "POST",

            data: {
                email: email,
                phone: phone,
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
                    "<strong>Thank you!</strong> We have received your donation enquiry. " +
                    "We will get back to you within a few hours."
                );

                // Clear form
                $form.trigger("reset");

                // Scroll to confirmation
                scrollToMessage();
            },

            error: function (xhr) {

                var errorMessage =
                    "We couldn't send your enquiry right now. Please try again in a few minutes.";

                if (
                    xhr.responseJSON &&
                    xhr.responseJSON.message
                ) {
                    errorMessage = xhr.responseJSON.message;
                }

                showMessage(
                    "danger",
                    "<strong>Not sent.</strong> " +
                    escapeHtml(errorMessage)
                );

                scrollToMessage();
            },

            complete: function () {

                // Always restore button
                $button.prop("disabled", false);
                $button.html("Donate Now");
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

        $("#donateMessage").html(
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

        var $message = $("#donateMessage");

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

    $("#donateEmail, #donatePhone, #donateMessageText").on(
        "focus",
        function () {
            $("#donateMessage").html("");
        }
    );

});