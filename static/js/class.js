(function () {
    $(".category").on("click",function(){
        var drugId = $(this).attr("data-id");
        var drugName = $(this).text();
        var data ={
            drugId:drugId,
            drugName:drugName
        }
        var allData=[]
        $.ajax({
            type:'get',
            url:'/requestClass',
            data:data,
            headers:{"Content-Type":"application/json"},
            dataType:'json',
            success:function(ret){
                var allData=ret.elements.content;
                console.log(ret);
                var li="";
                $.each(allData.slice(0,8),function (i,val) {
                    li+='<li>' +
                        '<div class="drug-item" data-id="' + val.drugId + '">' +
                        '<img class="drug-item-img" src="../static/images/drugItem.jpg" alt="">' +
                        '<div class="drug-item-name">' + val.drugName + '</div>' +
                        '</div>' +
                        '</li>'
                })
                $(".drug-list").html(li);
            }
        })
    })
})()