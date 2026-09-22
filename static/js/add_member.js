/* =========================================================
   DOB + AGE
========================================================= */

const dobInput =
    document.getElementById("date_of_birth");


function calculateAge() {

    if (!dobInput.value) {
        return;
    }

    const dob =
        new Date(dobInput.value + "T00:00:00");

    const today =
        new Date();

    document.getElementById("dob_year").value =
        dob.getFullYear();

    document.getElementById("dob_month").value =
        dob.getMonth() + 1;

    document.getElementById("dob_day").value =
        dob.getDate();

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

    document.getElementById("age").value =
        age + " Years";
}


dobInput.addEventListener(
    "change",
    calculateAge
);


const today =
    new Date();

dobInput.max =
    today.getFullYear() +
    "-" +
    String(today.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(today.getDate()).padStart(2, "0");


/* =========================================================
   GENDER + PREGNANCY
========================================================= */

const genderSelect =
    document.getElementById("gender");

const pregnancySection =
    document.getElementById("pregnancy_section");

const pregnancySelect =
    document.getElementById("currently_pregnant");

const pregnancyDates =
    document.getElementById("pregnancy_dates");

const pregnancyStartDate =
    document.getElementById("pregnancy_start_date");

const expectedDeliveryDate =
    document.getElementById("expected_delivery_date");


function updatePregnancySection() {

    const gender =
        genderSelect.value;

    if (gender === "Female") {

        pregnancySection.style.display =
            "flex";

        pregnancySelect.required =
            true;

    } else {

        pregnancySection.style.display =
            "none";

        pregnancySelect.value =
            "";

        pregnancySelect.required =
            false;

        pregnancyDates.style.display =
            "none";

        pregnancyStartDate.value =
            "";

        expectedDeliveryDate.value =
            "";

        pregnancyStartDate.required =
            false;

        expectedDeliveryDate.required =
            false;
    }
}


function updatePregnancyDates() {

    if (
        genderSelect.value === "Female" &&
        pregnancySelect.value === "Yes"
    ) {

        pregnancyDates.style.display =
            "flex";

        pregnancyStartDate.required =
            true;

        expectedDeliveryDate.required =
            true;

    } else {

        pregnancyDates.style.display =
            "none";

        pregnancyStartDate.value =
            "";

        expectedDeliveryDate.value =
            "";

        pregnancyStartDate.required =
            false;

        expectedDeliveryDate.required =
            false;
    }
}


genderSelect.addEventListener(
    "change",
    updatePregnancySection
);


pregnancySelect.addEventListener(
    "change",
    updatePregnancyDates
);


/* =========================================================
   RELIGION + CASTE SAVED OPTIONS
========================================================= */

function loadSavedOptions(
    storageKey,
    selectElement
) {

    const savedOptions =
        JSON.parse(
            localStorage.getItem(storageKey) || "[]"
        );

    savedOptions.forEach(
        function (value) {

            const option =
                document.createElement("option");

            option.value =
                value;

            option.textContent =
                value;

            selectElement.appendChild(
                option
            );

        }
    );
}


function saveOption(
    storageKey,
    inputElement,
    selectElement,
    inputBox
) {

    const value =
        inputElement.value.trim();

    if (!value) {
        return;
    }

    let savedOptions =
        JSON.parse(
            localStorage.getItem(storageKey) || "[]"
        );

    const alreadyExists =
        savedOptions.some(
            function (item) {

                return item.toLowerCase() ===
                    value.toLowerCase();

            }
        );

    if (!alreadyExists) {

        savedOptions.push(value);

        localStorage.setItem(
            storageKey,
            JSON.stringify(savedOptions)
        );

        const option =
            document.createElement("option");

        option.value =
            value;

        option.textContent =
            value;

        selectElement.appendChild(
            option
        );

    }

    selectElement.value =
        value;

    inputElement.value =
        "";

    inputBox.style.display =
        "none";
}


/* RELIGION */

const religionSelect =
    document.getElementById("religion");

const religionInputBox =
    document.getElementById("religion_input_box");

const newReligion =
    document.getElementById("new_religion");

const addReligionBtn =
    document.getElementById("add_religion_btn");

const saveReligionBtn =
    document.getElementById("save_religion_btn");


loadSavedOptions(
    "asha_care_religions",
    religionSelect
);


addReligionBtn.addEventListener(
    "click",
    function () {

        if (
            religionInputBox.style.display ===
            "flex"
        ) {

            religionInputBox.style.display =
                "none";

        } else {

            religionInputBox.style.display =
                "flex";

            newReligion.focus();

        }

    }
);


saveReligionBtn.addEventListener(
    "click",
    function () {

        saveOption(
            "asha_care_religions",
            newReligion,
            religionSelect,
            religionInputBox
        );

    }
);


newReligion.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            saveOption(
                "asha_care_religions",
                newReligion,
                religionSelect,
                religionInputBox
            );

        }

    }
);


/* CASTE */

const casteSelect =
    document.getElementById("caste");

const casteInputBox =
    document.getElementById("caste_input_box");

const newCaste =
    document.getElementById("new_caste");

const addCasteBtn =
    document.getElementById("add_caste_btn");

const saveCasteBtn =
    document.getElementById("save_caste_btn");


loadSavedOptions(
    "asha_care_castes",
    casteSelect
);


addCasteBtn.addEventListener(
    "click",
    function () {

        if (
            casteInputBox.style.display ===
            "flex"
        ) {

            casteInputBox.style.display =
                "none";

        } else {

            casteInputBox.style.display =
                "flex";

            newCaste.focus();

        }

    }
);


saveCasteBtn.addEventListener(
    "click",
    function () {

        saveOption(
            "asha_care_castes",
            newCaste,
            casteSelect,
            casteInputBox
        );

    }
);


newCaste.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            saveOption(
                "asha_care_castes",
                newCaste,
                casteSelect,
                casteInputBox
            );

        }

    }
);
