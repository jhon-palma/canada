/* ------------------------------------------------------------------------------
 *
 *  # Echarts - pies and donuts
 *
 *  Pies and donuts chart configurations
 *
 *  Version: 1.0
 *  Latest update: August 1, 2015
 *
 * ---------------------------------------------------------------------------- */

$(function () {

    // Set paths
    // ------------------------------

    require.config({
        paths: {
            echarts: 'app/js/plugins/visualization/echarts'
        }
    });


    // Configuration
    // ------------------------------

    require(
        [
            'echarts',
            'echarts/theme/limitless',
            'echarts/chart/pie',
            'echarts/chart/bar',
            'echarts/chart/funnel'
        ],


        // Charts setup
        function (ec, limitless) {


            // Initialize charts
            // ------------------------------

            
            var stacked_clustered_bars = ec.init(document.getElementById('stacked_clustered_bars'), limitless);
            var multiple_donuts = ec.init(document.getElementById('multiple_donuts'), limitless);
            var thermometer_columns = ec.init(document.getElementById('thermometer_columns'), limitless);
            var thermometer_columns_2 = ec.init(document.getElementById('thermometer_columns_2'), limitless);
            var thermometer_columns_3 = ec.init(document.getElementById('thermometer_columns_3'), limitless);
            var basic_pie = ec.init(document.getElementById('basic_pie'), limitless);
            var basic_pie_2 = ec.init(document.getElementById('basic_pie_2'), limitless);


            // Charts setup
            // ------------------------------                    

            //
            // Basic pie options
            //

            

            //
            // Multiple donuts options
            //

            // Top text label
            var labelTop = {
                normal: {
                    label: {
                        show: true,
                        position: 'center',
                        formatter: '{b}\n',
                        textStyle: {
                            baseline: 'middle',
                            fontWeight: 300,
                            fontSize: 12
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    
                }
            };

            // Format bottom label
            var labelFromatter = {
                normal: {
                    label: {
                        formatter: function (params) {
                            return '\n\n' + '$' + (params.value - 4000)
                        }

                    }
                }
            }

            // Bottom text label
            var labelBottom = {
                normal: {
                    color: '#eee',
                    label: {
                        show: true,
                        position: 'center',
                        textStyle: {
                            baseline: 'middle'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    
                },
                emphasis: {
                    color: 'rgba(0,0,0,0)'
                }
            };

            // Set inner and outer radius
            var radius = [50, 57];

            // Add options
            multiple_donuts_options = {

                // Add title
                // title: {
                //     text: ' 22 Enero 2020 a las 3:44 p.m.',
                //     subtext: 'from global web index',
                //     x: 'center'
                // },

                // Add legend
                legend: {
                    x: 'center',
                    y: '50%',
                    show: false,
                    data: ['Ingreso Anual \n Necesario', 'Ingreso Mensual \n Necesario', 'Ingreso Semanal\nNecesario', 'Volumen Ventas\nMensuales']
                },

                tooltip: {
                    trigger: 'item',
                    formatter: "$ {c} "
                },

                // Add series
                series: [
                    {
                        type: 'pie',
                        center: ['10%', '50.5%'],
                        radius: radius,
                        itemStyle: labelFromatter,
                        data: [
                            {name: 'other', value: 2000, itemStyle: labelBottom},
                            {name: 'Ingreso Anual \n Necesario', value: 100,itemStyle: labelTop}
                        ]
                    },
                    {
                        type: 'pie',
                        center: ['36%', '50.5%'],
                        radius: radius,
                        color: 'red',
                        itemStyle: labelFromatter,
                        data: [
                            {name: 'other', value: 34343, itemStyle: labelBottom},
                            {name: 'Ingreso Mensual \n Necesario', value: 10330 ,itemStyle: labelTop}
                        ]
                    },
                    {
                        type: 'pie',
                        center: ['63%', '50.5%'],
                        radius: radius,
                        itemStyle: labelFromatter,
                        data: [
                            {name: 'other', value: 65, itemStyle: labelBottom},
                            {name: 'Ingreso Semanal\nNecesario', value: 35,itemStyle: labelTop}
                        ]
                    },
                    {
                        type: 'pie',
                        center: ['90%', '50.5%'],
                        radius: radius,
                        itemStyle: labelFromatter,
                        data: [
                            {name: 'other', value: 70, itemStyle: labelBottom},
                            {name: 'Volumen Ventas\nMensuales', value: 30,itemStyle: labelTop}
                        ]
                    },
                    // {
                    //     type: 'pie',
                    //     center: ['90%', '32.5%'],
                    //     radius: radius,
                    //     itemStyle: labelFromatter,
                    //     data: [
                    //         {name:'other', value:73, itemStyle: labelBottom},
                    //         {name:'Weixin', value:27,itemStyle: labelTop}
                    //     ]
                    // },
                    // {
                    //     type: 'pie',
                    //     center: ['10%', '82.5%'],
                    //     radius: radius,
                    //     itemStyle: labelFromatter,
                    //     data: [
                    //         {name: 'other', value: 78, itemStyle: labelBottom},
                    //         {name: 'Twitter', value: 22,itemStyle: labelTop}
                    //     ]
                    // },
                    // {
                    //     type: 'pie',
                    //     center: ['30%', '82.5%'],
                    //     radius: radius,
                    //     itemStyle: labelFromatter,
                    //     data: [
                    //         {name: 'other', value: 78, itemStyle: labelBottom},
                    //         {name: 'Skype', value: 22,itemStyle: labelTop}
                    //     ]
                    // },
                    // {
                    //     type: 'pie',
                    //     center: ['50%', '82.5%'],
                    //     radius: radius,
                    //     itemStyle: labelFromatter,
                    //     data: [
                    //         {name: 'other', value: 78, itemStyle: labelBottom},
                    //         {name: 'Messenger', value: 22,itemStyle: labelTop}
                    //     ]
                    // },
                    // {
                    //     type: 'pie',
                    //     center: ['70%', '82.5%'],
                    //     radius: radius,
                    //     itemStyle: labelFromatter,
                    //     data: [
                    //         {name: 'other', value: 83, itemStyle: labelBottom},
                    //         {name: 'Whatsapp', value: 17,itemStyle: labelTop}
                    //     ]
                    // },
                    // {
                    //     type: 'pie',
                    //     center: ['90%', '82.5%'],
                    //     radius: radius,
                    //     itemStyle: labelFromatter,
                    //     data: [
                    //         {name:'other', value:89, itemStyle: labelBottom},
                    //         {name:'Instagram', value:11,itemStyle: labelTop}
                    //     ]
                    // }
                ]
            };


            stacked_clustered_bars_options = {

                // Setup grid
                grid: {
                    x: 45,
                    x2: 45,
                    y: 45,
                    y2: 25
                },

                // Add tooltip
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: "{b}: $ {c} "
                },
                

                // Add legends
                legend: {
                    data: [
                        'Gastos Mensuales','Meta Vivienda','Meta Vehiculo','Meta Vacaciones',
                        // 'Version 2.0 - 2k data','Version 2.0 - 2w data','Version 2.0 - 20w data','Version 2.0 - 202w data'
                    ]
                },

                // Enable drag recalculate
                calculable: true,

                // Vertical axis
                yAxis: [
                    {
                        type: 'category',
                        data: ['Meta']
                    },
                    {
                        type: 'category',
                        axisLine: {show: false},
                        axisTick: {show: false},
                        axisLabel: {show: false},
                        splitArea: {show: false},
                        splitLine: {show: false},
                        data: ['Ingreso']
                    }
                ],

                // Horizontal axis
                xAxis: [{
                    type: 'value',
                    axisLabel: {formatter: '$ {value}'}
                }],

                // Add series
                series: [

                    
                    {
                        name: 'Version 2.0 - 2k data',
                        type: 'bar',
                        yAxisIndex: 1,
                        itemStyle: {
                            normal: {
                                color: '#F44336',
                                label: {
                                    show: true,
                                    textStyle:{
                                        color: '#fff'
                                    }
                                }
                            },
                            emphasis: {
                                color: '#F44336',
                                label: {
                                    show: true,

                                }
                            }
                        },
                        data: [247],
                    },
                    {
                        name: 'Version 2.0 - 2w data',
                        type: 'bar',
                        yAxisIndex: 1,
                        itemStyle: {
                            normal: {
                                color: '#4CAF50',
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            },
                            emphasis: {
                                color: '#4CAF50',
                                label: {
                                    show: true
                                }
                            }
                        },
                        data: [488]
                    },
                    {
                        name: 'Version 2.0 - 20w data',
                        type: 'bar',
                        yAxisIndex: 1,
                        itemStyle: {
                            normal: {
                                color: '#2196F3',
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            },
                            emphasis: {
                                color: '#2196F3',
                                label: {
                                    show: true
                                }
                            }
                        },
                        data: [906]
                    },

                    
        
                    {
                        name: 'Version 2.0 - 202w data',
                        type: 'bar',
                        yAxisIndex: 1,
                        itemStyle: {
                            normal: {
                                color: '#00c5c9',
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            },
                            emphasis: {
                                color: '#00c5c9',
                                label: {
                                    show: true
                                }
                            }
                        },
                        data: [2000]
                    },
                   
                
                    {
                        name: 'Gastos Mensuales',
                        type: 'bar',
                        itemStyle: {
                            normal: {
                                color: '#E57373',
                                label: {
                                    show: true
                                }
                            },
                            emphasis: {
                                color: '#E57373',
                                label: {
                                    show: true
                                }
                            }
                        },
                        data: [680]
                    },
                    {
                        name: 'Meta Vivienda',
                        type: 'bar',
                        itemStyle: {
                            normal: {
                                color: '#81C784',
                                label: {
                                    show: true
                                }
                            },
                            emphasis: {
                                color: '#81C784',
                                label: {
                                    show: true
                                }
                            }
                        },
                        data: [1212]
                    },
                    {
                        name: 'Meta Vehiculo',
                        type: 'bar',
                        itemStyle: {
                            normal: {
                                color: '#64B5F6',
                                label: {
                                    show: true,
                                    // formatter: function(p) {return p.value > 0 ? (p.value +'+'):'';}
                                }
                            },
                            emphasis: {
                                color: '#64B5F6',
                                label: {
                                    show: false
                                }
                            }
                        },
                        data: [3000]
                    },

                    
                     {
                        name: 'Meta Vacaciones',
                        type: 'bar',
                        itemStyle: {
                            normal: {
                                color: '#76e2e2',
                                label: {
                                    show: true,
                                    formatter: function(p) {return p.value > 0 ? (p.value +'+'):'';}
                                }
                            },
                            emphasis: {
                                color: '#76e2e2',
                                label: {
                                    show: false
                                }
                            }
                        },
                        data: [4000]
                    },
                   
                ]
            };


//
            // Thermometer options
            //

            thermometer_columns_options = {

                // Setup grid
                grid: {
                    x: 35,
                    x2: 10,
                    y: 35,
                    y2: 25
                },

                // Add tooltip
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow' // 'line' | 'shadow'
                    },
                    formatter: function (params) {
                        return params[0].name + '<br/>'
                        + params[0].seriesName + ': ' + params[0].value + '<br/>'
                        + params[1].seriesName + ': ' + (params[1].value + params[0].value);
                    }
                },

                // Add legend
                legend: {
                    selectedMode: false,
                    data: ['Actual', 'Forecast'],
                    show: false,
                },

                // Enable drag recalculate
                calculable: true,

                // Horizontal axis
                xAxis: [{
                    type: 'category',
                    data: ['Anual', 'Mensual', 'Semanal', 'Ventas']
                }],

                // Vertical axis
                yAxis: [{
                    type: 'value',
                    boundaryGap: [0, 0.1]
                }],

                // Add series
                series: [
                    {
                        name: 'Actual',
                        type: 'bar',
                        stack: 'sum',
                        barCategoryGap: '50%',
                        itemStyle: {
                            normal: {
                                color: '#003DA5',
                                barBorderColor: '#003DA5',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    position: 'insideTop'
                                }
                            },
                            emphasis: {
                                color: '#0C56C1',
                                barBorderColor: '#0C56C1',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            }
                        },
                        data: [500, 200, 220, 120]
                    },
                    {
                        name: 'Forecast',
                        type: 'bar',
                        stack: 'sum',
                        itemStyle: {
                            normal: {
                                color: '#DC1C2E',
                                barBorderColor: '#DC1C2E',
                                barBorderWidth: 6,
                                barBorderRadius: 0,
                                label: {
                                    show: true, 
                                    position: 'top',
                                    // formatter: function (params) {
                                    //     for (var i = 0, l = thermometer_columns_options.xAxis[0].data.length; i < l; i++) {
                                    //         if (thermometer_columns_options.xAxis[0].data[i] == params.name) {
                                    //             return thermometer_columns_options.series[0].data[i] + params.value;
                                    //         }
                                    //     }
                                    // },
                                    textStyle: {
                                        color: '#DC1C2E'
                                    }
                                }
                            },
                            emphasis: {
                                barBorderColor: '#EF4D61',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#EF4D61'
                                    }
                                }
                            }
                        },
                        data:[50, 80, 100, 80]
                    }
                ]
            };

// Thermometer options
            //

            thermometer_columns_2_options = {

                // Setup grid
                grid: {
                    x: 35,
                    x2: 15,
                    y: 15,
                    y2:75
                },

                // Add tooltip
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow' // 'line' | 'shadow'
                    },
                    formatter: function (params) {
                        return params[0].name + '<br/>'
                        + params[0].seriesName + ': ' + params[0].value + '<br/>'
                        + params[1].seriesName + ': ' + (params[1].value + params[0].value);
                    }
                },

                // Add legend
                legend: {
                    selectedMode: false,
                    data: ['Actual', 'Forecast'],
                    show: false,
                },

                // Enable drag recalculate
                calculable: true,

                // Horizontal axis
                xAxis: [{
                    type: 'category',
                    data: ['Anual', 'Mensual', 'Semanal', 'Ventas']
                }],

                // Vertical axis
                yAxis: [{
                    type: 'value',
                    boundaryGap: [0, 0.1]
                }],

                // Add series
                series: [
                    {
                        name: 'Actual',
                        type: 'bar',
                        stack: 'sum',
                        barCategoryGap: '50%',
                        itemStyle: {
                            normal: {
                                color: '#003DA5',
                                barBorderColor: '#003DA5',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    position: 'insideTop'
                                }
                            },
                            emphasis: {
                                color: '#0C56C1',
                                barBorderColor: '#0C56C1',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            }
                        },
                        data: [500, 200, 220, 120]
                    },
                    {
                        name: 'Forecast',
                        type: 'bar',
                        stack: 'sum',
                        itemStyle: {
                            normal: {
                                color: '#DC1C2E',
                                barBorderColor: '#DC1C2E',
                                barBorderWidth: 6,
                                barBorderRadius: 0,
                                label: {
                                    show: true, 
                                    position: 'top',
                                    // formatter: function (params) {
                                    //     for (var i = 0, l = thermometer_columns_options.xAxis[0].data.length; i < l; i++) {
                                    //         if (thermometer_columns_options.xAxis[0].data[i] == params.name) {
                                    //             return thermometer_columns_options.series[0].data[i] + params.value;
                                    //         }
                                    //     }
                                    // },
                                    textStyle: {
                                        color: '#DC1C2E'
                                    }
                                }
                            },
                            emphasis: {
                                barBorderColor: '#EF4D61',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#EF4D61'
                                    }
                                }
                            }
                        },
                        data:[50, 80, 100, 80]
                    }
                ]
            };


