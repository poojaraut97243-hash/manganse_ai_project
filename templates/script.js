const productionCtx = document.getElementById('productionChart');

new Chart(productionCtx, {

    type: 'line',

    data: {

        labels: [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun'
        ],

        datasets: [

            {
                label: 'Actual Production',

                data: [
                    8200,
                    8700,
                    9100,
                    8800,
                    9500,
                    9700
                ],

                borderWidth: 3,

                tension: 0.4,

                fill: true
            },

            {
                label: 'Predicted Production',

                data: [
                    8500,
                    8900,
                    9200,
                    9400,
                    9800,
                    10200
                ],

                borderWidth: 3,

                borderDash: [8, 5],

                tension: 0.4
            }

        ]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

            legend: {

                position: 'bottom'

            }

        }

    }

});