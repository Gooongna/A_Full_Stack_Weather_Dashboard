function lineChart(date, data1, data2){
    var linechart = echarts.init(document.getElementById('line-chart'));
    var option = {
        color: [
            '#05386b', '#8ee4af'
        ],

        tooltip: {
            trigger: 'axis'
        },

        legend: {
            x: 400,
            y: 30,
            data: ['Temperature', 'Humidity']
        },

        toolbox: {
            show: true,
            feature: {
                magicType: {
                    show: true,
                    title: {
                        line: 'Line',
                        bar: 'Bar',
                        stack: 'Stack',
                    },
                    type: ['line', 'bar', 'stack']
                },
                restore: {
                    show: true,
                    title: "Restore"
                },
                saveAsImage: {
                    show: true,
                    title: "Save Image"
                }
            }
        },

        calculable: true,

        xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: date //['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        }],
        yAxis: [{
            type: 'value'
        }],

        series: [{
            name: 'Temperature',
            type: 'line',
            smooth: true,
            itemStyle: {
                normal: {
                    areaStyle: {
                        type: 'default'
                    }
                }
            },
            data: data1 //[10, 12, 21, 54, 260, 830, 710]
        }, {
            name: 'Humidity',
            type: 'line',
            smooth: true,
            itemStyle: {
                normal: {
                    areaStyle: {
                        type: 'default'
                    }
                }
            },
            data: data2 //[30, 182, 434, 791, 390, 30, 10]
        }],
    };

    linechart.setOption(option);
    window.onresize = function(){
        linechart.resize();
    };

}