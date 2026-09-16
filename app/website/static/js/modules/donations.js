const DonationManager = (() => {

    const selectors = {

        form: "#donationForm",

        amountInput: "#donationAmount",

        amountButton: ".js-donation-amount",

        submitButton: "#donationSubmit",

        buttonText: ".js-button-text",

        spinner: ".js-button-spinner",

        alert: "#donationAlert"

    };


    function init() {

        if (!$(selectors.form).length) {
            return;
        }

        bindEvents();

    }


    function bindEvents() {

        $(document).on(
            "click",
            selectors.amountButton,
            handleAmountSelection
        );


        $(selectors.form).on(
            "submit",
            handleSubmit
        );

    }


    function handleAmountSelection(event) {

        event.preventDefault();


        const $button = $(
            event.currentTarget
        );


        const amount = (
            $button.data("amount")
        );


        $(selectors.amountInput).val(
            amount
        );


        $(selectors.amountButton)
            .removeClass("active");


        $button.addClass("active");

    }


    function handleSubmit(event) {

        event.preventDefault();


        hideAlert();


        const payload = getFormData();


        if (!payload.amount) {

            showAlert(
                "Please enter a donation amount.",
                "danger"
            );

            return;

        }


        setLoading(true);


        $.ajax({

            url: "/api/donations/checkout",

            method: "POST",

            contentType: "application/json",

            data: JSON.stringify(
                payload
            )

        })

        .done(function(response) {

            handleCheckoutSuccess(
                response
            );

        })

        .fail(function(xhr) {

            handleCheckoutError(
                xhr
            );

        })

        .always(function() {

            setLoading(false);

        });

    }


    function getFormData() {

        return {

            donor_name:
                $("#donorName")
                    .val()
                    .trim(),

            donor_email:
                $("#donorEmail")
                    .val()
                    .trim(),

            donor_phone:
                $("#donorPhone")
                    .val()
                    .trim(),

            amount:
                $(selectors.amountInput)
                    .val(),

            currency:
                $(
                    '[name="currency"]'
                ).val(),

            purpose:
                $("#donationPurpose")
                    .val(),

            message:
                $("#donationMessage")
                    .val()
                    .trim(),

            is_anonymous:
                $("#anonymousDonation")
                    .is(":checked")

        };

    }


    function handleCheckoutSuccess(
        response
    ) {

        const checkoutUrl = (
            response
            && response.data
            && response.data.checkout_url
        );


        if (!checkoutUrl) {

            showAlert(
                "The payment checkout could not be opened.",
                "danger"
            );

            return;

        }


        window.location.href = (
            checkoutUrl
        );

    }


    function handleCheckoutError(xhr) {

        const response = (
            xhr.responseJSON || {}
        );


        if (response.errors) {

            showValidationErrors(
                response.errors
            );

            return;

        }


        showAlert(
            response.message
            || "We could not start the donation payment. Please try again.",
            "danger"
        );

    }


    function showValidationErrors(
        errors
    ) {

        const messages = [];


        $.each(
            errors,
            function(field, fieldErrors) {

                $.each(
                    fieldErrors,
                    function(index, message) {

                        messages.push(
                            message
                        );

                    }
                );

            }
        );


        showAlert(
            messages.join("<br>"),
            "danger"
        );

    }


    function showAlert(
        message,
        type
    ) {

        $(selectors.alert)

            .removeClass(
                "d-none alert-success alert-danger alert-warning"
            )

            .addClass(
                `alert-${type}`
            )

            .html(
                message
            );

    }


    function hideAlert() {

        $(selectors.alert)

            .addClass("d-none")

            .empty();

    }


    function setLoading(
        loading
    ) {

        $(selectors.submitButton)
            .prop(
                "disabled",
                loading
            );


        $(selectors.spinner)
            .toggleClass(
                "d-none",
                !loading
            );


        $(selectors.buttonText)
            .text(
                loading
                    ? "Preparing Payment..."
                    : "Continue to Payment"
            );

    }


    return {
        init
    };

})();


$(function() {

    DonationManager.init();

});