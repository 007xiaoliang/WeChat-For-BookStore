# -*- coding: utf-8 -*-

from bson import json_util
from flask import Blueprint, request, jsonify

from utils import mongodb, pagination, redisUtils, connectionLinux, saveImage, dangRobot
from utils.config import SERVER_IP
from utils.models import User, db, Permission, Role

# 处理业务逻辑
book_bp = Blueprint('book_blueprint', __name__)
mdb = mongodb.Mongodb()  # mongodb连接
reu = redisUtils.RedisClient()  # redis连接
linux = connectionLinux.LinuxConn()  # linux连接


# 加载修改注册用户的权限页面
@book_bp.route("/load_user/", methods=["POST"])
def load_user_view():
    # 接受可能的参数
    entries = request.values.get("entries")  # 每页显示条数
    uname = request.values.get("uname")  # 查询具体用户名的权限信息
    page_now = int(request.values.get("page_now"))  # 当前页面
    if str(entries).isdigit() and str(page_now).isdigit() and int(entries) > 0 and int(page_now) > 0:
        role_list = []
        roles = Role.query.all()
        for role in roles:
            # 根据角色id查询相应的权限
            permission = Permission.query.filter_by(id=role.permission_id).first()
            role_dict = {"role_name": role.role_name, "role_id": role.id, "permission": permission.permission_name}
            role_list.append(role_dict)
        user_list = []
        if uname and uname != '':
            user = User.query.filter_by(name=uname).first()
            if user:
                img_id = user.img_id
                if img_id is None:
                    img_id = '未上传'
                # 查询角色
                role = Role.query.filter_by(id=user.role_id).first()
                room_dict = {"user": user.name, "regis_d": user.regis_date.strftime("%Y-%m-%d %H:%M:%S"), "img": img_id,
                             "role_id": role.id}
                user_list.append(room_dict)
                page_info = {"start_page": 1, "end_page": 1, "page_total": 1,
                             "page_now": 1},
                return jsonify({'info': "ok", 'server': SERVER_IP, 'return_info': user_list, "role_list": role_list,
                                "page_info": page_info})
            else:
                return jsonify({'info': "no"})
        else:
            s_page = int(entries) * (int(page_now) - 1)  # 起始页
            les = User.query.count()
            users = User.query.limit(entries).offset(s_page).all()
            for user in users:
                img_id = user.img_id
                if img_id is None:
                    img_id = '未上传'
                # 查询角色
                role = Role.query.filter_by(id=user.role_id).first()
                room_dict = {"user": user.name, "regis_d": user.regis_date.strftime("%Y-%m-%d %H:%M:%S"), "img": img_id,
                             "role_id": role.id}
                user_list.append(room_dict)
            # 返回分页信息
            page_info = pagination.pagina(les, entries, page_now)
            return jsonify({'info': "ok", 'server': SERVER_IP, 'return_info': user_list, "role_list": role_list,
                            "page_info": page_info})
    else:
        return jsonify({'info': "no"})


# 修改注册用户权限
@book_bp.route("/update_permission/", methods=['POST'])
def update_permission_view():
    uname = request.values.get("user")
    role_id = request.values.get("role_id")
    # 根据用户名查询
    user = User.query.filter_by(name=uname).first()
    # 查看数据库是否有role_id的角色权限
    role = Role.query.filter_by(id=role_id).first()
    if user and role:
        # 修改用户表中权限
        user.role_id = role_id
        db.session.commit()
        return jsonify({'info': "ok"})
    else:
        return jsonify({'info': "no"})


