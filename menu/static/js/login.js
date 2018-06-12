function check_reg() {
    let user = $('#username').val();
    console.log('user', user)
    let psd = $('#password').val();
    let errmsg = $('#error_msg');
    if (user == '' || psd == '') {
        let msg = '输入不能为空';
        //alert(msg)
        errmsg.text(msg);
        return false;
    }
    return true
}
