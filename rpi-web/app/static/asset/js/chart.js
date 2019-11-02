$(document).ready(function () {
    var charts = {};
    charts.myLightChart = echarts.init(document.getElementById('lightchart'));
    charts.myTmpChart = echarts.init(document.getElementById('tmpchart'));
    charts.myHmtChart = echarts.init(document.getElementById('hmtchart'));
    charts.myCo2Chart = echarts.init(document.getElementById('co2chart'));
    initCharts(charts);
    $('#singleDateRange').DatePicker({
        startDate: moment()
    });
    $('#show-button').click(function () {
        var selectdate = $('#singleDateRange').val().split('-').join('');
        getIoTData(selectdate, 1, function (data) {
        createTMPChart(charts,data);
        createHMTChart(charts,data);
        createCo2Chart(charts,data);
        createLightChart(charts,data);
        });
    });


});

function initCharts(charts){
    var todaytime = showLocale(new Date());
    getIoTData(todaytime, 1, function (data) {
        createTMPChart(charts,data);
        createHMTChart(charts,data);
        createCo2Chart(charts,data);
        createLightChart(charts,data);
    });
}

function getIoTData(todaytime, offset, callback) {
    var data = {};
    data.timedata = [];
    data.tmpdata = [];
    data.tmpdata = [];
    data.hmtdata = [];
    data.co2data = [];
    data.lxdata = [];
    $.getJSON('/api/v1/date/' + todaytime,
        function (rawData) {
            $.each(rawData,
                function (i, item) {
                    if (i % offset == 0) {
                        data.timedata.push(item['time']);
                        data.tmpdata.push(item['tmp']);
                        data.hmtdata.push(item['hmt']);
                        data.co2data.push(item['ppm']);
                        data.lxdata.push(item['lx']);
                    }
                });
            callback(data);
        });
}

function showLocale(objD) {
    var str, colorhead, colorfoot;
    var yy = objD.getYear();
    if (yy < 1900) yy = yy + 1900;
    var MM = objD.getMonth() + 1;
    if (MM < 10) MM = '0' + MM;
    var dd = objD.getDate();
    if (dd < 10) dd = '0' + dd;
    str = yy + "" + MM + "" + dd;
    console.log(str);
    return (str);
}

function createTMPChart(charts, data) {
    var option = {
        title: {
            text: 'Temperature(°C)',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ['line', 'bar']
                },
                restore: {},
                saveAsImage: {}
            }
        },

        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.timedata
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} °C'
            }
        },
        series: [{
            name: 'temperature',
            type: 'line',
            data: data.tmpdata,
             itemStyle: {
                normal: {
                    color: '#d68262'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#d68262'
                    }, {
                        offset: 1,
                        color: '#ffe'
                    }])
                }
            },
            markPoint: {
                data: [{
                    type: 'max',
                    name: 'Max Value'
                }, {
                    type: 'min',
                    name: 'Min Value'
                }]
            },
        }]
    };
    charts.myTmpChart.setOption(option);
}


function createHMTChart(charts, data) {
    var option = {
        title: {
            text: 'Humidity(%)',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ['line', 'bar']
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.timedata
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} %'
            }
        },
        series: [{
            name: 'humidity',
            type: 'line',
            data: data.hmtdata,
            itemStyle: {
                normal: {
                    color: '#5fc672'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#8ec6ad'
                    }, {
                        offset: 1,
                        color: '#ffe'
                    }])
                }
            },
            markPoint: {
                data: [{
                    type: 'max',
                    name: 'Max Value'
                }, {
                    type: 'min',
                    name: 'Min Value'
                }]
            },
        }]
    };
    charts.myHmtChart.setOption(option);
}

function createCo2Chart(charts, data) {
    option = {
        title: {
            text: 'Co2(ppm)',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['Co2 ppm', ]
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ['line', 'bar']
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.timedata
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} ppm'
            }
        },
        series: [{
            name: 'Co2',
            type: 'line',
            data: data.co2data,
            itemStyle: {
                normal: {
                    color: '#00a6d7'
                }
            },
             areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#00a6d7'
                    }, {
                        offset: 1,
                        color: '#ffe'
                    }])
                }
            },
            markPoint: {
                data: [{
                    type: 'max',
                    name: 'Max Value'
                }, {
                    type: 'min',
                    name: 'Min Value'
                }]
            },
        }]
    };
    charts.myCo2Chart.setOption(option);
}



function createLightChart(charts,data) {

    option = {
        title: {
            text: 'Light(lx)',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['Light lx', ]
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ['line', 'bar']
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.timedata
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} lx'
            }
        },
        series: [{
            name: 'Light Strength',
            type: 'line',
            data: data.lxdata,
            markPoint: {
                data: [{
                    type: 'max',
                    name: 'Max Value'
                }, {
                    type: 'min',
                    name: 'Min Value'
                }]
            },
        }, ]
    };
    charts.myLightChart.setOption(option);
}