const WebsiteApp = (() => {

    const selectors = {

        currentYear:
            ".js-current-year"

    };


    function init() {

        setCurrentYear();

        bindEvents();

    }


    function bindEvents() {

        // Global website events
        // will live here.

    }


    function setCurrentYear() {

        const year = (
            new Date().getFullYear()
        );


        $(selectors.currentYear)
            .text(year);

    }


    return {
        init
    };

})();


$(function() {

    WebsiteApp.init();

});

