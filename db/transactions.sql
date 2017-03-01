/*
 * the transactions table, responsible for holding to/from payments
 */

create table transactions (
    id serial not null,
    from_entity integer not null,
    to_entity integer not null,
    balance integer not null,
    type char(10) default 'payment',
    created_at timestamp default current_timestamp
);
