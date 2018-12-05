select * from book where title like %s or author like %s;

select * from image
where image_id in (
    select image_id from image_cpt
    where book_id in (
        select book_id from book
        where title like %s
    )
    and cpt_num=%s
);

select * from image
where image_id in (
    select image_id from image_cpt
    where book_id=%s and cpt_num=%s
);

select * from image where ent_name like %s;