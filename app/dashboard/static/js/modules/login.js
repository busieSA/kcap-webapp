const LoginManager = (() => {

    const selectors = {

        form: "#loginForm",

        email: "#email",
        password: "#password",

        loginButton: "#loginButton",

        loginLabel: ".js-login-label",
        loginSpinner: ".js-login-spinner",

        loginError: "#loginError",

        emailError: "#emailError",
        passwordError: "#passwordError",

        togglePassword:
            ".js-toggle-password"

    };


    function init() {

        bindEvents();

    }


    function bindEvents() {

        $(selectors.form).on(
            "submit",
            handleSubmit
        );


        $(document).on(
            "click",
            selectors.togglePassword,
            handlePasswordToggle
        );

    }


    function handleSubmit(event) {

        event.preventDefault();

        clearErrors();


        const payload = {

            email:
                $(selectors.email)
                .val()
                .trim(),

            password:
                $(selectors.password)
                .val()

        };


        setLoading(true);


        authenticate(payload);

    }


    function authenticate(payload) {

        $.ajax({

            url: "/api/auth/login",

            method: "POST",

            contentType:
                "application/json",

            data: JSON.stringify(
                payload
            )

        })

        .done(function () {

            window.location.href =
                "/admin/";

        })

        .fail(function (xhr) {

            handleLoginError(xhr);

        })

        .always(function () {

            setLoading(false);

        });

    }


    function handleLoginError(xhr) {

        const response =
            xhr.responseJSON || {};


        if (response.errors) {

            displayValidationErrors(
                response.errors
            );

            return;

        }


        showGeneralError(
            response.message
            || "Unable to sign in."
        );

    }


    function displayValidationErrors(
        errors
    ) {

        if (errors.email) {

            showFieldError(
                selectors.email,
                selectors.emailError,
                errors.email[0]
            );

        }


        if (errors.password) {

            showFieldError(
                selectors.password,
                selectors.passwordError,
                errors.password[0]
            );

        }

    }


    function showFieldError(
        fieldSelector,
        errorSelector,
        message
    ) {

        $(fieldSelector)
            .addClass("is-invalid");


        $(errorSelector)
            .text(message);

    }


    function showGeneralError(
        message
    ) {

        $(selectors.loginError)
            .text(message)
            .removeClass("d-none");

    }


    function clearErrors() {

        $(selectors.loginError)
            .addClass("d-none")
            .text("");


        $(selectors.email)
            .removeClass("is-invalid");


        $(selectors.password)
            .removeClass("is-invalid");


        $(selectors.emailError)
            .text("");


        $(selectors.passwordError)
            .text("");

    }


    function setLoading(
        isLoading
    ) {

        $(selectors.loginButton)
            .prop(
                "disabled",
                isLoading
            );


        $(selectors.loginSpinner)
            .toggleClass(
                "d-none",
                !isLoading
            );


        $(selectors.loginLabel)
            .text(
                isLoading
                    ? "Signing In"
                    : "Sign In"
            );

    }


    function handlePasswordToggle() {

        const passwordField =
            $(selectors.password);


        const isPassword =
            passwordField.attr("type")
            === "password";


        passwordField.attr(
            "type",
            isPassword
                ? "text"
                : "password"
        );


        const icon =
            $(this).find("i");


        icon.toggleClass(
            "bi-eye",
            !isPassword
        );


        icon.toggleClass(
            "bi-eye-slash",
            isPassword
        );

    }


    return {

        init

    };

})();


$(function () {

    LoginManager.init();

});