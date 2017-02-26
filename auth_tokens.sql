/* 
 * sql surrounding auth_tokens table:
 *   - create table syntax
 */

create table auth_tokens (
    id serial not null,
    created_at timestamp default current_timestamp,
    expires_at timestamp default current_timestamp + interval '10 days',
    user_id integer,
    auth_token char(36)
);
