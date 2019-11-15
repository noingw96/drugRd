(function () {
    var data = [];
    var tipFloatFlag = false;
    $.ajax({
        type:'get',
        url:'/requestProvinceFloat',
        headers:{"Content-Type":"application/json"},
        dataType:'json',
        success:function(ret){
            data = ret.elements;
            console.log(ret);
            initEcharts("china", "中国");
            initColumnChart();
            initLineChart();
        }
    })
    var myChart = echarts.init(document.getElementById('china-map'));
    var columnChart = echarts.init(document.getElementById('columnEcharts'));
    var lineChart = echarts.init(document.getElementById('lineEcharts'));
    var oBack = document.getElementById("back");
    var provinces = ['shanghai', 'hebei', 'shanxi', 'neimenggu', 'liaoning', 'jilin', 'heilongjiang', 'jiangsu', 'zhejiang', 'anhui', 'fujian', 'jiangxi', 'shandong', 'henan', 'hubei', 'hunan', 'guangdong', 'guangxi', 'hainan', 'sichuan', 'guizhou', 'yunnan', 'xizang', 'shanxi1', 'gansu', 'qinghai', 'ningxia', 'xinjiang', 'beijing', 'tianjin', 'chongqing', 'xianggang', 'aomen'];
    var provincesText = ['上海', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '北京', '天津', '重庆', '香港', '澳门'];
    var seriesData = [{
        name: '北京',
        value: 100
    }, {
        name: '天津',
        value: 0
    }, {
        name: '上海',
        value: 60
    }, {
        name: '重庆',
        value: 0
    }, {
        name: '河北',
        value: 60
    }, {
        name: '河南',
        value: 60
    }, {
        name: '云南',
        value: 0
    }, {
        name: '辽宁',
        value: 0
    }, {
        name: '黑龙江',
        value: 0
    }, {
        name: '湖南',
        value: 60
    }, {
        name: '安徽',
        value: 0
    }, {
        name: '山东',
        value: 60
    }, {
        name: '新疆',
        value: 0
    }, {
        name: '江苏',
        value: 0
    }, {
        name: '浙江',
        value: 0
    }, {
        name: '江西',
        value: 0
    }, {
        name: '湖北',
        value: 60
    }, {
        name: '广西',
        value: 60
    }, {
        name: '甘肃',
        value: 0
    }, {
        name: '山西',
        value: 60
    }, {
        name: '内蒙古',
        value: 0
    }, {
        name: '陕西',
        value: 0
    }, {
        name: '吉林',
        value: 0
    }, {
        name: '福建',
        value: 0
    }, {
        name: '贵州',
        value: 0
    }, {
        name: '广东',
        value: 597
    }, {
        name: '青海',
        value: 0
    }, {
        name: '西藏',
        value: 0
    }, {
        name: '四川',
        value: 60
    }, {
        name: '宁夏',
        value: 0
    }, {
        name: '海南',
        value: [10,12]
    }, {
        name: '台湾',
        value: 0
    }, {
        name: '香港',
        value: 0
    }, {
        name: '澳门',
        value: 0
    }];

    oBack.onclick = function () {
        $(".map").css('overflow','hidden');
        initEcharts("china", "中国");
    };
    function debounce(fn,wait) {
        var timer = null;
        return function () {
            if(timer){
                console.log('清除')
                clearTimeout(timer);
            }else {
                console.log('生成')
                timer = setTimeout(fn,wait);
            }
        }
    }
    var backData;
    // 初始化echarts
    function initEcharts(pName, Chinese_) {
        var tmpSeriesData = pName === "china" ? seriesData : [];
        var option = {
            title: {
                text: Chinese_ || pName,
                left: 'center'
            },
            tooltip: {
                show:true,
                trigger: 'item',
//                formatter: '{b}<br/>{c} (p / km2)'
                formatter:function (params) {
                    $(".first-p").text(params.name+'-常见药材');
                    $(".second-p").text(data[params.name]);
                },
            },
            series: [
                {
                    name: Chinese_ || pName,
                    type: 'map',
                    mapType: pName,
                    roam: false,//是否开启鼠标缩放和平移漫游
                    data: tmpSeriesData,
                    top: "3%",//组件距离容器的距离
                    zoom:1.1,
                    selectedMode : 'single',

                    label: {
                        normal: {
                            show: true,//显示省份标签
                            textStyle:{color:"#fbfdfe"}//省份标签字体颜色
                        },
                        emphasis: {//对应的鼠标悬浮效果
                            show: true,
                            textStyle:{color:"#323232"}
                        }
                    },
                    itemStyle: {
                        normal: {
                            borderWidth: .5,//区域边框宽度
                            borderColor: '#0550c3',//区域边框颜色
                            areaColor:"#4ea397",//区域颜色

                        },

                        emphasis: {
                            borderWidth: .5,
                            borderColor: '#4b0082',
                            areaColor:"#ece39e",
                        }
                    },
                }
            ]

        };
        myChart.setOption(option);
        myChart.off("click");
        if (pName === "china") { // 全国时，添加click 进入省级
            myChart.on('click', function (param) {
                var qiwenData,jiangshuiData;
                var data = {
                    province:param.name
                }
                $.ajax({
                    type:'get',
                    url:'/ProvinceClassNum',
                    data:data,
                    headers:{"Content-Type":"application/json"},
                    dataType:'json',
                    success:function (ret) {
                        backData=ret.elements;
                        var newDataAxis=[],newData=[];
                        for (var key in backData.content){
                            newDataAxis.push(key);
                            newData.push(backData.content[key]);
                        }
                        columnChart.setOption({
                            tooltip:{
                                formatter:function(params){
                                    var myIndex = params.dataIndex;
                                    return newData[myIndex];
                                }
                            },
                            title: {
                                text: backData.province + '药材分类情况'
                            },
                            xAxis:{
                                data:newDataAxis
                            },
                            series: [
                                {
                                    type: 'bar',
                                    itemStyle: {
                                        normal: {
                                            color: new echarts.graphic.LinearGradient(
                                                0, 0, 0, 1,
                                                [
                                                    {offset: 0, color: '#83bff6'},
                                                    {offset: 0.5, color: '#188df0'},
                                                    {offset: 1, color: '#188df0'}
                                                ]
                                            ),
                                        },
                                        emphasis: {
                                            color: new echarts.graphic.LinearGradient(
                                                0, 0, 0, 1,
                                                [
                                                    {offset: 0, color: '#2378f7'},
                                                    {offset: 0.7, color: '#2378f7'},
                                                    {offset: 1, color: '#83bff6'}
                                                ]
                                            )
                                        }
                                    },
                                    data: newData
                                }
                            ]
                        })
//                        console.log(newData);
//                        console.log(newDataAxis)
                    }
                })
                //获得气温降水数据
                for(var provinceIndex=0;provinceIndex<qiwen.length;provinceIndex++){
                    if(qiwen[provinceIndex]['NAME'].indexOf(param.name)>-1){
                        qiwenData = qiwen[provinceIndex];
                        break;
                    }
                }
                for(var provinceIndex=0;provinceIndex<jiangshui.length;provinceIndex++){
                    if(jiangshui[provinceIndex]['NAME'].indexOf(param.name)>-1){
                        jiangshuiData = jiangshui[provinceIndex];
                        break;
                    }
                }
                qiwenData = objFormat(qiwenData);
                jiangshuiData = objFormat(jiangshuiData);
                lineChart.setOption({
                    title: {
                        text: param.name + '月均气温/降水量情况'
                    },
                    series: [{
                        data: jiangshuiData,
                        type: 'bar',
                        itemStyle:{
                            normal:{
                                color:"#f40d0d"
                            }
                        }
                    },{
                        data:qiwenData,
                        yAxisIndex: 1,
                        type:'line',
                        itemStyle:{
                            normal:{
                                color:"#46f41a"
                            }
                        }
                    }]
                })
                console.log(qiwenData,jiangshuiData)
            });
            myChart.on('dblclick', function (param) {
//                console.log(param.name);
                // 遍历取到provincesText 中的下标  去拿到对应的省js
                for (var i = 0; i < provincesText.length; i++) {
                    if (param.name === provincesText[i]) {
                        //显示对应省份的方法
                        $(".map").css('overflow','inherit');
                        showProvince(provinces[i], provincesText[i]);
                        break;
                    }
                }
                if (param.componentType === 'series') {
                    var provinceName =param.name;
                    $('#box').css('display','block');
                    $("#box-title").html(provinceName);
                }
            });
        } else { // 省份，添加双击 回退到全国
            myChart.on("dblclick", function () {
                initEcharts("china", "中国");
            });
        }
    }
    function objFormat(obj) {
        var arr=[];
        for(var key in obj){
            if(key.indexOf('MEAN')>-1){
                arr.push(obj[key]);
            }
        }
        return arr;
    }
    function initLineChart() {
        var optionLineChart = {
            tooltip:{
                show:true,
                formatter:function(params){
                    return params.name+'月:\n'+params.value;
                }
            },
            title: {
                text: '北京月均气温/降水量情况',
                x:'center',
                textStyle: {
                    color: '#fff',
                    fontSize:16
                },
                y:'0px',
            },
            xAxis: {
                type: 'category',
                data: ['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12'],
                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    }
                }
            },
            yAxis: [
                {
                    type:'value',
                    name:'降水量/mm',
                    show:true,
                    axisLabel: {
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    nameTextStyle:{
                        color: '#fff',
                    }

                },
                {
                    type:'value',
                    name:'温度/℃',
                    show:true,
                    interval:10,
                    min:-10,
                    max:40,
                    axisLabel: {
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    nameTextStyle:{
                        color: '#fff',
                    }
                }
            ],
            series: [{
                data: [820, 932, 901, 934, 1290, 1330, 1320,820, 932, 901, 934, 1290],
                type: 'bar',
                itemStyle:{
                    normal:{
                        color:"#f40d0d"
                    }
                }
            },{
                data:[12,19,21,25,19,24,15,12,19,21,25,19],
                yAxisIndex: 1,
                type:'line',
                itemStyle:{
                    normal:{
                        color:"#46f41a"
                    }
                }
            }]
        };
        lineChart.setOption(optionLineChart)
    }
    function initColumnChart() {
        var dataAxis = ["全草类", "加工类", "动物类", "叶类", "果实籽仁类", "根茎类", "花类", "菌藻类"];
//        var data = [60, 20, 26, 17, 7, 110, 65, 11];
        var data = [0,0,0,0,0,0,0,0];
        var yMax = 100;
        var dataShadow = [];
        for (var i = 0; i < data.length; i++) {
            dataShadow.push(yMax);
        }
        var optionColumnChart = {
            //显示悬浮提示
            tooltip:{
                formatter:function(params){
                    var myIndex = params.dataIndex;
                    return data[myIndex];
                }
            },
            title: {
                text: '北京药材分类情况',
                x:'center',
                textStyle: {
                    color: '#fff',
                    fontSize:16
                },
                y:'20px',
//                subtext: 'Feature Sample: Gradient Color, Shadow, Click Zoom'
            },
            xAxis: {
                data: dataAxis,
                axisLabel: {
                    inside: true,
                    textStyle: {
                        color: '#fff'
                    },
                    formatter:function(value){
                        return value.split("").join('\n');
                    }
                },
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                z: 10
            },
            yAxis: {
                type:'value',
                name:'种类数目',
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    }
                },
                nameTextStyle:{
                    color: '#fff',
                }
            },
            dataZoom: [
                {
                    type: 'inside'
                }
            ],
            series: [
                { // For shadow
                    type: 'bar',
                    itemStyle: {
                        normal: {
                            color: 'rgba(0,0,0,0.05)',
                        }
                    },
                    barGap:'-100%',
                    barCategoryGap:'40%',
                    data: dataShadow,
                    animation: false
                },
                {
                    type: 'bar',
                    itemStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(
                                0, 0, 0, 1,
                                [
                                    {offset: 0, color: '#83bff6'},
                                    {offset: 0.5, color: '#188df0'},
                                    {offset: 1, color: '#188df0'}
                                ]
                            ),
                        },
                        emphasis: {
                            color: new echarts.graphic.LinearGradient(
                                0, 0, 0, 1,
                                [
                                    {offset: 0, color: '#2378f7'},
                                    {offset: 0.7, color: '#2378f7'},
                                    {offset: 1, color: '#83bff6'}
                                ]
                            )
                        }
                    },
                    data: data
                }
            ]
        };

        // Enable data zoom when user click bar.
        var zoomSize = 6;
        columnChart.on('click', function (params) {
            console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
            columnChart.dispatchAction({
                type: 'dataZoom',
                startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                endValue: dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
            });
        });
        columnChart.setOption(optionColumnChart);
    }

    // 展示对应的省
    function showProvince(pName, Chinese_) {
        //这写省份的js都是通过在线构建工具生成的，保存在本地，需要时加载使用即可，最好不要一开始全部直接引入。
        loadBdScript('$' + pName + 'JS', '../static/js/map/province/' + pName + '.js', function () {
            initEcharts(Chinese_);
        });
    }

    // 加载对应的JS
    function loadBdScript(scriptId, url, callback) {
        var script = document.createElement("script");
        script.type = "text/javascript";
        if (script.readyState) {  //IE
            script.onreadystatechange = function () {
                if (script.readyState === "loaded" || script.readyState === "complete") {
                    script.onreadystatechange = null;
                    callback();
                }
            };
        } else {  // Others
            script.onload = function () {
                callback();
            };
        }
        script.src = url;
        script.id = scriptId;
        document.getElementsByTagName("head")[0].appendChild(script);
    };
})()