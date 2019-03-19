use csc346;

create table users
(
    id int(6) NOT NULL AUTO_INCREMENT,
    first_name varchar(64),
    last_name varchar(64),
    email varchar(128),
    pw_hash varchar(255),
    PRIMARY KEY (id)
);

create table dog
(
    id int(6) NOT NULL AUTO_INCREMENT,
    owner_id int(6),
    name varchar(64),
    description varchar(255),
    location varchar(64),
    gender varchar(12),
    PRIMARY KEY (id)
);

create table listing
(
    dog_id int(6),
    owner_id int(6),
    price int(6),
    PRIMARY KEY (dog_id, owner_id)

);

create table favorite
(
    user_id int(6),
    dog_id int(6),
    PRIMARY KEY (user_id, dog_id)
);
