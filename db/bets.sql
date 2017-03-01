/*
 * bets table schema
 */

create table bets (
    id serial not null,
    user_id integer not null,
    poll_id integer not null,
    choice_id integer not null,
    multiplier integer default 1,
    created_at timestamp default current_timestamp
);
