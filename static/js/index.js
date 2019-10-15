(function () {
    $(".search").on("click",function(){
        var search = $(".input1").val();
        if(search==""){
            alert("请输入搜索内容！");
        }
        var data={
            content:search
        };
        $.ajax({
            type:'get',
            url:'/inforRd',
            data:data,
            headers:{"Content-Type":"application/json"},
            dataType:'json',
            success:function(ret){
                var inforList=ret.elements;
                console.log(ret);
                var li="";
                $.each(inforList,function (i,val) {
                    li+='<li>' +
                        ' <div class="infor-item">' +
                        '<div class="infor-title"><a href="'+val.url+'" target="_blank">【'+val.title+'】</a></div>' +
                        '<div class="infor-intro">'+val.intro+'</div>' +
                        '<div class="item-footer">' +
                        '<div class="time">发布时间：'+val.time+'</div>' +
                        '<div class="author">作者：'+val.author+'</div>' +
                        '<div class="keyword">品种：'+val.key+'</div>' +
                        '</div>' +
                        '</div>' +
                        '</li>'
                })
                $("#myInfor").html(li);
            }
        })
    })
})()