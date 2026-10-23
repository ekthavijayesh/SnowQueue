
const form = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");
const errorBox = document.getElementById("form-error");

const waitResult = document.getElementById("wait-result");
const waitCategory = document.getElementById("wait-category");
const resultRide = document.getElementById("result-ride");
const resultTime = document.getElementById("result-time");

const barFills = document.querySelectorAll(".bar-fill");
const maximumWait = Math.max(
    1,
    ...Array.from(barFills, (bar) => Number(bar.dataset.wait) || 0)
);

barFills.forEach((bar) => {
    const wait = Number(bar.dataset.wait) || 0;
    bar.style.width = `${Math.max(3, (wait / maximumWait) * 100)}%`;
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorBox.textContent = "";

    if (!form.reportValidity()) return;

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

    predictButton.disabled = true;
    predictButton.innerHTML = "Calculating estimate…";
    
    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to generate a prediction.");
        }

        waitResult.innerHTML =
            `${Number(data.wait_time).toFixed(1)}<span> min</span>`;

        waitCategory.textContent = `${data.category} wait`;
        resultRide.textContent = data.ride_name;
        resultTime.textContent =
            `Selected time: ${String(data.hour).padStart(2, "0")}:00`;

        document.querySelector(".result-card").scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });
    } catch (error) {
        errorBox.textContent = error.message ||
            "Something went wrong. Please try again.";
    } finally {
        predictButton.disabled = false;
        predictButton.innerHTML =
            'Calculate estimated wait <span>↗</span>';
    }
});

// Highlight the active navigation link as the user navigates.
document.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
        document.querySelectorAll(".nav-link").forEach((item) => {
            item.classList.remove("active");
        });
        link.classList.add("active");
    });
});
