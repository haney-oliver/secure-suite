export const nidl1_ne6_lr0_005_bs_32_loss_data= {
    type: 'line',
    data: {
        labels: [0, 1, 2, 3, 4, 5],
        datasets: [
            {
                label: 'Train',
                data: [0.379, 0.151, 0.034, 0.021, 0.019, 0.015],
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
                data: [0.391, 0.056, 0.055, 0.064, 0.051, 0.054],
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

export default nidl1_ne6_lr0_005_bs_32_loss_data
