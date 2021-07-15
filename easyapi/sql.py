from sqlalchemy import Table
from dataclasses import dataclass

# _or__like_<attr>:*** 、 _or_<attr>:*** ,  :   SELECT * from student WHERE id = 1 or id = 2 AND age = 20;   - 查询结果是id = 2且age = 20或者id=1
# _or_:[{id:1},{id:2}]    :                     SELECT * from student WHERE (id = 1 or id = 2 )
def search_sql(sql, query: dict, table: Table):
    for k in query.keys():
        if type(query[k]) is not list:
            # 兼容处理
            values = [query[k]]
        else:
            values = query[k]
        if k.startswith('_gt_'):
            for v in values:
                sql = sql.where(getattr(table.c, k[4:]) > v)
        elif k.startswith('_gte_'):
            for v in values:
                sql = sql.where(getattr(table.c, k[5:]) >= v)
        elif k.startswith('_lt_'):
            for v in values:
                sql = sql.where(getattr(table.c, k[4:]) < v)
        elif k.startswith('_lte_'):
            for v in values:
                sql = sql.where(getattr(table.c, k[5:]) <= v)
        elif k.startswith('_like_'):
            for v in values:
                sql = sql.where(getattr(table.c, k[6:]).ilike('%' + v + '%'))
        elif k.startswith('_in_'):
            if values:
                sql = sql.where(getattr(table.c, k[4:]).in_(values))
        else:
            sql = sql.where(getattr(table.c, k) == values[0])
    return sql


@dataclass
class Pager:
    """
    分页
    """
    page: int = None
    per_page: int = None


@dataclass
class Sorter:
    """
    排序
    """
    sort_by: str = 'id'
    desc: bool = True
