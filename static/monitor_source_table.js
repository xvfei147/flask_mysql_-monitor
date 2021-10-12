
$(function () {
    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

    // 2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_departments').bootstrapTable({
            url: '/monitor/source/get_all',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            responseHandler: function(data){
                return data.rows;
            },
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: false,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: 'id'
            }, {
                field: 'name',
                align: 'center',
                title: '数据源名称'
            }, {
                field: 'host',
                align: 'center',
                title: '主机地址'
            }, {
                field: 'port',
                align: 'center',
                title: '端口'
            }, {
                field: 'username',
                align: 'center',
                title: '用户名'
            }/*, {
                field: 'password',
                align: 'center',
                title: '密码'
            }*/,  {
                field: 'database',
                align: 'center',
                title: '数据库'
            }]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            departmentname: $("#txt_search_departmentname").val(),
            statu: $("#txt_search_title").val()
        };
        return temp;
    };

    return oTableInit;
};
var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        $(".msg").hide();
        //初始化页面上面的按钮事件
        $("#btn_add").click(function(){
            $("#myModalLabel").text("新增");
            $("#name").val('');
            $("#host").val('');
            $("#port").val('');
            $("#username").val('');
            $("#password").val('');
            $("#database").val('');
            $("#id").val('');
            $("#myModal").modal()
        })
        $("#btn_delete").click(function () {
            var arrselect = $("#tb_departments").bootstrapTable('getSelections')
            if(arrselect.length<=0){
                alert("请选择要删除的行")
                return
            }
            if(arrselect.length>1){
                alert("仅可选中一行");
                return
            }
            var id = arrselect[0]['id']
            if(confirm("确定要删除选择的数据吗？")){
                $.ajax({
                    type:"get",
                    url:"/monitor/source/delete/"+ id,
                    success:function (data) {
                        if (data === 'success'){
                            alert("删除成功")
                            $("#tb_departments").bootstrapTable('refresh')
                        }
                    },error:function () {
                        alert("Error")
                    }
                })
            }
        });
        $("#btn_edit").click(function () {
            $(".msg").hide();
            var arrselect = $("#tb_departments").bootstrapTable('getSelections');
            if(arrselect.length<=0){
                alert("请选择要编辑的行");
                return
            }
            if(arrselect.length>1){
                alert("仅可选中一行");
                return
            }
            $("#myModalLabel").text("修改");
            $("#myModal").modal();
            var item = arrselect[0];
            $("#name").val(item['name']);
            $("#host").val(item['host']);
            $("#port").val(item['port']);
            $("#username").val(item['username']);
            $("#password").val(item['password']);
            $("#database").val(item['database']);
            $("#id").val(item['id']);

        });
        $("#conn_test").click(function () {
            $("#msg").html("");
            postdata.host = $("#host").val();
            postdata.port = $("#port").val();
            postdata.username = $("#username").val();
            postdata.password = $("#password").val();
            postdata.database = $("#database").val();
            // console.log(postdata);
            $.ajax({
                type:'post',
                url:'/monitor/source/test_conn',
                data: postdata,
                success:function (data) {
                    // console.log(data);
                    if(data ==="连接成功"){
                        $("#msg").css("color","green")
                    }else{
                        $("#msg").css("color","red")
                    }
                    $("#msg").html(data);
                    $(".msg").show();
                },error:function () {
                    alert("Error")
                }
            })
        });
        $("#btn_submit").click(function () {
            postdata.name = $("#name").val();
            postdata.host = $("#host").val();
            postdata.port = $("#port").val();
            postdata.username = $("#username").val();
            postdata.password = $("#password").val();
            postdata.database = $("#database").val();
            postdata.id = $("#id").val();
            // console.log(postdata);
            $.ajax({
                type:'post',
                url:'/monitor/source/save',
                data: postdata,
                success:function (data) {
                    // console.log(data);
                    if (data === 'success'){
                        alert("保存成功");
                        $("#tb_departments").bootstrapTable('refresh')
                    }else{
                        alert(data)
                    }
                },error:function () {
                    alert("Error")
                }
            })
        })
    };
    return oInit;
};


