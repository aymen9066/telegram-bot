create table if not exists users
(
    id            serial primary key,
    chat_id       bigint unique,
    first_name    text    not null,
    last_name     text,
    username      text,
    is_bot        boolean not null,
    language_code text default 'fr',
    password      text,
    role          text default 'client',
    constraint check_role check (role in ('client', 'mecanicien', 'bot'))
);
insert into users(first_name, last_name, username, is_bot, role) values('telegram', 'bot', 'driveSafe', true, 'bot');
select setval('users_id_seq', currval('users_id_seq')+1);

create table if not exists car_brand
(
    id   serial primary key,
    name text not null unique
);

create table if not exists car_model
(
    id              serial primary key,
    id_brand        int  not null,
    name            text not null,
    production_year int,
    constraint fk_idbrand foreign key (id_brand) references car_brand (id)
);

create table if not exists cars
(
    id        serial primary key,
    id_model  int not null,
    km_dirven int,
    constraint fk_idmodel foreign key (id_model) references car_model (id)
);

create table if not exists car_listing
(
    id_car  int,
    id_user int,
    primary key (id_car, id_user),
    constraint fk_idcar foreign key (id_car) references cars (id),
    constraint fk_iduser foreign key (id_user) references users (id)
);

create table if not exists chats
(
    id bigint primary key
);
create table if not exists chat_users(
    chat_id bigint not null,
    user_id int not null,
    primary key (chat_id, user_id),
    constraint fk_chatid foreign key (chat_id) references chats(id),
    constraint fk_userid foreign key (user_id) references users(id)
);
create table if not exists messages(
    id serial primary key ,
    chat_id bigint not null,
    user_id int not null,
    number int not null,
    content text not null,
    constraint fk_chatid foreign key (chat_id) references chats(id),
    constraint fk_userid foreign key (user_id) references users(id)
);
create or replace view message_view as
    select chat_users.chat_id as chat_id, chat_users.user_id as user_id, messages.id as message_id, messages.number as number, messages.content as content
    from chat_users, messages
    where chat_users.chat_id = messages.chat_id and chat_users.user_id = messages.user_id;

create or replace view car_view as
    select car_listing.id_car as car_id, car_listing.id_user as user_id, car_brand.name as brand_name,
    car_model.name as model_name, car_model.production_year as year, cars.km_dirven as km
    from car_listing, cars, car_model, car_brand
    where car_listing.id_car = cars.id and cars.id_model = car_model.id and car_model.id_brand = car_model.id;
