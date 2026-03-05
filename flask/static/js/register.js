function bindEmailCaptchaClick(){
    $("#get-code").click(function (event){
        var $this = $(this)
        event.preventDefault();
        var email = $("input[name='email']").val();
        $.ajax({
            url: "/auth/captcha/email?email="+email,
            method: "GET",
            success: function (result){
                var code = result['code'];
                if(code == 200)
                {
                    var countdown = 60;
                    $this.off("click");
                    var timer = setInterval( function(){
                        $this.text(countdown);
                        countdown -= 1;
                        if(countdown <= 0){
                            clearInterval(timer);
                            $this.text("获取验证码");
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    alert("验证码已发送！");
                }
                else
                {
                    alert(result['message']);
                }
                console.log(result);
            },
            error: function (error){
                console.log(error);
            }
        })
    });
}

$(function (){
    bindEmailCaptchaClick();
});
