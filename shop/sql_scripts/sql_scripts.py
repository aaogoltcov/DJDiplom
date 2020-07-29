from django.db import connection


def dict_fetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


SELECT_PAPERS = '''
    select  p.id paper_id,
            p.name paper_name,
            p.title paper_title,
            p."text" paper_text,
            null goods
    from shop_paper p
    order by p."order"
'''

SELECT_GOODS_IN_PAPERS = '''
    select  p.id paper_id,
            g.id good_id,
            g.name good_name,
            g.image good_image,
            g.description good_desctiption,
            g."date" good_date
    from shop_paper p
    left join shop_good g on g.papers_id = p.id
    order by g."date" desc
'''

SELECT_CATALOG = '''
    select  c.id catalog_id,
            c.name catalog_name,
            c."date" catalog_date,
            null goods
    from shop_catalog c
    order by c."order"
'''

SELECT_GOODS_IN_CATALOG = '''
    select  c.id catalog_id,
            g.id good_id,
            g.name good_name,
            g.image good_image,
            g.description good_desctiption,
            g."date" good_date
    from shop_catalog c
    left join shop_good g on g.catalog_id = c.id
    order by g."date" desc
'''

SELECT_MENU = '''
    select 	c.id catalog_id,
            c.name catalog_name
    from shop_catalog c
    order by c."order"
'''

SELECT_SUB_MENU = '''
    select 	cs.catalog_id catalog_id,
            cs.id sub_catalog_id,
            cs.name sub_catalog_name
    from shop_subcatalog cs
    order by cs."order"
'''


def get_good_info_and_feedback(good_id):
    SELECT_GOOD_INFO = '''
        select  g.id good_id,
                g.name good_name,
                g.image good_image,
                g.description good_desctiption,
                g.price good_price,
                g."date" good_date
        from shop_good g
        where g.id = %d
    ''' % int(good_id)

    SELECT_GOOD_FEEDBACK = '''
        select  g.id good_id,
                f.id feedback_id,
                f.author_id feedback_author_id,
                f."date" feedback_date, 
                f.description feedback_description,
                f.person_name feedback_person_name,
                f.score feedback_score,
                u.id user_id,
                u.first_name user_name,
                u.username user_username
        from shop_good g
        left join shop_feedback f on f.good_id = g.id 
        left join auth_user u on u.id = f.author_id 
        where g.id = %d
    ''' % int(good_id)

    with connection.cursor() as cursor:
        good = dict_fetchall(cursor.execute(SELECT_GOOD_INFO))
        feedbacks = dict_fetchall(cursor.execute(SELECT_GOOD_FEEDBACK))
        good[0]['feedbacks'] = [feedback for feedback in feedbacks if feedback['feedback_id']]
    return good