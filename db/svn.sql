-- mysql

drop database if exists svn;
create database svn collate utf8mb4_general_ci;

use svn;

create table access_group(
	id int unsigned not null auto_increment primary key,
    group_code_name varchar(20) not null,
    group_name varchar(20),
    sub_groups text,
    group_users text,
    description varchar(500)
);

create table access_path(
	id int unsigned not null auto_increment primary key,
    repo_name varchar(100),
	dir_name varchar(500) not null,
    par_path_id int unsigned,
    description varchar(500)
);

create table access_rule(
	id int unsigned not null auto_increment primary key,
    path_id int unsigned not null,
    rank tinyint unsigned not null,
    unit char(1) not null,
    ref varchar(10) not null,
    priv varchar(5) not null
);


