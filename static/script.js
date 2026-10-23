
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");
    const button = document.getElementById("predict-button");
    const errorBox = document.getElementById("error-message");
    const resultBox = document.getElementById("result");
    const waitTime = document.getElementById("wait-time");
    const category = document.getElementById("result-category");
    const message = document.getElementById("result-message");

    // Ensure the prediction form exists before attaching events.
    if (
        !form ||
        !button ||
        !errorBox ||
        !resultBox ||
        !waitTime ||
        !category ||
        !message
    ) {
        console.error(
            "SnowQueue: Required prediction form elements are missing."
        );
        return;
    }

    function showError(text) {
        errorBox.textContent = text;
        errorBox.hidden = false;
        resultBox.classList.remove("visible");
    }

    function clearError() {
        errorBox.textContent = "";
        errorBox.hidden = true;
    }

    function getNumericValue(formData, name) {
        const value = formData.get(name);

        if (value === null || String(value).trim() === "") {
            return NaN;
        }

        return Number(value);
    }

    function validatePayload(payload) {
        if (!payload.ride_name || !payload.day_type || !payload.weather) {
            return "Please select a ride, day type, and weather condition.";
        }

        const numericFields = [
            ["hour", payload.hour],
            ["queue length", payload.queue_length],
            ["ride capacity", payload.ride_capacity],
            ["ride cycle", payload.ride_cycle_minutes],
            ["park attendance", payload.park_attendance],
            ["temperature", payload.temperature_c]
        ];

        for (const [label, value] of numericFields) {
            if (!Number.isFinite(value)) {
                return `Please enter a valid ${label}.`;
            }
        }

        if (payload.hour < 0 || payload.hour > 23) {
            return "Please select a valid visit hour.";
        }

        if (payload.queue_length < 0) {
            return "Queue length cannot be negative.";
        }

        if (payload.ride_capacity <= 0) {
            return "Ride capacity must be greater than zero.";
        }

        if (payload.ride_cycle_minutes <= 0) {
            return "Ride cycle must be greater than zero.";
        }

        if (payload.park_attendance < 0) {
            return "Park attendance cannot be negative.";
        }

        if (payload.temperature_c < -20 || payload.temperature_c > 60) {
            return "Please enter a temperature between -20°C and 60°C.";
        }

        return null;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearError();

        // Native HTML validation first.
        if (!form.reportValidity()) {
            return;
        }

        const values = new FormData(form);

        const payload = {
            ride_name: values.get("ride_name"),
            hour: getNumericValue(values, "hour"),
            day_type: values.get("day_type"),
            weather: values.get("weather"),
            queue_length: getNumericValue(values, "queue_length"),
            ride_capacity: getNumericValue(values, "ride_capacity"),
            ride_cycle_minutes: getNumericValue(
                values,
                "ride_cycle_minutes"
            ),
            park_attendance: getNumericValue(values, "park_attendance"),
            temperature_c: getNumericValue(values, "temperature_c")
        };

        const validationError = validatePayload(payload);

        if (validationError) {
            showError(validationError);
            return;
        }

        button.disabled = true;
        button.setAttribute("aria-busy", "true");
        button.textContent = "⏳ Calculating estimate...";

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(payload)
            });

            let data;

            try {
                data = await response.json();
            } catch {
                throw new Error(
                    "The server returned an unexpected response. Please try again."
                );
            }

            if (!response.ok) {
                throw new Error(
                    data?.error ||
                    `Prediction failed (HTTP ${response.status}). Please try again.`
                );
            }

            const minutes = Number(data?.wait_time);

            if (!Number.isFinite(minutes) || minutes < 0) {
                throw new Error(
                    "The server returned an invalid prediction."
                );
            }

            // Display the prediction.
            waitTime.textContent = `${minutes.toFixed(1)} minutes`;
            category.textContent = data.category || "Estimated wait";

            message.textContent =
                data.message ||
                "This is the estimated waiting time for your selected ride.";

            if (data.disclaimer) {
                message.textContent += ` ${data.disclaimer}`;
            }

            resultBox.classList.add("visible");

            resultBox.scrollIntoView({
                behavior: window.matchMedia(
                    "(prefers-reduced-motion: reduce)"
                ).matches ? "auto" : "smooth",
                block: "nearest"
            });

        } catch (error) {
            console.error("SnowQueue prediction error:", error);

            showError(
                error.message ||
                "Could not connect to the prediction server. Please try again."
            );
        } finally {
            button.disabled = false;
            button.removeAttribute("aria-busy");
            button.textContent = "❄ Predict waiting time";
        }
    });

    // Decorative snowfall, disabled when reduced motion is preferred.
    const snowContainer = document.getElementById("snow-container");
    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (snowContainer && !reduceMotion) {
        const fragment = document.createDocumentFragment();

        for (let i = 0; i < 35; i++) {
            const flake = document.createElement("span");

            flake.className = "snowflake";
            flake.textContent = "❄";
            flake.setAttribute("aria-hidden", "true");

            flake.style.left = `${Math.random() * 100}%`;
            flake.style.animationDuration = `${6 + Math.random() * 9}s`;
            flake.style.animationDelay = `${Math.random() * 8}s`;
            flake.style.fontSize = `${8 + Math.random() * 12}px`;

            fragment.appendChild(flake);
        }

        snowContainer.appendChild(fragment);
    }
});
