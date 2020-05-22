export const nidl1_ne3_lr0_001_bs_16_acc_data = {
    type: 'line',
    data: {
        labels: [1, 2, 3],
        datasets: [
            {
                label: 'Train',
                data: [0.821, 0.844, 0.917],
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
                data: [0.813, 0.894, 0.979],
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

export default nidl1_ne3_lr0_001_bs_16_acc_data
