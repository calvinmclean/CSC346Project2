use csc346;

insert into users (first_name, last_name, email, pw_hash)
    values('Morgan', 'Henry', 'mh@email.arizona.edu', '1234');

insert into users (first_name, last_name, email, pw_hash)
    values('Laura', 'Shoemake', 'ls@email.arizona.edu', '1234');

insert into users (first_name, last_name, email, pw_hash)
    values('Calvin', 'McLean', 'cm@email.arizona.edu', '1234');

insert into users (first_name, last_name, email, pw_hash)
    values('Lindsy', 'Henry', 'lh@email.arizona.edu', '1234');


insert into dog(name, gender, age, color, city, state, description)
    values ('Sammi', 'Female', 15, 'red', 'Chico' , 'CA', 'loving dog who hates to cuddle');

insert into dog(name, gender, age, color, city, state, description)
    values ('Fluffy', 'Male', 1, 'Stable', 'Phoenix' , 'AZ', 'Shy pupper, but loves to play when he gets to know you');

insert into listing (owner_id, dog_id, price, contact)
    values((select id from users where first_name="Morgan"),
          (select id from dog where name="Sammi"), 1200, 'email: email@email.com, phone: 555-555-5555');

insert into favorite (user_id, dog_id)
    values ((select id from users where first_name='Calvin'),
            (select id from dog where name='Fluffy'));
