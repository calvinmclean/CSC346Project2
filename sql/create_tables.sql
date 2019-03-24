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
    gender varchar(12),
    age int(6),
    color varchar(64),
    city varchar(64),
    state varchar(64),
    description varchar(255),
    PRIMARY KEY (id)
);

create table listing
(
    dog_id int(6) NOT NULL,
    price int(6),
    contact varchar(255),
    PRIMARY KEY (dog_id)

);

create table favorite
(
    user_id int(6),
    dog_id int(6),
    PRIMARY KEY (user_id, dog_id)
);
