/**
 * Created by zdf on 2016/10/5.
 */

function refresh() {
    alert("refresh start!");
    $.get("/userinfo/", function () {
        //用ajax传递请求
    })
    alert("refresh Done!");
}
