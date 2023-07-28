layui.define(function(exports){
    var $ = layui.$

    let http = function({
        method, url, data, success, error
                        }){
        let headers = {
            "Content-Type": "application/json;charset=utf-8"
        }

        let params = {
            type: method,
            url,
            headers,
            success,
            error
        }
        if(method === 'POST'){
            params['data'] = JSON.stringify(data)
        }
        $.ajax(params)
    }

    let ajaxGet = function({url, success, error}){
        http({
            method: 'GET',
            url,success,error
        })
    }

    let ajaxPost = function({url, data, success, error}){
        http({
            method: 'POST',
            url,data, success,error
        })
    }

    exports('func', {ajaxGet, ajaxPost})
})