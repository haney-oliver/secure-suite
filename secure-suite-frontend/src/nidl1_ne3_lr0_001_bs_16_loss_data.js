export const nidl1_ne3_lr0_001_bs_16_loss_data = {
    type: 'line',
    data: {
        labels: [1, 2, 3],
        datasets: [
            {
                label: 'Train',
                data: [0.469, 0.445, 0.261],
                backgroundColor: [
                    'rgba(188, 245, 255,0.5)'
                ],
                borderColor: [
                    '#2dabce'
                ],
                borderWidth: 3
            },
            {
                label: 'Validate',
                data: [0.473, 0.367, 0.051],
                backgroundColor: [
                    'rgba(147, 194, 255,0.5)',
                ],
                borderColor: [
                    '#2985FF',
                ],
                borderWidth: 3
            }
        ]
    },
    options: {
        responsive: true,
        lineTension: 1,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: false,
                    padding: 20
                }
            }]
        }
    }
}

export default nidl1_ne3_lr0_001_bs_16_loss_data
