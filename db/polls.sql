/*
 * the polls and poll answer table definitions
 */

create table polls (
    id serial not null,
    title varchar(150),
    is_pre bool default true,
    close_time timestamp,
    correct_answer integer,
    buy_in integer default 30,
    finished bool default false,
    created_at timestamp default current_timestamp
);

create table poll_answers (
    id serial not null,
    poll_id integer NOT NULL,
    title varchar(100) NOT NULL
);