// Thermometer options
            //

            thermometer_columns_3_options = {

                // Setup grid
                grid: {
                    x: 35,
                    x2: 15,
                    y: 15,
                    y2:75
                },

                // Add tooltip
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow' // 'line' | 'shadow'
                    },
                    formatter: function (params) {
                        return params[0].name + '<br/>'
                        + params[0].seriesName + ': ' + params[0].value + '<br/>'
                        + params[1].seriesName + ': ' + (params[1].value + params[0].value);
                    }
                },

                // Add legend
                legend: {
                    selectedMode: false,
                    data: ['Actual', 'Forecast'],
                    show: false,
                },

                // Enable drag recalculate
                calculable: true,

                // Horizontal axis
                xAxis: [{
                    type: 'category',
                    data: ['Anual', 'Mensual', 'Semanal', 'Ventas']
                }],

                // Vertical axis
                yAxis: [{
                    type: 'value',
                    boundaryGap: [0, 0.1]
                }],

                // Add series
                series: [
                    {
                        name: 'Actual',
                        type: 'bar',
                        stack: 'sum',
                        barCategoryGap: '50%',
                        itemStyle: {
                            normal: {
                                color: '#003DA5',
                                barBorderColor: '#003DA5',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    position: 'insideTop'
                                }
                            },
                            emphasis: {
                                color: '#0C56C1',
                                barBorderColor: '#0C56C1',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            }
                        },
                        data: [500, 200, 220, 120]
                    },
                    {
                        name: 'Forecast',
                        type: 'bar',
                        stack: 'sum',
                        itemStyle: {
                            normal: {
                                color: '#DC1C2E',
                                barBorderColor: '#DC1C2E',
                                barBorderWidth: 6,
                                barBorderRadius: 0,
                                label: {
                                    show: true, 
                                    position: 'top',
                                    // formatter: function (params) {
                                    //     for (var i = 0, l = thermometer_columns_options.xAxis[0].data.length; i < l; i++) {
                                    //         if (thermometer_columns_options.xAxis[0].data[i] == params.name) {
                                    //             return thermometer_columns_options.series[0].data[i] + params.value;
                                    //         }
                                    //     }
                                    // },
                                    textStyle: {
                                        color: '#DC1C2E'
                                    }
                                }
                            },
                            emphasis: {
                                barBorderColor: '#EF4D61',
                                barBorderWidth: 6,
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#EF4D61'
                                    }
                                }
                            }
                        },
                        data:[50, 80, 100, 80]
                    }
                ]
            };


            //
            // Basic pie options
            //

            basic_pie_options = {

                // Add title
                title: {
                    // text: 'Browser popularity',
                    // subtext: 'Open source information',
                    x: 'center'
                },

                // Add tooltip
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                },

                // Add legend
                // legend: {
                //     orient: 'vertical',
                //     x: 'left',
                //     data: ['Tasaciones', 'Propiedades Subidas']
                // },

                // // Display toolbox
                // toolbox: {
                //     show: true,
                //     orient: 'vertical',
                //     feature: {
                //         mark: {
                //             show: true,
                //             title: {
                //                 mark: 'Markline switch',
                //                 markUndo: 'Undo markline',
                //                 markClear: 'Clear markline'
                //             }
                //         },
                //         dataView: {
                //             show: true,
                //             readOnly: false,
                //             title: 'View data',
                //             lang: ['View chart data', 'Close', 'Update']
                //         },
                //         magicType: {
                //             show: true,
                //             title: {
                //                 pie: 'Switch to pies',
                //                 funnel: 'Switch to funnel',
                //             },
                //             type: ['pie', 'funnel'],
                //             option: {
                //                 funnel: {
                //                     x: '25%',
                //                     y: '20%',
                //                     width: '50%',
                //                     height: '70%',
                //                     funnelAlign: 'left',
                //                     max: 1548
                //                 }
                //             }
                //         },
                //         restore: {
                //             show: true,
                //             title: 'Restore'
                //         },
                //         saveAsImage: {
                //             show: true,
                //             title: 'Same as image',
                //             lang: ['Save']
                //         }
                //     }
                // },

                // Enable drag recalculate
                calculable: true,

                // Add series
                series: [{
                    name: 'Browsers',
                    type: 'pie',
                    radius: '50%',
                    center: ['50%', '40.5%'],
                    data: [
                        {value: 4, name: 'Tasaciones'},
                        {value: 1, name: 'Propiedades Subidas'}
                    ]
                }]
            };


            basic_pie_2_options = {

                // Add title
                title: {
                    // text: 'Browser popularity',
                    // subtext: 'Open source information',
                    x: 'center'
                },

                // Add tooltip
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                },

                // Add legend
                // legend: {
                //     orient: 'vertical',
                //     x: 'left',
                //     data: ['Tasaciones', 'Propiedades Subidas']
                // },

                // // Display toolbox
                // toolbox: {
                //     show: true,
                //     orient: 'vertical',
                //     feature: {
                //         mark: {
                //             show: true,
                //             title: {
                //                 mark: 'Markline switch',
                //                 markUndo: 'Undo markline',
                //                 markClear: 'Clear markline'
                //             }
                //         },
                //         dataView: {
                //             show: true,
                //             readOnly: false,
                //             title: 'View data',
                //             lang: ['View chart data', 'Close', 'Update']
                //         },
                //         magicType: {
                //             show: true,
                //             title: {
                //                 pie: 'Switch to pies',
                //                 funnel: 'Switch to funnel',
                //             },
                //             type: ['pie', 'funnel'],
                //             option: {
                //                 funnel: {
                //                     x: '25%',
                //                     y: '20%',
                //                     width: '50%',
                //                     height: '70%',
                //                     funnelAlign: 'left',
                //                     max: 1548
                //                 }
                //             }
                //         },
                //         restore: {
                //             show: true,
                //             title: 'Restore'
                //         },
                //         saveAsImage: {
                //             show: true,
                //             title: 'Same as image',
                //             lang: ['Save']
                //         }
                //     }
                // },

                // Enable drag recalculate
                calculable: true,

                // Add series
                series: [{
                    name: 'Browsers',
                    type: 'pie',
                    radius: '50%',
                    center: ['50%', '40.5%'],
                    data: [
                        {value: 4, name: 'Tasaciones'},
                        {value: 1, name: 'Entradas Rápidas'}
                    ]
                }]
            };



            // Apply options
            // ------------------------------

            
            stacked_clustered_bars.setOption(stacked_clustered_bars_options);
            multiple_donuts.setOption(multiple_donuts_options);
            thermometer_columns.setOption(thermometer_columns_options);
            thermometer_columns_2.setOption(thermometer_columns_2_options);
            thermometer_columns_3.setOption(thermometer_columns_3_options);
            basic_pie.setOption(basic_pie_options);
            basic_pie_2.setOption(basic_pie_2_options);



            // Resize charts
            // ------------------------------

            window.onresize = function () {
                setTimeout(function (){
                    
                    multiple_donuts.resize();
                    stacked_clustered_bars.resize();
                    thermometer_columns.resize();
                    thermometer_columns_2.resize();
                    thermometer_columns_3.resize();
                    basic_pie.resize();
                    basic_pie_2.resize();
                }, 200);
            }
        }
    );
});
