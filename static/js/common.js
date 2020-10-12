$(document).ajaxError(function (event,xhr,settings,e) {
    if (xhr.status==401){
        // 跳转到登录(首页)页面、并携带 回跳的地址
        let url = xhr.responseJSON.url
        if (url != "") {
            // 跳转到首页
            window.location.href = "/?url=" + escape(url)
        } else {
            window.location.href = "/"
        }
    }
})