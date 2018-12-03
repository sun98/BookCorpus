drop database bookcorpus;
create database bookcorpus;
use bookcorpus;

-- book
create table book
(
    book_id int not null unique,
    title varchar(512) not null,
    author varchar(128) not null,
    subject varchar(128),
    language varchar(64),
    release_date date,
    price float,
    copyright varchar(128),
    primary key(book_id)
);

-- chapter
create table chapter
(
    book_id int not null unique,
    cpt_num int not null unique,
    primary key(book_id, cpt_num)
);

-- entity
create table entity
(
    book_id int not null unique,
    ent_name varchar(64) not null,
    primary key(book_id,ent_name)
);

-- image
create table image
(
    image_id int not null unique auto_increment,
    book_id int not null unique,
    ent_name varchar(64) not null,
    primary key(image_id),
    foreign key(book_id) references book(book_id)
);

-- cpt_ent
CREATE TABLE cpt_ent
(
    book_id int not null unique,
    cpt_num int not null unique,
    ent_name varchar(64) not null,
    PRIMARY KEY(book_id,cpt_num,ent_name)
);

-- image_cpt
CREATE TABLE image_cpt(
    image_id int not null unique auto_increment,
    book_id int not null unique,
    cpt_num int not null unique,
    primary KEY(image_id, book_id, cpt_num)
)