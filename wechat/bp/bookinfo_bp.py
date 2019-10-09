from flask import Blueprint, jsonify, request, render_template

# 处理书籍展示
from utils import CreateSign, mongodb
from utils.config import SERVER_IP
from utils.util import check_image

book_info_bp = Blueprint('bookinfo_blueprint', __name__)
# 创建mongodb连接
mdb = mongodb.Mongodb()


# 进入商城主页
@book_info_bp.route('/index', methods=["GET", "POST"], endpoint="index")
def index_view():
    if request.method == "GET":
        # 获取主页面需要的信息
        # 获取菜单项
        cate_infos = mdb.search_category()
        cate_list = []
        for cate_info in cate_infos:
            cate_list.append(cate_info)
        # 获取轮播图信息
        lunbo_info = mdb.search_lunbo()
        # 填充主页面信息
        main_info = mdb.main_search()
        return render_template("index.html", cate_list=cate_list, lunbo_info=lunbo_info, main_info=main_info)
    else:
        local_url = request.values.get("link")
        appid, timestamp, signature, nonceStr = CreateSign.wx_config(url=local_url)
        return jsonify({'appid': appid, 'timestamp': timestamp, 'signature': signature, 'nonceStr': nonceStr})


# 改变主页面显示内容
@book_info_bp.route('/change/info', methods=["GET", "POST"])
def change_ingo_view():
    main_info = mdb.main_search()
    return jsonify({"main_info": main_info})


# 进入商品详情页
@book_info_bp.route('/details', methods=["GET", "POST"])
def details_view():
    book_name = request.args.get("book_name").replace("*******", "+")
    book_writer = request.args.get("book_writer").replace("*******", "+")
    book_press = request.args.get("book_press").replace("*******", "+")
    # 查询图书详细信息并返回页面
    condition = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press}
    book_info = mdb.search_one(condition=condition)
    book_info = check_image(book_info)
    book_image = []
    for k, v in book_info.items():
        if "book_image" in k:
            if v != "":
                if "http" not in v:
                    book_image.append(SERVER_IP + v)
                else:
                    book_image.append(v)
    return render_template("details.html", book_info=book_info, book_image=book_image)


# 进入搜索详情页
@book_info_bp.route('/search/type', methods=["GET", "POST"])
def search_type_view():
    book_type1 = request.args.get("book_type1")
    book_type2 = request.args.get("book_type2")
    # 根据类型查询数据库
    main_info = mdb.query_search({"book_type1": book_type1, "book_type2": book_type2})
    main_list = []
    for info in main_info:
        info = check_image(info)
        main_list.append(info)
    return render_template("search.html", main_info=main_list, book_type1=book_type1, book_type2=book_type2)


# 动态加载信息
@book_info_bp.route('/search/reload', methods=["GET", "POST"])
def search_reload_view():
    book_type1 = request.values.get("book_type1")
    book_type2 = request.values.get("book_type2")
    pageid = int(request.values.get("pageid"))
    # 根据类型查询数据库
    query_filter = {"book_type1": book_type1, "book_type2": book_type2}
    main_info = mdb.query_search(query_filter=query_filter, skip=pageid)
    info_list = []
    for cate in main_info:
        cate = check_image(cate)
        info_list.append(cate)
    return jsonify({"main_info": info_list})


# 根据关键字搜索
@book_info_bp.route('/search', methods=["GET", "POST"])
def search_view():
    keyword = request.values.get("keyword").replace("*******", "+")
    count, info_list = mdb.search_in_keyword(keyword=keyword)
    return jsonify({"info_list": info_list, "count": count})
