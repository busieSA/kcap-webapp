const DashboardApp = (() => {

    const selectors = {
        logoutButton: ".js-logout"
    };


    function init() {
        bindEvents();
    }


    function bindEvents() {

        $(document).on(
            "click",
            selectors.logoutButton,
            handleLogout
        );

    }


    function handleLogout(event) {

        event.preventDefault();

        $.ajax({
            url: "/api/auth/logout",
            method: "POST"
        })
        .done(function () {

            window.location.href = "/admin/login";

        })
        .fail(function (xhr) {

            console.error(
                "Logout failed:",
                xhr.responseJSON || xhr.responseText
            );

        });

    }


    return {
        init
    };

})();


$(function () {

    DashboardApp.init();

});