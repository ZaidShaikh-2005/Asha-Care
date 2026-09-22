    function calculateAge(dob) {

        if (!dob) {
            return "—";
        }

        const birthDate = new Date(dob);

        if (isNaN(birthDate.getTime())) {
            return "—";
        }

        const today = new Date();

        let age =
            today.getFullYear() -
            birthDate.getFullYear();

        const monthDifference =
            today.getMonth() -
            birthDate.getMonth();

        if (
            monthDifference < 0 ||
            (
                monthDifference === 0 &&
                today.getDate() < birthDate.getDate()
            )
        ) {
            age--;
        }

        return age + " years";
    }


    document
        .querySelectorAll(".member-age")
        .forEach(function(element) {

            const dob =
                element.getAttribute("data-dob");

            element.textContent =
                calculateAge(dob);

        });
