const EnquiryManager = (() => {

    const selectors = {
        resolveButton: ".js-resolve-enquiry",
        reopenButton: ".js-reopen-enquiry",
        archiveButton: ".js-archive-enquiry",
        statusBadge: "#enquiryStatus"
    };


    function init() {
        bindEvents();
    }


    function bindEvents() {

        $(document).on(
            "click",
            selectors.resolveButton,
            handleResolve
        );

        $(document).on(
            "click",
            selectors.reopenButton,
            handleReopen
        );

        $(document).on(
            "click",
            selectors.archiveButton,
            handleArchive
        );

    }


    function handleResolve(event) {

        event.preventDefault();

        const enquiryId = (
            $(this).data("id")
        );

        changeStatus(
            enquiryId,
            "resolve"
        );

    }


    function handleReopen(event) {

        event.preventDefault();

        const enquiryId = (
            $(this).data("id")
        );

        changeStatus(
            enquiryId,
            "reopen"
        );

    }


    function handleArchive(event) {

        event.preventDefault();

        const enquiryId = (
            $(this).data("id")
        );

        if (
            !window.confirm(
                "Archive this enquiry?"
            )
        ) {
            return;
        }

        archiveEnquiry(
            enquiryId
        );

    }


    function changeStatus(
        enquiryId,
        action
    ) {

        $.ajax({
            url: `/admin/api/enquiries/${enquiryId}/${action}`,
            method: "POST"
        })
        .done(function (response) {

            updateStatusUI(
                response.data
            );

        })
        .fail(handleRequestError);

    }


    function archiveEnquiry(
        enquiryId
    ) {

        $.ajax({
            url: `/admin/api/enquiries/${enquiryId}/archive`,
            method: "POST"
        })
        .done(function () {

            const row = $(
                `#enquiry-row-${enquiryId}`
            );

            if (row.length) {

                row.fadeOut(
                    200,
                    function () {
                        $(this).remove();
                    }
                );

                return;
            }

            window.location.href =
                "/admin/enquiries";

        })
        .fail(handleRequestError);

    }


    function updateStatusUI(data) {

        const badge = $(
            selectors.statusBadge
        );

        if (!badge.length) {
            window.location.reload();
            return;
        }

        badge
            .removeClass(
                "text-bg-warning " +
                "text-bg-secondary " +
                "text-bg-success"
            );

        if (data.status === "resolved") {

            badge
                .addClass("text-bg-success")
                .text("Resolved");

            replaceActionButton(
                "reopen"
            );

        } else if (data.status === "read") {

            badge
                .addClass("text-bg-secondary")
                .text("Read");

            replaceActionButton(
                "resolve"
            );

        } else {

            badge
                .addClass("text-bg-warning")
                .text("New");

        }

    }


    function replaceActionButton(
        action
    ) {

        const enquiryId = (
            $("#enquiryCard")
            .data("enquiry-id")
        );

        if (action === "reopen") {

            $(selectors.resolveButton)
                .replaceWith(`
                    <button
                        type="button"
                        class="btn btn-warning js-reopen-enquiry"
                        data-id="${enquiryId}"
                    >
                        <i class="bi bi-arrow-counterclockwise me-1"></i>
                        Reopen
                    </button>
                `);

            return;

        }

        $(selectors.reopenButton)
            .replaceWith(`
                <button
                    type="button"
                    class="btn btn-success js-resolve-enquiry"
                    data-id="${enquiryId}"
                >
                    <i class="bi bi-check-circle me-1"></i>
                    Resolve
                </button>
            `);

    }


    function handleRequestError(xhr) {

        if (xhr.status === 401) {

            window.location.href =
                "/admin/login";

            return;
        }


        const response =
            xhr.responseJSON || {};


        const message =
            response.message
            || "Something went wrong.";


        window.alert(
            message
        );

    }


    return {
        init
    };

})();


$(function () {

    EnquiryManager.init();

});