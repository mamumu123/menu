// 检查是否合法
function check_reg() {
    let user = $('#username').val();
    console.log('user', user)
    let psd = $('#password').val();
    let re_psd = $('#repassword').val();
    let errmsg = $('#error_msg');
    if (user == '' || psd == '') {
        let msg = '输入不能为空';
        //alert(msg)
        errmsg.text(msg);
        return false;
    }
    if (user.length < 5 || user.length > 20) {
        let msg = '用户名长度要求在5-20,请重新修改';
        errmsg.text(msg);
        return false;
    }
    if (psd.length < 5 || psd.length > 20) {
        let msg = '密码长度要求在5-20,请重新修改';
        errmsg.text(msg);
        return false;
    }
    if (psd != re_psd) {
        let msg = '两次密码不一致，请重新输入';
        errmsg.text(msg);
        return false;
    }
    return true
}
