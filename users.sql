/* 
 * sql surrounding users table:
 *   - create table syntax
 */

create table users (
    id serial not null,
    username varchar(50),
    created_at timestamp default current_timestamp,
    pw_hash char(60)
);