# 加载所有书籍信息并返回到页面
@book_bp.route("/load_book/", methods=['POST'])
def load_book_view():
    # 接受可能的参数
    entries = request.values.get("entries")  # 每页显示条数
    book_name = request.values.get("book_name")  # 查询具体用户名的权限信息
    page_now = int(request.values.get("page_now"))  # 当前页面
    if str(entries).isdigit() and str(page_now).isdigit() and int(entries) > 0 and int(page_now) > 0:
        book_list = []
        if book_name and book_name != '':
            page_records = []
            records = mdb.search({"book_name": book_name})
            for record in records:
                page_records.append(record)
            les = len(page_records)
        else:
            les = mdb.count()
            page_records = mdb.page_query(page_size=int(entries), page_now=int(page_now))
        for page_record in page_records:
            if "book_image1" in page_record.keys():
                book_image1 = page_record.get("book_image1")
            else:
                book_image1 = "未上传.jpg"
            if "book_image2" in page_record.keys():
                book_image2 = page_record.get("book_image2")
            else:
                book_image2 = "未上传.jpg"
            if "book_image3" in page_record.keys():
                book_image3 = page_record.get("book_image3")
            else:
                book_image3 = "未上传.jpg"
            if "book_image4" in page_record.keys():
                book_image4 = page_record.get("book_image4")
            else:
                book_image4 = "未上传.jpg"
            if "book_image5" in page_record.keys():
                book_image5 = page_record.get("book_image5")
            else:
                book_image5 = "未上传.jpg"
            book_dict = {"book_name": page_record.get("book_name"),
                         "book_writer": page_record.get("book_writer"),
                         "book_press": page_record.get("book_press"),
                         "book_press_time": page_record.get("book_press_time"),
                         "book_induction": page_record.get("book_induction"),
                         "book_price": page_record.get("book_price"),
                         "book_type1": page_record.get("book_type1"),
                         "book_type2": page_record.get("book_type2"),
                         "book_image1": book_image1,
                         "book_image2": book_image2,
                         "book_image3": book_image3,
                         "book_image4": book_image4,
                         "book_image5": book_image5
                         }
            book_list.append(book_dict)
        # 返回分页信息
        page_info = pagination.pagina(les, entries, page_now)
        return jsonify({'info': "ok", 'server': SERVER_IP, 'return_info': book_list, "page_info": page_info})
    else:
        return jsonify({'info': "no"})


# 新书上架
@book_bp.route("/save_new_book/", methods=['POST'])
def save_new_book_view():
    # 接受参数
    book_name = request.values.get('book_name', default="")
    book_writer = request.values.get('book_writer', default="")
    book_press = request.values.get('book_press', default="")
    book_press_time = request.values.get('book_press_time', default="")
    book_induction = request.values.get('book_induction', default="")
    book_price = request.values.get('book_price', default="")
    book_type1 = request.values.get('book_type1', default="未知")
    book_type2 = request.values.get('book_type2', default="")
    book_image1 = request.values.get('book_image1', default="")
    # 后端进行校验
    if book_name != "" and book_writer != "" and book_press != "" and book_press_time != "" and book_induction != "" and book_price != "":
        try:
            # 查询mongodb数据库是否已存在相同书籍（书名，作者和出版社相同则视为相同书籍）
            s_condition = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press}
            ret = mdb.search_one(condition1=s_condition)
            if ret is None:
                i_condition = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press,
                               "book_press_time": book_press_time, "book_induction": book_induction,
                               "book_price": book_price, "book_type1": book_type1, "book_type2": book_type2,
                               "book_image1": book_image1}
                mdb.insert(content=i_condition)
                return jsonify({'info': "ok"})
            else:
                return jsonify({'info': "img_exits"})
        except Exception as e:
            print(e)
            return jsonify({'info': "no"})
    else:
        return jsonify({'info': "data_no"})


