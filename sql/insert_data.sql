use csc346;

insert into users (first_name, last_name, email, pw_hash)
    values('Morgan', 'Henry', 'mh@email.arizona.edu', '1234');

insert into users (first_name, last_name, email, pw_hash)
    values('Laura', 'Shoemake', 'ls@email.arizona.edu', '1234');

insert into users (first_name, last_name, email, pw_hash)
    values('Calvin', 'McLean', 'cm@email.arizona.edu', '1234');

insert into users (first_name, last_name, email, pw_hash)
    values('Lindsy', 'Henry', 'lh@email.arizona.edu', '1234');


insert into dog (owner_id, name, description, location, gender)
    values ((select id from users where first_name="Morgan"),
            'Sammi', 'loving dog who hates to cuddle', 'Chico CA', 'Female');

insert into dog (owner_id, name, description, location, gender)
    values ((select id from users where first_name="Laura"),
            'Fluffy', 'Small dog, big personality', 'Phoenix AZ', 'Male');

insert into favorite (user_id, dog_id)
    values ((select id from users where first_name='Calvin'),
            (select id from dog where name='Fluffy'));
