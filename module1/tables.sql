create table if not exists users
(
    id            serial primary key,
    chat_id       bigint     not null unique,
    first_name    text    not null,
    last_name     text,
    username      text,
    is_bot        boolean not null,
    language_code text default 'fr',
    password      text,
    role          text default 'client',
    constraint check_role check (role in ('client', 'mecanicien'))
);

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

commit;