# 书籍图片操作
@book_bp.route("/save_new_image/", methods=['POST'])
def save_new_image_view():
    book_name = request.form.get('book_name', default="")
    book_writer = request.form.get('book_writer', default="")
    book_press = request.form.get('book_press', default="")
    # 获取当当网图片地址
    book_img1 = request.values.get("book_img1")
    condition = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press}
    edit = {}
    # 查找原来图片的名字
    image_name_ori = mdb.search_one(condition)
    try:
        book_image1 = request.files['book_image1']
        if book_image1.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image1")
            image_name = saveImage.save_image(book_name + book_writer + book_press + "1", book_image1)
            edit["book_image1"] = image_name
        else:
            if not "/static/img/" in book_img1:  # 说明不是本地图片
                edit["book_image1"] = book_img1
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image1")
        edit["book_image1"] = ""
    try:
        book_image2 = request.files['book_image2']
        if book_image2.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image2")
            image_name = saveImage.save_image(book_name + book_writer + book_press + "2", book_image2)
            edit["book_image2"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image2")
        edit["book_image2"] = ""
    try:
        book_image3 = request.files['book_image3']
        if book_image3.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image3")
            image_name = saveImage.save_image(book_name + book_writer + book_press + "3", book_image3)
            edit["book_image3"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image3")
        edit["book_image3"] = ""
    try:
        book_image4 = request.files['book_image4']
        if book_image4.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image4")
            image_name = saveImage.save_image(book_name + book_writer + book_press + "4", book_image4)
            edit["book_image4"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image4")
        edit["book_image4"] = ""
    try:
        book_image5 = request.files['book_image5']
        if book_image5.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image5")
            image_name = saveImage.save_image(book_name + book_writer + book_press + "5", book_image5)
            edit["book_image5"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image5")
        edit["book_image5"] = ""
    # 保存到数据库
    if edit:
        mdb.update(condition, edit)
    return jsonify({'info': "ok"})


# 删除书籍
@book_bp.route("/delete_book/", methods=['POST'])
def delete_book_view():
    # 接受参数
    book_name = request.form.get('book_name', default="")
    book_writer = request.form.get('book_writer', default="")
    book_press = request.form.get('book_press', default="")
    try:
        condition1 = {"book_name": book_name, "book_writer": book_writer, "book_press": book_press}
        condition2 = {"book_image1": 1, "book_image2": 1, "book_image3": 1, "book_image4": 1, "book_image5": 1}
        image_name = mdb.search_one(condition1, condition2)
        mdb.delete(condition1)
        # 从图片服务器删除图片
        linux.delete_img(image_name, "book_image1")
        linux.delete_img(image_name, "book_image2")
        linux.delete_img(image_name, "book_image3")
        linux.delete_img(image_name, "book_image4")
        linux.delete_img(image_name, "book_image5")
        return jsonify({'info': "ok"})
    except Exception as e:
        print(e)
        return jsonify({'info': "no"})


# 更新书籍信息
@book_bp.route("/update_book/", methods=['POST'])
def update_book_view():
    book_name = request.form.get('book_name', default="")
    book_writer = request.form.get('book_writer', default="")
    book_press = request.form.get('book_press', default="")
    book_press_time = request.form.get('book_press_time', default="")
    book_induction = request.form.get('book_induction', default="")
    book_price = request.form.get('book_price', default="")
    book_type1 = request.form.get('book_type1', default="")
    book_type2 = request.form.get('book_type2', default="")
    # 从redis数据库拿到要更新的书籍
    book_name_ori = reu.search("book_name").decode("utf-8")
    book_writer_ori = reu.search("book_writer").decode("utf-8")
    book_press_ori = reu.search("book_press").decode("utf-8")
    condition = {"book_name": book_name_ori, "book_writer": book_writer_ori, "book_press": book_press_ori}
    edit = {"book_name": book_name,
            "book_writer": book_writer,
            "book_press": book_press,
            "book_press_time": book_press_time,
            "book_induction": book_induction,
            "book_price": book_price,
            "book_type1": book_type1,
            "book_type2": book_type2
            }
    try:
        # 更改书籍信息
        mdb.update(condition, edit)
        return jsonify({'info': "ok"})
    except Exception as e:
        print(e)
        return jsonify({'info': "no"})


# 加载要更改图书信息
@book_bp.route("/load_update_book/", methods=['GET'])
def load_update_book_view():
    # 从redis数据库拿到要更新的书籍
    book_name = reu.search("book_name").decode("utf-8")
    book_writer = reu.search("book_writer").decode("utf-8")
    book_press = reu.search("book_press").decode("utf-8")
    # 根据书籍信息去mongodb查询
    book_info = json_util.dumps(
        mdb.search_one({"book_name": book_name, "book_writer": book_writer, "book_press": book_press}))
    return jsonify({'info': "ok", "book_info": book_info, "addr": SERVER_IP})


# 上传轮播图片
@book_bp.route("/update_lunbo/", methods=['POST'])
def update_lunbo_view():
    condition = {"id": 1}
    edit = {"id": 1}
    # 查找原来图片的名字
    image_name_ori = mdb.search_lunbo_set(condition)
    try:
        book_image1 = request.files['book_image1']
        if book_image1.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image1")
            image_name = saveImage.save_image("book_image1", book_image1)
            edit["book_image1"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image1")
        edit["book_image1"] = ""
    try:
        book_image2 = request.files['book_image2']
        if book_image2.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image2")
            image_name = saveImage.save_image("book_image2", book_image2)
            edit["book_image2"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image2")
        edit["book_image2"] = ""
    try:
        book_image3 = request.files['book_image3']
        if book_image3.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image3")
            image_name = saveImage.save_image("book_image3", book_image3)
            edit["book_image3"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image3")
        edit["book_image3"] = ""
    try:
        book_image4 = request.files['book_image4']
        if book_image4.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image4")
            image_name = saveImage.save_image("book_image4", book_image4)
            edit["book_image4"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image4")
        edit["book_image4"] = ""
    try:
        book_image5 = request.files['book_image5']
        if book_image5.filename != "":
            # 从图片服务器删除原来的图片
            linux.delete_img(image_name_ori, "book_image5")
            image_name = saveImage.save_image("book_image5", book_image5)
            edit["book_image5"] = image_name
    except:
        # 从图片服务器删除原来的图片
        linux.delete_img(image_name_ori, "book_image5")
        edit["book_image5"] = ""
    # 保存到数据库
    mdb.update_lunbo(condition, edit)
    return jsonify({'info': "ok"})


# 页面加载轮播图片
@book_bp.route("/load_lunbo/", methods=['POST'])
def load_lunbo_view():
    # 查询数据库获取所有图片
    image_name = json_util.dumps(mdb.search_lunbo_set({"id": 1}))
    return jsonify({'info': "ok", "image_name": image_name, "addr": SERVER_IP})


# 上传书店书籍分类
@book_bp.route("/save/category/", methods=['POST'])
def save_category_view():
    # 接受参数
    categories = request.form.to_dict()
    # 清空原有书籍分类表
    mdb.drop_category_set()
    try:
        for k, v in categories.items():
            num = 0
            v_arr = v.strip(" ").split(" ")
            content = {}
            for cate in v_arr:
                if cate is not "":
                    num += 1
                    content[str(num)] = cate
            # 存储到数据库
            mdb.insert_category(content)
    except:
        return jsonify({'info': "no"})
    return jsonify({'info': "ok"})


# 加载书店书籍分类
@book_bp.route("/load/category/", methods=['POST'])
def load_category_view():
    # 查询数据库得到书籍分类信息
    cate_infos = mdb.search_category_set()
    cate_list = []
    for cate_info in cate_infos:
        cate_s = ""
        for value in cate_info.values():
            cate_s += value + " "
        cate_list.append(cate_s)
    return jsonify({'info': "ok", "cate_info": cate_list})


# 从当当网爬取数据
@book_bp.route("/search/dangdang/", methods=['POST'])
def search_dangdang_view():
    id = request.values.get("id")  # 爬取类型，1表示爬取单条书籍，2表示批量爬取
    url = request.values.get("url")  # 爬取路径
    page_info = dangRobot.Robot(int(id), url).search_info()
    # 上传到mongodb数据库
    if int(id) is 2:
        mdb.insert_many(page_info)
    return jsonify({'info': "ok", "page_info": json_util.dumps(page_info)})
