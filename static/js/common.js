(function () {
    var userInfo = {
        userName:'123',
        date:'2019/11/15',
        operDrug:{
            '人参':13,
            '丹参':3
        },
        operProvince:{
            '北京':1,
            '南京':12
        }
    }
    localStorage.setItem('userInfo',userInfo);
})()