(function () {
    var allData=[];
    var len = 0;
    var pageNum = 1;
    var perNum = 8;
    //请求分类信息
    $(".category").on("click",function(){
        var drugId = $(this).attr("data-id");
        var drugName = $(this).text();
        var data ={
            drugId:drugId,
            drugName:drugName
        }
        allData=[];
        len = 0;
        pageNum = 1;
        perNum = 8;
        $.ajax({
            type:'get',
            url:'/requestClass',
            data:data,
            headers:{"Content-Type":"application/json"},
            dataType:'json',
            success:function(ret){
                allData=ret.elements.content;
                len = allData.length;
                console.log(ret);
                var li="";
                $.each(allData.slice(0,pageNum*perNum),function (i,val) {
                    li+='<li>' +
                        '<div class="drug-item" data-id="' + val.drugId + '">';
                    if(val.img == "无"||val.img.indexOf("nopic")>-1){
                        li+='<img class="drug-item-img" src="../static/images/drugItem.jpg" alt="">';
                    }else {
                        li+='<img class="drug-item-img" src="'+val.img+'" alt="">';
                    }
                    li+='<div class="drug-item-name">' + val.drugName + '</div>' +
                        '</div>' +
                        '</li>'
                })
                $(".drug-list").html(li);
                if(len >= pageNum*perNum){
                    $(".load-more").show();
                }
            }
        })
    })
    //加载更多
    $(".load-more").on('click',function () {
        var li="";
        $.each(allData.slice(pageNum*perNum,(pageNum+1)*perNum),function (i,val) {
            li+='<li>' +
                '<div class="drug-item" data-id="' + val.drugId + '">' +
                '<img class="drug-item-img" src="../static/images/drugItem.jpg" alt="">' +
                '<div class="drug-item-name">' + val.drugName + '</div>' +
                '</div>' +
                '</li>'
        })
        $(".drug-list").append(li);
        pageNum++;
        if(len >= pageNum*perNum){
            $(".load-more").show();
        }else {
            $(".load-more").hide();
        }
    })
    //关闭
    $(".close").on('click',function () {
        $(".detail-page").hide();
    })
    //点击详情
    $(document).on('click','.drug-item',function (e) {
        var curDrugId = $(this).attr("data-id");
        var curObj = {};
        for(var i=0;i<allData.length;i++){
            if(allData[i].drugId == curDrugId ){
                curObj = allData[i];
                break;
            }
        }
        $("#name").text(curObj.drugName);
        $("#othername").text(curObj.otherName);
        $("#newtime").text(curObj.newTime);
        $("#position").text(curObj.productionArea);
        $("#spec").text(curObj.characteristic);
        if(curObj.img!="无"){
            $("#myImg").attr('src',curObj.img);
        }
        $(".detail-page").show();
    })
})()