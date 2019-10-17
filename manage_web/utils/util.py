import math


def pagina(les, entries, page_now):
    page_total = math.ceil(les / int(entries))
    start_page = page_now - 2
    if start_page < 1:
        start_page = 1
    end_page = start_page + 4
    if end_page > page_total:
        end_page = page_total
    if end_page < 5:
        start_page = 1
    else:
        start_page = end_page - 4
    return {"start_page": start_page, "end_page": end_page, "page_total": page_total, "page_now": page_now}


# 订单状态的数字与汉字对应
def filter_status(order_status):
    order_status = int(order_status)
    if order_status == 0:
        return "未付款"
    elif order_status == 1:
        return "已付款"
    elif order_status == 2:
        return "配送中"
    elif order_status == 3:
        return "已完成"
