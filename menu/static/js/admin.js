function check_reg() {
    let ID = $('#ID').val();
    let name = $('#name').val();
    let price = $('#price').val();
    if (ID == '' || name == '' || price == '') {
        let msg = document.querySelector('#errmsg');
        msg.textContent = '输入不能为空';
        return false;
    }
    if (ID[0] != 'S' || ID.length != 8) {
        let msg = document.querySelector('#errmsg');
        msg.textContent = 'ID填写错误，请重新阅读规则';
        return false;
    }
    return true
}

function check_mul_reg() {
    let ID = $('#input_mul_ID').val();
    let name = $('#input_mul_name').val();
    let mix = $('#input_mul_mix').val();
    let price = Number($('#input_mul_price').val());
    if (ID == '' || name == '' || price == '') {
        let msg = document.querySelector('#errmsg');
        msg.textContent = '输入不能为空';
        return false;
    }
    if (ID[0] != 'M' || ID.length != 8) {
        let msg = document.querySelector('#errmsg');
        msg.textContent = 'ID填写错误，请重新阅读规则';
        return false;
    }
    let per = mix.trim().split(' ')
    let sum = 0
    for (let item of per) {
        let perprice = Number((item.split('￥')[1]).split('*')[0])
        console.log('perprice', perprice)
        sum += perprice
    }
    console.log(sum, price)
    if (sum < price) {
        let msg = document.querySelector('#errmsg');
        msg.textContent = '套餐总价须低于单品总价，请重新填写';
        return false;
    }
    return true
}


//提交单
function insertMenu() {
    if (check_reg()) {
        let dataForm = [];
        $(".input_menu").each(function () {
            dataForm.push(this.value);
        })
        console.log("dataForm", dataForm)
        let data = {
            "dataForm": dataForm
        };
        $.ajax({
            url: '/admin/insertMenu',
            type: 'post',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8', //指定传递给服务器的是Jso
            success: function () {
                console.log('success')
                let msg = document.querySelector('#errmsg')
                msg.textContent = '添加成功'
            },
            error: function (err) {
                console.log('error')
                let errmsg = document.querySelector('#errmsg')
                errmsg.textContent = '插入错误，请仔细阅读规则'
                console.log(err)
            }
        })
    }
}

//提交套餐
function insertMul() {
    if (check_mul_reg()) {
        let dataForm = [];
        $(".input_mul").each(function () {
            dataForm.push(this.value);
        })
        console.log("dataForm", dataForm)
        let data = {
            "dataForm": dataForm
        };
        $.ajax({
            url: '/admin/insertMul',
            type: 'post',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8', //指定传递给服务器的是Jso
            success: function () {
                console.log('success')
                let msg = document.querySelector('#errmsg')
                msg.textContent = '添加成功'
            },
            error: function (err) {
                console.log('error')
                console.log(err)
                let msg = document.querySelector('#errmsg')
                msg.textContent = '插入错误，请仔细阅读规则'

            }
        })
    }
}

function insert_to_mul() {
    let num = $('#input_mul_num').val();
    //console.log('num', num);
    let select_single = $('#select_single').val();
    console.log('select_single', select_single);
    let input_mul_mix = $('#input_mul_mix');
    //let select_ID = $('#select_single').find("option:selected").val();
    //let select_price = $('#select_single').find("option:selected").text();
    //console.log('price', select_ID, select_price);
    input_mul_mix.val(input_mul_mix.val() + select_single + '*' + num + ' ')
}