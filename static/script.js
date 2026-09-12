// --------------------------------
// LOAD DASHBOARD
// --------------------------------

async function loadDashboard() {

    const response =
        await fetch("/api/dashboard");

    const data =
        await response.json();

    document.getElementById(
        "reserve"
    ).innerText =
        data.total_reserve + " M";

    document.getElementById(
        "production"
    ).innerText =
        data.today_production;

    document.getElementById(
        "expected"
    ).innerText =
        data.expected_production;

    document.getElementById(
        "risk"
    ).innerText =
        data.risk;

    document.getElementById(
        "riskPercent"
    ).innerText =
        data.shortfall_percentage +
        "% shortfall";
}


// --------------------------------
// RESERVE PREDICTION
// --------------------------------

async function predictReserve() {

    const input = {

        depth:
            document.getElementById(
                "depth"
            ).value,

        grade:
            document.getElementById(
                "grade"
            ).value,

        ndvi:
            document.getElementById(
                "ndvi"
            ).value,

        soil_moisture:
            document.getElementById(
                "soil"
            ).value,

        temperature:
            document.getElementById(
                "temperature"
            ).value
    };


    const response =
        await fetch(
            "/api/predict_reserve",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(input)
            }
        );


    const result =
        await response.json();


    document.getElementById(
        "reserveResult"
    ).innerText =
        "Predicted Reserve: "
        + result.predicted_reserve
        + " units";
}


// --------------------------------
// PRODUCTION PREDICTION
// --------------------------------

async function predictProduction() {

    const input = {

        rainfall:
            document.getElementById(
                "rainfall"
            ).value,

        downtime:
            document.getElementById(
                "downtime"
            ).value,

        blasting_delay:
            document.getElementById(
                "blasting"
            ).value,

        temperature:
            document.getElementById(
                "temp2"
            ).value,

        soil_moisture:
            document.getElementById(
                "soil2"
            ).value,

        target_production:
            document.getElementById(
                "target"
            ).value
    };


    const response =
        await fetch(
            "/api/predict_production",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(input)
            }
        );


    const result =
        await response.json();


    document.getElementById(
        "productionResult"
    ).innerHTML =

        "Predicted Production: "
        + result.predicted_production
        + " tonnes<br>"
        + "Expected Shortfall: "
        + result.shortfall
        + " tonnes<br>"
        + "Risk: "
        + result.risk;
}


// --------------------------------
// LOAD RECOMMENDATIONS
// --------------------------------

async function loadRecommendations() {

    const response =
        await fetch(
            "/api/recommendations"
        );

    const data =
        await response.json();

    const list =
        document.getElementById(
            "recommendations"
        );

    list.innerHTML = "";

    data.recommendations.forEach(
        function(item) {

            const li =
                document.createElement(
                    "li"
                );

            li.innerText = item;

            list.appendChild(li);
        }
    );
}


// --------------------------------
// PRODUCTION GRAPH
// --------------------------------

async function createChart() {

    const response =
        await fetch(
            "/api/dashboard"
        );

    const dashboard =
        await response.json();

    const productionData = [
        7500,
        8000,
        8300,
        8500,
        9000,
        9200,
        dashboard.today_production
    ];

    const targetData = [
        10000,
        10000,
        10000,
        10000,
        10000,
        10000,
        dashboard.expected_production
    ];


    new Chart(

        document.getElementById(
            "productionChart"
        ),

        {
            type: "line",

            data: {

                labels: [
                    "Day 1",
                    "Day 2",
                    "Day 3",
                    "Day 4",
                    "Day 5",
                    "Day 6",
                    "Today"
                ],

                datasets: [

                    {
                        label:
                            "Actual Production",

                        data:
                            productionData
                    },

                    {
                        label:
                            "Target Production",

                        data:
                            targetData
                    }

                ]
            },

            options: {
                responsive: true
            }
        }
    );
}


// --------------------------------
// START DASHBOARD
// --------------------------------

loadDashboard();

loadRecommendations();

createChart();