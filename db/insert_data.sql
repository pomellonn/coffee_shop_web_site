-- Coffee Shops
INSERT INTO
    coffee_shops (name, address, manager_id)
VALUES
    (
        'gotcha - Peterhof',
        'Санкт-Петербург, ул. Аврова, 36',
        1
    ),
    (
        'gotcha - Nekrasov',
        'Санкт-Петербург, ул. Некрасова, 23',
        2
    ),
    (
        'gotcha - Nevsky',
        'Санкт-Петербург, Невский пр., 25',
        3
    ),
    (
        'gotcha - Strelna',
        'Санкт-Петербург, Ново-Нарвское шоссе, 12',
        4
    ),
    (
        'gotcha - Kupchino',
        'Санкт-Петербург, ул. Ярослава Гашека, 4',
        3
    );

-- Administrator
INSERT INTO
    users (email, password_hash, name, role)
VALUES
    /* password= adminmel */
    (
        'melania@coffee.com',
        '$2b$12$.HHPSjIAwskZRuZ8D.LyI.CvWb8HRYe9M0Ko/kNjyjwUSDWm0OZp6',
        'Мелания',
        'admin'
    ),
    /* password= adminks */
    (
        'ksenia@coffee.com',
        '$2b$12$n06aocCZvJCfGS5f40.yvepVIgToix4VPUmCVGxrqxBG5f1hrN.mK',
        'Ксения',
        'admin'
    );

-- Managers
INSERT INTO
    users (email, password_hash, name, role)
VALUES
    /* password= manager1 */
    (
        'manager_rostova@coffee.com',
        '$2b$12$Pfs/PhK5t2ip5MYfFnBVNOcqiUamDUPRTH2At4BMrlu5KNRpUG6IG',
        'Наталья Ростова',
        'manager'
    ),
    /* password= manager1 */
    (
        'manager_karenina@coffee.com',
        '$2b$12$/crRPqcwkP/tNK.4NUMM0OpCdW2sYz57aJ2NIYA94QDEYnpdqC5M.',
        'Анна Каренина',
        'manager'
    ),
    /* password= manager3 */
    (
        'manager_bolkonskiy@coffee.com',
        '$2b$12$gqkM2Fi5uAVrotiDXjlcwunyunRF4OAFjyXbnLXn2SGoNlDL9i3zu',
        'Андрей Болконский',
        'manager'
    ),
    /* password= manager4 */
    (
        'manager_loskutnikova@coffee.com',
        '$2b$12$$2b$12$hritGeeDgOYeLjXaALp30uVpNWm3JnFr/WgTxuVEcgx3sKp4eO.lK',
        'София Лоскутникова',
        'manager'
    ),
    /* password= manager5 */
    (
        'manager_strugatsky@coffee.com',
        '$2b$12$yBKKtUPl9aEx0dPdoHeq2eNANBbrofGMeKIU19BItDM.U63SldvgS',
        'Аркадий Стругацкий',
        'manager'
    );

-- Customers
INSERT INTO
    users (email, password_hash, name, role, created_at)
