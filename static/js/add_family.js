    const villageSelect =
        document.getElementById("village");

    const houseSelect =
        document.getElementById("house_number");


    villageSelect.addEventListener(
        "change",
        function () {

            const selectedOption =
                this.options[this.selectedIndex];

            const totalHouses =
                parseInt(
                    selectedOption.dataset.houses
                );


            houseSelect.innerHTML = "";


            if (
                !selectedOption.value ||
                !totalHouses ||
                totalHouses < 1
            ) {

                houseSelect.disabled = true;

                const option =
                    document.createElement("option");

                option.value = "";

                option.textContent =
                    "Select Village First";

                houseSelect.appendChild(option);

                return;
            }


            houseSelect.disabled = false;


            const defaultOption =
                document.createElement("option");

            defaultOption.value = "";

            defaultOption.textContent =
                "Select House Number";

            houseSelect.appendChild(
                defaultOption
            );


            for (
                let i = 1;
                i <= totalHouses;
                i++
            ) {

                const option =
                    document.createElement("option");

                option.value = i;

                option.textContent =
                    String(i).padStart(4, "0");

                houseSelect.appendChild(
                    option
                );

            }

        }
    );
