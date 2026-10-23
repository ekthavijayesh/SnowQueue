
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");
    const button = document.getElementById("predict-button");
    const errorBox = document.getElementById("error-message");
    const resultBox = document.getElementById("result");
    const waitTime = document.getElementById("wait-time");
    const category = document.getElementById("result-category");
    const message = document.getElementById("result-message");

    function showError(text) {
        errorBox.textContent = text;
        errorBox.hidden = false;
        resultBox.classList.remove("visible");
    }

    function clearError() {
        errorBox.textContent = "";
        errorBox.hidden = true;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearError();

        const values = new FormData(form);

        const payload = {
            ride_name: values.get("ride_name"),
            hour: Number(values.get("hour")),
            day_type: values.get("day_type"),
            weather: values.get("weather"),
            queue_length: Number(values.get("queue_length")),
            ride_capacity: Number(values.get("ride_capacity")),
            ride_cycle_minutes: Number(values.get("ride_cycle_minutes")),
            park_attendance: Number(values.get("park_attendance")),
            temperature_c: Number(values.get("temperature_c"))
        };

        if (
            !payload.ride_name ||
            !payload.day_type ||
            !payload.weather ||
            !Number.isFinite(payload.hour) ||
            !Number.isFinite(payload.queue_length) ||
            !Number.isFinite(payload.ride_capacity) ||
            !Number.isFinite(payload.ride_cycle_minutes) ||
            !Number.isFinite(payload.park_attendance) ||
            !Number.isFinite(payload.temperature_c)
        ) {
            showError("Please fill in every field correctly.");
            return;
        }

        button.disabled = true;
        button.textContent = "Predicting...";

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Prediction failed. Please try again."
                );
            }

            const minutes = Number(data.wait_time);

            if (!Number.isFinite(minutes) || minutes < 0) {
                throw new Error("The server returned an invalid prediction.");
            }

            waitTime.textContent = `${minutes} minutes`;
            category.textContent = data.category || "Estimated wait";
            message.textContent =
                data.message ||
                "This is the estimated waiting time for your selected ride.";

            if (data.disclaimer) {
                message.textContent += ` ${data.disclaimer}`;
            }

            resultBox.classList.add("visible");
            resultBox.scrollIntoView({
                behavior: "smooth",
                block: "nearest"
            });

        } catch (error) {
            showError(
                error.message ||
                "Could not connect to the prediction server."
            );
        } finally {
            button.disabled = false;
            button.textContent = "❄ Predict waiting time";
        }
    });

    // Decorative snowfall
    const snowContainer = document.getElementById("snow-container");

    if (snowContainer) {
        for (let i = 0; i < 35; i++) {
            const flake = document.createElement("span");

            flake.className = "snowflake";
            flake.textContent = "❄";
            flake.style.left = `${Math.random() * 100}%`;
            flake.style.animationDuration =
                `${6 + Math.random() * 9}s`;
            flake.style.animationDelay =
                `${Math.random() * 8}s`;
            flake.style.fontSize =
                `${8 + Math.random() * 12}px`;

            snowContainer.appendChild(flake);
        }
    }
});
