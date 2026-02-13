// ===============================
// API Configuration (IMPORTANT)
// ===============================
const BASE_URL = "https://stock-backend.onrender.com";
const API_URL = `${BASE_URL}/predict`;


// ===============================
// LOAD COMPANIES FROM BACKEND
// ===============================
async function loadCompanies() {

    try {

        const response = await fetch(`${BASE_URL}/companies`);

        if (!response.ok)
            throw new Error("Failed to load companies");

        const companies = await response.json();

        const select = document.getElementById("company");

        // clear existing
        select.innerHTML =
            '<option value="">Select Company</option>';

        companies.forEach(company => {

            const option =
                document.createElement("option");

            option.value = company;
            option.textContent = company;

            select.appendChild(option);

        });

    } catch (error) {

        console.error("Error:", error);
        showError("Cannot load companies");

    }

}


// ===============================
// LOAD LATEST PRICE
// ===============================
async function loadLatestPrice(company) {

    if (!company) return;

    try {

        const response = await fetch(
            `${BASE_URL}/latest/${company}`
        );

        if (!response.ok)
            throw new Error("Failed latest price");

        const data = await response.json();

        document.getElementById("open").value =
            data.open;

        document.getElementById("high").value =
            data.high;

        document.getElementById("low").value =
            data.low;

        document.getElementById("close").value =
            data.close;

    } catch (error) {

        console.error(error);
        showError("Cannot load latest price");

    }

}


// ===============================
// DOM ELEMENTS
// ===============================
const predictionForm =
    document.getElementById("predictionForm");

const predictBtn =
    document.getElementById("predictBtn");

const btnText =
    document.getElementById("btnText");

const btnLoader =
    document.getElementById("btnLoader");

const errorMessage =
    document.getElementById("errorMessage");

const errorText =
    document.getElementById("errorText");

const resultSection =
    document.getElementById("resultSection");

const currentPrice =
    document.getElementById("currentPrice");

const predictedPrice =
    document.getElementById("predictedPrice");

const trendIcon =
    document.getElementById("trendIcon");

const trendValue =
    document.getElementById("trendValue");


// form inputs
const companySelect =
    document.getElementById("company");

const openInput =
    document.getElementById("open");

const highInput =
    document.getElementById("high");

const lowInput =
    document.getElementById("low");

const closeInput =
    document.getElementById("close");


// ===============================
// ERROR HANDLING
// ===============================
function showError(message) {

    errorText.textContent = message;
    errorMessage.style.display = "flex";

    resultSection.style.display = "none";

}

function hideError() {

    errorMessage.style.display = "none";

}


// ===============================
// LOADING STATE
// ===============================
function showLoading() {

    predictBtn.disabled = true;
    btnText.style.display = "none";
    btnLoader.style.display = "inline-block";

}

function hideLoading() {

    predictBtn.disabled = false;
    btnText.style.display = "inline";
    btnLoader.style.display = "none";

}


// ===============================
// VALIDATION
// ===============================
function validateInputs(data) {

    if (!data.company)
        throw new Error("Select company");

    if (
        data.open <= 0 ||
        data.high <= 0 ||
        data.low <= 0 ||
        data.close <= 0
    )
        throw new Error("Invalid price");

    if (data.high < data.low)
        throw new Error("High < Low");

}


// ===============================
// FORMAT CURRENCY
// ===============================
function formatCurrency(value) {

    return "₹" + parseFloat(value).toFixed(2);

}


// ===============================
// DISPLAY RESULT
// ===============================
function displayResults(result, closePrice) {

    resultSection.style.display = "block";

    currentPrice.textContent =
        formatCurrency(closePrice);

    predictedPrice.textContent =
        formatCurrency(result.prediction);

    if (result.trend === "UP") {

        trendIcon.textContent = "📈";
        trendValue.textContent = "UPWARD";
        trendValue.className = "trend-value up";

    } else {

        trendIcon.textContent = "📉";
        trendValue.textContent = "DOWNWARD";
        trendValue.className = "trend-value down";

    }

}


// ===============================
// MAKE PREDICTION
// ===============================
async function makePrediction(data) {

    const response =
        await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(data)

        });

    if (!response.ok)
        throw new Error("Backend error");

    return await response.json();

}


// ===============================
// FORM SUBMIT
// ===============================
async function handleSubmit(e) {

    e.preventDefault();

    const data = {

        company: companySelect.value,

        open:
            parseFloat(openInput.value),

        high:
            parseFloat(highInput.value),

        low:
            parseFloat(lowInput.value),

        close:
            parseFloat(closeInput.value)

    };

    try {

        validateInputs(data);

        showLoading();

        const result =
            await makePrediction(data);

        displayResults(
            result,
            data.close
        );

    } catch (error) {

        showError(error.message);

    } finally {

        hideLoading();

    }

}


// ===============================
// INIT
// ===============================
function init() {

    loadCompanies();

    predictionForm.addEventListener(
        "submit",
        handleSubmit
    );

    companySelect.addEventListener(
        "change",
        function () {

            loadLatestPrice(
                this.value
            );

        }
    );

}


// ===============================
// START APP
// ===============================
document.addEventListener(
    "DOMContentLoaded",
    init
);
