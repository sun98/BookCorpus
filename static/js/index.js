window.onload = function () {
    waterfall('box', 'main');
    //此处模拟后台元素
    var dataInt = { "data": [{ "src": '1.jpg' }, { "src": '2.jpg' }, { "src": '3.jpg' }] }
    window.onscroll = function () {
        if (checkScrollSlide()) {
            //将数据渲染到页面尾部
            var oParent = document.getElementById('main');
            for (var i = 0; i < dataInt.data.length; i++) {
                var oBox = document.createElement('div');
                oBox.className = 'box';
                oParent.appendChild(oBox);
                var opic = document.createElement('div');
                opic.className = 'pic';
                oBox.appendChild(opic);
                var oimg = document.createElement('img');
                oimg.src = "images/" + dataInt.data[i].src;
                opic.appendChild(oimg);
            }
            waterfall('box', 'main');
        }
    }
}

function waterfall(box, parent) {
    var oParent = document.getElementById(parent);
    var oBoxs = getByClass(box, oParent);
    //获取图片所占有的全部宽度
    var oBoxW = oBoxs[0].offsetWidth;
    //图片的列数
    var cols = Math.floor(document.documentElement.clientWidth / oBoxW);
    oParent.style.cssText = 'width:' + oBoxW * cols + 'px;margin: 0 auto';
    //用数组存放图片高度，为了使下一列的图片从上一行中高度最小的图片下面排列
    var hArr = [];
    for (var i = 0; i < oBoxs.length; i++) {
        if (i < cols) {
            //获取第一列元素的高度
            hArr.push(oBoxs[i].offsetHeight);
        } else {
            var minH = Math.min.apply(null, hArr);
            var index = getMinhIndex(hArr, minH);
            oBoxs[i].style.position = 'absolute';
            oBoxs[i].style.top = minH + 'px';
            oBoxs[i].style.left = index * oBoxW + 'px';
            hArr[index] += oBoxs[i].offsetHeight;
        }
    }
}


function getByClass(cName, parent) {
    var oParent = oParent ? document.getElementById(parent) : document,
        eles = new Array(),
        elements = oParent.getElementsByTagName('*');
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].className == cName) {
            eles.push(elements[i]);
        }
    }
    return eles;
}

//获取高度最小的元素的索引值
function getMinhIndex(arr, val) {
    for (var i in arr) {
        if (arr[i] == val) {
            return i;
        }
    }
}


//判断是否具备加载效果
function checkScrollSlide() {
    var oParent = document.getElementById('main');
    var oBoxs = getByClass('box', oParent);
    var lastBoxH = oBoxs[oBoxs.length - 1].offsetTop + Math.floor(oBoxs[oBoxs.length - 1].offsetHeight / 2);
    //获取页面滚动的距离，为了兼容，此处有在混合模式下和在标准模式下
    var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.body.clientHeight || document.documentElement.clientHeight;
    return (lastBoxH < scrollTop + height) ? true : false;
}
