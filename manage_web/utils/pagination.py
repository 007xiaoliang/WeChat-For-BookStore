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
