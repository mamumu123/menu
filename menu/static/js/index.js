const app = new Vue({
    //指定元素
    el: '#app',
    //数据
    data: {
        list: [],//购物车数据
        car: 1,//一个Flag，作为判断主页面右侧的逻辑
        new_list: [],   //支付时的数据
        dis: false,//一个Flag,用于判断是否需要添加额外单品
        add_single: []  //增加一个单品的信息
    },
    //方法
    methods: {
        //增加单品
        add_menu(e) {
            let btn = e.currentTarget; // 当前元素
            //console.info("btn", btn);
            let tds = $(btn).parent().siblings();//获取当前元素的父节点的全部兄弟节点，就是当前这行的所有td
            let id = $(tds).eq(0).text();//获取商品名称的td的文本值
            let flag = 0
            for (let item of this.list) {
                if (item['id'] == id) {
                    flag = id;
                    item['count'] += 1;
                    break;
                }
            }
            if (flag != 0) {
                //console.log(flag, '\nequal')
            }
            else {
                let name = $(tds).eq(1).text();//
                //console.info("name", name);
                let price = $(tds).eq(2).text();//
                //console.info("price", price);
                let data = {id, name, count: 1, price, complated: true};
                //console.log('data', data);
                this.list.push(data);
            }


        },
        //增加套餐
        add_mul(e) {
            let btn = e.currentTarget; // 当前元素
            // console.info("btn", btn);
            let tds = $(btn).parent().siblings();//获取当前元素的父节点的全部兄弟节点，就是当前这行的所有td
            let zucheng_tem = $(tds).eq(2).text();//
            //console.info("zucheng_tem", zucheng_tem);
            let zucheng = String(zucheng_tem).split(' ');

            //遍历，获得需要的id,name, num,
            for (let per of zucheng) {
                let name_id = per.trim().split('*')[0]
                let id = name_id.slice(0, 8);
                let num = Number(per.trim().split('*')[1].split('￥')[0]);
                //flag 用于判断之前是否有这个单品
                let flag = 0
                for (let item of this.list) {
                    //如果找到已经添加
                    if (item['id'] == id) {
                        flag = id;
                        //count++
                        item['count'] += num;
                        break;
                    }
                }

                if (flag != 0) {
                    //console.log(flag, '\nequal')
                }
                //如果之前没有添加过
                else {
                    let name = name_id.slice(8)
                    let price = per.trim().split('*')[1].split('￥')[1]
                    let data = {id, name, count: num, price, complated: true};
                    // console.log('data', data);
                    this.list.push(data);
                }
            }
            // let data = {id, name, count: 1, price, complated: true};
            // console.log('data', data);
            // this.list.push(data);
        },
        //在购物车中减少数量
        hangleReduce(index) {
            //如果已经为1，则不能再减少，可以直接删除
            if (this.list[index].count == 1) return;
            this.list[index].count -= 1;
        },
        //在购物车中增加数量
        hangleUp(index) {
            this.list[index].count += 1;
        },
        //移除购物车物品
        handleRemove(index) {
            this.list.splice(index, 1);
        },
        //物品选购完成，开始支付
        cal_sum() {
            this.car = 0
        },
        //支付
        //将表单提交到后台，如果提交成功，则在三面后返回空购物车
        sub_mit() {
            let _this = this;
            let cost = _this.totalprice;
            let new_cost = _this.new_totalprice;
            let myDate = new Date();
            let time = String(myDate.toLocaleString());        //获取日期与时间
            console.log('time', time)
            let _user = document.querySelector('#username')
            let user = _user.textContent;
            console.log('user', user)
            //合成数据，向后台传输
            let data = {
                list: _this.new_list,
                cost,
                new_cost,
                time,
                user

            };
            // console.log(data.list);
            $.ajax({
                type: "POST",
                url: "/index/sub_mit",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=UTF-8', //
                success: function () {
                    let message = '提交成功，祝你用餐愉快(三秒后跳转回购物车）';
                    let msg = document.querySelector('#car_msg');
                    msg.textContent = message;
                    setTimeout(function () {
                        console.log('正在等待')
                        _this.car = 1;
                        _this.list = [];
                    }, 3000);
                },
                error: function (err) {
                    let message = '发生错误，请重新尝试'
                    let msg = document.querySelector('#car_msg')
                    msg.textContent = message
                    console.log('发生错误', err)

                }
            })
        },
        //如果点击按钮，则会将改单品加入到list，节省更多钱
        add_one() {
            let _this = this;
            let id = _this.add_single[0];
            let name = _this.add_single[1];
            let price = _this.add_single[2];
            let flag = 0;
            //判断该单品之前是否已经存在
            for (let item of this.list) {
                if (item['id'] == id) {
                    flag = id;
                    item['count'] += 1;
                    break;
                }
            }
            if (flag != 0) {
                //console.log(flag, '\nequal')
            }
            //如果之前 没有添加过
            else {
                //console.info("price", price);
                let data = {id, name, count: 1, price, complated: true};
                //console.log('data', data);
                this.list.push(data);
            }
        }
    },
    //计算属性
    computed: {
        //单品时的总价
        totalprice() {
            let total = 0;
            for (let i of this.list) {
                total += (i.price * i.count)
            }

            return total;
        },
        //组合套餐后的总价
        new_totalprice() {
            let total = 0;
            for (let i of this.new_list) {
                total += (i.price * i.count)
            }

            return total;
        }
    },
    //检测 list,如果有变化，就自动触发
    //当list改变时，会自动用到ajax，得到两件东西
    //一：最简套餐：并将其赋值到new_list
    //二：再添加一个单品，省更多钱
    watch: {
        list: {
            handler(newValue) {
                let _this = this;
                let data = {
                    list: newValue
                };
                //console.log('数组发生了改变');
                $.ajax({
                    type: "POST",
                    url: "/index/cal_sum",
                    data: JSON.stringify(data),
                    contentType: 'application/json; charset=UTF-8', //
                    success: function (data) {
                        //let json_data = JSON.parse(data);//后台返回的json数据需要转为对象
                        let json_data = eval("(" + data + ")");
                        let cost = Number(json_data['cost']);
                        let tem_s = json_data['tem_s'];
                        let tem_m = json_data['tem_m'];
                        let get_num = json_data['num'];
                        let target_single = json_data['target_single'];
                        let target_cost = json_data['target_min'];
                        let target_s = Number(json_data['target_s']);
                        let target_m = json_data['target_m'];
                        let target_num = json_data['target_num'];


                        _this.new_list = []
                        for (let i in tem_m) {
                            let id = tem_m[i][0];
                            let name = tem_m[i][1];
                            let price = tem_m[i][2];
                            let num = get_num[id];
                            let new_data = {id, name, count: num, price, complated: true};
                            _this.new_list.push(new_data);
                        }
                        for (let i in tem_s) {
                            let id = tem_s[i][0];
                            let name = tem_s[i][1];
                            let price = tem_s[i][2];
                            let num = get_num[id];
                            let new_data = {id, name, count: num, price, complated: true};
                            _this.new_list.push(new_data);
                        }
                        let if_add = document.querySelector('#if_add');
                        //添加单品
                        if (if_add && _this.car == 1 && _this.list.length) {
                            let jiage = String(Number(target_single[2]) + cost - target_cost);
                            console.log(Number(target_single[2]));
                            console.log(cost);
                            console.log(target_cost);
                            console.log('jiage', jiage);
                            if (Number(jiage) != 0) {
                                _this.dis = true;
                                _this.add_single = target_single;
                                let msg = '如果再增加一个' + String(target_single[1]) + ',就可以节省' + jiage + '块钱'

                                if_add.textContent = msg;
                                console.log('msg is changing ')

                            }
                            else {
                                if_add.textContent = '';
                                _this.dis = false
                            }
                        }
                    },
                    error: function (err) {
                        console.log("错误");
                        console.log(err);
                    }

                });
            },
            deep: true
        }
    }
})