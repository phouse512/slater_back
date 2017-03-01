/*
 * the sql that supports the banks table, holding accounts for money
 */

create table banks (
    id serial not null, 
    type char(4) default 'poll', 
    entity_id integer, 
    created_at timestamp default current_timestamp
);
