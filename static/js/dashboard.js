    document.addEventListener("DOMContentLoaded", function () {

        const minSlider = document.getElementById("minAgeSlider");
        const maxSlider = document.getElementById("maxAgeSlider");
        const minAgeText = document.getElementById("selectedMinAge");
        const maxAgeText = document.getElementById("selectedMaxAge");
        const countText = document.getElementById("ageRangeCount");
        const progress = document.getElementById("ageSliderProgress");
        const ageRangeCard = document.querySelector(".age-range-card");

        if (!minSlider || !maxSlider || !ageRangeCard) {
            return;
        }

        function updateAgeRange() {

            let minAge = parseInt(minSlider.value);
            let maxAge = parseInt(maxSlider.value);

            if (minAge > maxAge) {
                minAge = maxAge;
                minSlider.value = minAge;
            }

            minAgeText.textContent = minAge;
            maxAgeText.textContent = maxAge;

            const minPercent = ((minAge - 1) / 104) * 100;
            const maxPercent = ((maxAge - 1) / 104) * 100;

            progress.style.left = minPercent + "%";
            progress.style.width = (maxPercent - minPercent) + "%";

            fetch(
                window.ASHA_PAGE_CONFIG.ageRangeCountUrl +
                "?min_age=" + minAge +
                "&max_age=" + maxAge
            )
            .then(response => response.json())
            .then(data => {
                countText.textContent = data.count;
            })
            .catch(error => {
                console.error("Age range error:", error);
            });
        }

        minSlider.addEventListener("input", updateAgeRange);
        maxSlider.addEventListener("input", updateAgeRange);

        /*
           Open the selected age-range member list.
           Clicking the slider itself will NOT open the page.
        */
        ageRangeCard.addEventListener("click", function (event) {

            if (event.target.closest(".age-mini-slider")) {
                return;
            }

            const minAge = parseInt(minSlider.value);
            const maxAge = parseInt(maxSlider.value);

            window.location.href =
                window.ASHA_PAGE_CONFIG.ageRangeMembersUrl +
                "?min_age=" + minAge +
                "&max_age=" + maxAge;
        });

        updateAgeRange();

    });
    document.addEventListener("DOMContentLoaded", function () {

        const workerName = document.getElementById("worker-name");

        const savedName = localStorage.getItem("asha_worker_name");

        if (savedName) {
            workerName.textContent = savedName;
        }


        workerName.addEventListener("blur", function () {

            const name = workerName.textContent.trim();

            if (name) {
                localStorage.setItem("asha_worker_name", name);
            } else {
                workerName.textContent = "Healthcare Worker";
                localStorage.setItem(
                    "asha_worker_name",
                    "Healthcare Worker"
                );
            }

        });


        workerName.addEventListener("keydown", function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                workerName.blur();

            }

        });

    });
