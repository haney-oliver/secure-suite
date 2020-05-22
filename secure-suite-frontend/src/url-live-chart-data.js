export const urlLiveChartData = {
    type: 'doughnut',
    data: {
        labels: ['Good URLs', 'Bad URLs'],
        datasets: [
            {
                data: [0, 0],
                backgroundColor: [
                    'rgb(71,218,255)',
                    'rgb(255,117,117)',
                ]
            }
        ]
    },
    options: {
        responsive: true
    }
}

export default urlLiveChartData