VALUES
    (
        'onegin_1820@coffeemail.com',
        '$2b$12$dudGap0GUkt4H.5oM6a4ru7cyWr6JyP2jA8TNNiALp0NfSODEyo/O', -- 'hash_onegin_abc', 
        'Евгений',
        'customer',
        NOW ()
    ),
    (
        'pechorin_gore@coffeemail.com',
        '$2b$12$C94zOImJezPePLsEtGdKoOVy4i/OOGeMi.gKx2TunM8Lq52D.2hcW' -- 'hash_pechorin_xyz',
        'Григорий',
        'customer',
        NOW ()
    ),
    (
        'raskolnikov_topor@coffeemail.com',
        '$2b$12$vZeGQeZfTRHzyV55Ew8jquUUURypR0dQGl7ksgJWqiCtdx5Xy/dwm' -- 'raskolnikov_123', 
        'Родион',
        'customer',
        NOW ()
    ),
    (
        'bazarov_nigilist@coffeemail.com',
        '$2b$12$J2Y3pePeqkvzof01zQ2uNexPSF1nOiDBJdGlqoYYHTyj1hXVnyJli' -- 'bazarov_456',
        'Евгений',
        'customer',
        NOW ()
    ),
    (
        'oblomov_divan@coffeemail.com',
        '$2b$12$ife0xNTBmoawat0DToKL5OIJHuXnZ/eknHPcAWdCvztvBnm6ObFoq' --'oblomov_777',
        'Илья',
        'customer',
        NOW ()
    ),
    (
        'chichikov_mertvie@coffeemail.com',
        '$2b$12$YW5JPpkmkOA4eqroAYZ/N.QwZ.Ya5n3e3kJJEvVsrgBEtVig8kgz.' -- 'chichikov_888',
        'Павел',
        'customer',
        NOW ()
    ),
    (
        'karamazov_brat@coffeemail.com',
        '$2b$12$5B62n0/gImjGCD.dOQc2XOaw.cvyLGh6j5NoyCbtZxGH1b1oEBLZu' -- 'karamazov_trinity',
        'Алексей',
        'customer',
        NOW ()
    ),
    (
        'sofya_gore@coffeemail.com',
        '$2b$12$7P1fBbJ7V9MLTPPQtQMh3euzucediKRdQYEPwV9SDSNf/2QcW0zi2' -- 'sofya_smekh',
        'Софья',
        'customer',
        NOW ()
    ),
    (
        'masha_kapitanskaya@coffeemail.com',
        '$2b$12$CGU5vy5rgJ3P6sksvcBQ/.QX/fGAKXMCc3ac4GhayPAVIXllarJ0e' -- 'masha_krepost',
        'Маша',
        'customer',
        NOW ()
    ),
    (
        'grinev_bunt@coffeemail.com',
        'hash_grinev_pugachev',
        'Пётр',
        'customer',
        NOW ()
    ),
    (
        'lermontov_poet@coffeemail.com',
        'hash_lermontov_stih',
        'Михаил',
        'customer',
        NOW ()
    ),
    (
        'gogol_nos@coffeemail.com',
        'hash_gogol_strashno',
        'Николай',
        'customer',
        NOW ()
    ),
    (
        'tolstoy_voyna@coffeemail.com',
        'hash_tolstoy_mir',
        'Лев',
        'customer',
        NOW ()
    ),
    (
        'chehov_vishnya@coffeemail.com',
        'hash_chehov_sad',
        'Антон',
        'customer',
        NOW ()
    ),
    (
        'goncharov_oblom@coffeemail.com',
        'hash_goncharov_son',
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'dostoevsky_prestup@coffeemail.com',
        'hash_dostoevsky_nakaz',
        'Фёдор',
        'customer',
        NOW ()
    ),
    (
        'pushkin_evgeny@coffeemail.com',
        'hash_pushkin_roman',
        'Александр',
        'customer',
        NOW ()
    ),
    (
        'griboedov_gore@coffeemail.com',
        'hash_griboedov_um',
        'Александр',
        'customer',
        NOW ()
    ),
    (
        'saltykov_shchedrin_guber@coffeemail.com',
        'hash_saltykov_satira',
        'Михаил',
        'customer',
        NOW ()
    ),
    (
        'leskov_levsha@coffeemail.com',
        'hash_leskov_podkovka',
        'Николай',
        'customer',
        NOW ()
    ),
    (
        'blok_nochi@coffeemail.com',
        'hash_blok_stihi',
        'Александр',
        'customer',
        NOW ()
    ),
    (
        'esenin_rus@coffeemail.com',
        'hash_esenin_bereza',
        'Сергей',
        'customer',
        NOW ()
    ),
    (
        'mayakovsky_lestnica@coffeemail.com',
        'hash_mayakovsky_krik',
        'Владимир',
        'customer',
        NOW ()
    ),
    (
        'bunin_temnie@coffeemail.com',
        'hash_bunin_alye',
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'sholohov_tihii@coffeemail.com',
        'hash_sholohov_don',
        'Михаил',
        'customer',
        NOW ()
    ),
    (
        'paustovsky_telefon@coffeemail.com',
        'hash_paustovsky_rasskaz',
        'Константин',
        'customer',
        NOW ()
    ),
    (
        'turgenev_otci@coffeemail.com',
        'hash_turgenev_deti',
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'goncharov_oblojka@coffeemail.com',
        'hash_goncharov_roman',
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'korolenko_deti@coffeemail.com',
        'hash_korolenko_sumrak',
        'Владимир',
        'customer',
        NOW ()
    );

-- Products
INSERT INTO
    products (name, description, image_url, price, volume, product_type)
VALUES
    (
        'Эспрессо',
        'Насыщенный кофейный напиток',
        '',
        180,
        40,
        'coffee'
    ),
    (
        'Двойной капучино',
        'Кофейный напиток на основе эспрессо с добавлением вспененного молока',
        '',
        350,
        350,
        'coffee'
    ),
    (
        'Капучино',
        'Кофейный напиток на основе эспрессо с добавлением вспененного молока',
        '',
        280,
        250,
        'coffee'
    ),
    (
        'Латте',
        'Кофе на основе эспрессо с большим количеством молока',
        '',
        290,
        350,
        'coffee'
    ),
    (
        'Флэт уайт',
        'Кофе на основе двойного эспрессо и молока',
        '',
        310,
        180,
        'coffee'
    ),
    (
        'Айс латте',
        'Охлаждённый латте со льдом и молочной пеной',
        '',
        330,
        400,
        'coffee'
    ),
    (
        'Фильтр-кофе',
        'Чёрный фильтр-кофе с насыщенным вкусом и ароматом',
        '',
        220,
        300,
        'coffee'
    ),
    (
        'Чай Матча латте',
        'Напиток на основе зелёного японского чая матча с молоком',
        '',
        320,
        300,
        'non_coffee'
    ),
    (
        'Имбирный чай',
        'Горячий чай с имбирём, лимоном и мёдом',
        '',
        270,
        300,
        'non_coffee'
    ),
    (
        'Какао',
        'Натуральный какао с молоком',
        '',
        310,
        350,
        'non_coffee'
    ),
    (
        'Горячий шоколад',
        'Густой шоколад с молочной пеной',
        '',
        330,
        350,
        'non_coffee'
    ),
    (
        'Апельсиновый фреш',
        'Свежевыжатый сок из сочных апельсинов',
        '',
        250,
        250,
        'non_coffee'
    ),
    (
        'Бамбл-кофе',
        'Эспрессо с добавлением апельсинового фреша',
        '',
        300,
        350,
        'coffee'
    ),
    (
        'Чай эрл грей',
        'Чёрный чай с бергамотом',
        '',
        240,
        300,
        'non_coffee'
    ),
    (
        'Тыквенный латте',
        'Пряный латте с тыквенным сиропом и корицей',
        '',
        380,
        350,
        'coffee'
    );