/* ========================================================= */
/* AGE CALCULATION */
/* ========================================================= */

function calculateAge(dateString) {

    if (!dateString) {
        return "-";
    }


    const dob =
        new Date(dateString + "T00:00:00");


    if (isNaN(dob.getTime())) {
        return "-";
    }


    const today =
        new Date();


    let age =
        today.getFullYear() -
        dob.getFullYear();


    const monthDifference =
        today.getMonth() -
        dob.getMonth();


    if (
        monthDifference < 0 ||
        (
            monthDifference === 0 &&
            today.getDate() < dob.getDate()
        )
    ) {

        age--;

    }


    return age >= 0
        ? age + " Years"
        : "-";
}



/* ========================================================= */
/* EDIT MODE DOB */
/* ========================================================= */

function calculateMemberAge() {

    const dobInput =
        document.getElementById(
            "date_of_birth"
        );


    if (!dobInput) {
        return;
    }


    const dob =
        dobInput.value;


    if (!dob) {
        return;
    }


    const date =
        new Date(
            dob + "T00:00:00"
        );


    const yearElement =
        document.getElementById(
            "dob_year"
        );


    const monthElement =
        document.getElementById(
            "dob_month"
        );


    const dayElement =
        document.getElementById(
            "dob_day"
        );


    const ageElement =
        document.getElementById(
            "age"
        );


    if (yearElement) {

        yearElement.value =
            date.getFullYear();

    }


    if (monthElement) {

        monthElement.value =
            String(
                date.getMonth() + 1
            ).padStart(2, "0");

    }


    if (dayElement) {

        dayElement.value =
            String(
                date.getDate()
            ).padStart(2, "0");

    }


    if (ageElement) {

        ageElement.value =
            calculateAge(dob);

    }

}



/* ========================================================= */
/* PREGNANCY UI IN EDIT MODE */
/* ========================================================= */

function updatePregnancyFields() {

    const gender =
        document.getElementById(
            "gender"
        );


    const pregnancyQuestion =
        document.getElementById(
            "pregnancy-question"
        );


    const pregnancySelect =
        document.getElementById(
            "currently_pregnant"
        );


    const pregnancyStartGroup =
        document.getElementById(
            "pregnancy-start-group"
        );


    const expectedDeliveryGroup =
        document.getElementById(
            "expected-delivery-group"
        );


    const pregnancyStartDate =
        document.getElementById(
            "pregnancy_start_date"
        );


    const expectedDeliveryDate =
        document.getElementById(
            "expected_delivery_date"
        );


    if (
        !gender ||
        !pregnancyQuestion ||
        !pregnancySelect ||
        !pregnancyStartGroup ||
        !expectedDeliveryGroup
    ) {

        return;

    }


    /* MALE / OTHER */

    if (gender.value !== "Female") {

        pregnancyQuestion.style.display =
            "none";

        pregnancyStartGroup.style.display =
            "none";

        expectedDeliveryGroup.style.display =
            "none";


        pregnancySelect.value =
            "No";


        if (pregnancyStartDate) {

            pregnancyStartDate.value =
                "";

        }


        if (expectedDeliveryDate) {

            expectedDeliveryDate.value =
                "";

        }


        return;

    }


    /* FEMALE */

    pregnancyQuestion.style.display =
        "block";


    /* FEMALE + NOT PREGNANT */

    if (pregnancySelect.value !== "Yes") {

        pregnancyStartGroup.style.display =
            "none";

        expectedDeliveryGroup.style.display =
            "none";


        if (pregnancyStartDate) {

            pregnancyStartDate.value =
                "";

        }


        if (expectedDeliveryDate) {

            expectedDeliveryDate.value =
                "";

        }


        return;

    }


    /* FEMALE + PREGNANT */

    pregnancyStartGroup.style.display =
        "block";

    expectedDeliveryGroup.style.display =
        "block";

}



/* ========================================================= */
/* PREGNANCY COUNTDOWN */
/* ========================================================= */

function calculatePregnancyCountdown() {

    const countdownElement =
        document.getElementById(
            "pregnancy-countdown"
        );


    if (!countdownElement) {

        return;

    }


    const expectedDate =
        new Date(
            window.ASHA_PAGE_CONFIG.expectedDeliveryDate + "T23:59:59"
        );


    if (isNaN(expectedDate.getTime())) {

        countdownElement.textContent =
            "";

        return;

    }


    function updateCountdown() {

        const now =
            new Date();


        const difference =
            expectedDate.getTime() -
            now.getTime();


        if (difference <= 0) {

            countdownElement.textContent =
                "Due Date Passed";

            return;

        }


        const days =
            Math.ceil(
                difference /
                (
                    1000 *
                    60 *
                    60 *
                    24
                )
            );


        countdownElement.textContent =
            days +
            (
                days === 1
                    ? " Day Remaining"
                    : " Days Remaining"
            );

    }


    updateCountdown();


    setInterval(
        updateCountdown,
        1000 * 60 * 60
    );

}



/* ========================================================= */
/* PAGE LOAD */
/* ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {


        /* DOB */

        const dobInput =
            document.getElementById(
                "date_of_birth"
            );


        if (dobInput) {

            calculateMemberAge();


            const today =
                new Date();


            const year =
                today.getFullYear();


            const month =
                String(
                    today.getMonth() + 1
                ).padStart(2, "0");


            const day =
                String(
                    today.getDate()
                ).padStart(2, "0");


            dobInput.max =
                year +
                "-" +
                month +
                "-" +
                day;


            dobInput.addEventListener(
                "change",
                calculateMemberAge
            );

        }



        /* DISPLAY AGE */

        const displayAge =
            document.getElementById(
                "display-age"
            );


        if (displayAge) {

            displayAge.textContent =
                calculateAge(
                    window.ASHA_PAGE_CONFIG.dateOfBirth
                );

        }



        /* PREGNANCY EDIT CONTROLS */

        const gender =
            document.getElementById(
                "gender"
            );


        const pregnancySelect =
            document.getElementById(
                "currently_pregnant"
            );


        if (gender) {

            gender.addEventListener(
                "change",
                updatePregnancyFields
            );

        }


        if (pregnancySelect) {

            pregnancySelect.addEventListener(
                "change",
                updatePregnancyFields
            );

        }


        if (gender) {

            updatePregnancyFields();

        }



        /* PREGNANCY COUNTDOWN */

        calculatePregnancyCountdown();

    }

);
