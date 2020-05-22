export const nidl1_ne6_lr0_005_bs_32_acc_data = {
    type: 'line',
    data: {
        labels: [0, 1, 2, 3, 4, 5],
        datasets: [
            {
                label: 'Train',
                data: [0.826, 0.936, 0.975, 0.984, 0.992, 0.994],
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
                data: [0.822, 0.977, 0.979, 0.963, 0.974, 0.971],
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

export default nidl1_ne6_lr0_005_bs_32_acc_data
