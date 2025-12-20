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
    /* password= manager2 */
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

-- Coffee Shops
INSERT INTO
    coffee_shops (name, address, manager_id)
VALUES
    (
        'FLTR - Peterhof',
        'Санкт-Петербург, ул. Аврова, 36',
        1
    ),
    (
        'FLTR - Nekrasov',
        'Санкт-Петербург, ул. Некрасова, 23',
        2
    ),
    (
        'FLTR - Nevsky',
        'Санкт-Петербург, Невский пр., 25',
        3
    ),
    (
        'FLTR - Strelna',
        'Санкт-Петербург, Ново-Нарвское шоссе, 12',
        4
    ),
    (
        'FLTR - Kupchino',
        'Санкт-Петербург, ул. Ярослава Гашека, 4',
        5
    );

-- -- Administrator
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
        '$2b$12$C94zOImJezPePLsEtGdKoOVy4i/OOGeMi.gKx2TunM8Lq52D.2hcW', -- 'hash_pechorin_xyz',
        'Григорий',
        'customer',
        NOW ()
    ),
    (
        'raskolnikov_topor@coffeemail.com',
        '$2b$12$vZeGQeZfTRHzyV55Ew8jquUUURypR0dQGl7ksgJWqiCtdx5Xy/dwm', -- 'raskolnikov_123', 
        'Родион',
        'customer',
        NOW ()
    ),
    (
        'bazarov_nigilist@coffeemail.com',
        '$2b$12$J2Y3pePeqkvzof01zQ2uNexPSF1nOiDBJdGlqoYYHTyj1hXVnyJli', -- 'bazarov_456',
        'Евгений',
        'customer',
        NOW ()
    ),
    (
        'oblomov_divan@coffeemail.com',
        '$2b$12$ife0xNTBmoawat0DToKL5OIJHuXnZ/eknHPcAWdCvztvBnm6ObFoq', --'oblomov_777',
        'Илья',
        'customer',
        NOW ()
    ),
    (
        'chichikov_mertvie@coffeemail.com',
        '$2b$12$YW5JPpkmkOA4eqroAYZ/N.QwZ.Ya5n3e3kJJEvVsrgBEtVig8kgz.', -- 'chichikov_888',
        'Павел',
        'customer',
        NOW ()
    ),
    (
        'karamazov_brat@coffeemail.com',
        '$2b$12$5B62n0/gImjGCD.dOQc2XOaw.cvyLGh6j5NoyCbtZxGH1b1oEBLZu', -- 'karamazov_trinity',
        'Алексей',
        'customer',
        NOW ()
    ),
    (
        'sofya_gore@coffeemail.com',
        '$2b$12$7P1fBbJ7V9MLTPPQtQMh3euzucediKRdQYEPwV9SDSNf/2QcW0zi2', -- 'sofya_smekh',
        'Софья',
        'customer',
        NOW ()
    ),
    (
        'masha_kapitanskaya@coffeemail.com',
        '$2b$12$CGU5vy5rgJ3P6sksvcBQ/.QX/fGAKXMCc3ac4GhayPAVIXllarJ0e', -- 'masha_krepost',
        'Маша',
        'customer',
        NOW ()
    ),
    (
        'grinev_bunt@coffeemail.com',
        '$2b$12$omJMuGZG4mOr3hbpV7kmQeewxFHZp3QPkOyp/.kG294wz2casHLs.', -- 'grinev_pugachev'
        'Пётр',
        'customer',
        NOW ()
    ),
    (
        'lermontov_poet@coffeemail.com',
        '$2b$12$OWNjwHIqfYIFNV9dW2O36OOtm3WHSbuJn9A/ArZsO24UpCt2syWKO', -- 'lermontov_stih'
        'Михаил',
        'customer',
        NOW ()
    ),
    (
        'gogol_nos@coffeemail.com',
        '$2b$12$OZA2QmXOHR/2Ri5.K33/I.UYDLZGWWy3CI8Pn0MXKQXkbfAere.Q.', -- 'gogol_strashno'
        'Николай',
        'customer',
        NOW ()
    ),
    (
        'tolstoy_voyna@coffeemail.com',
        '$2b$12$.NBPIDue8qcIKFOE2em6lehJzRLN3eKKo.uruOniJ0x87XBkRN.Fy', -- 'tolstoy_mir'
        'Лев',
        'customer',
        NOW ()
    ),
    (
        'chehov_vishnya@coffeemail.com',
        '$2b$12$nYzx2BMWZHCTUSlt8rcvJO6KaORCBTpTZylDGSdXF0dZz2goB.HW2', -- 'chehov_sad'
        'Антон',
        'customer',
        NOW ()
    ),
    (
        'goncharov_oblom@coffeemail.com',
        '$2b$12$rtVq6NG2SNf6kzp76cYm9.89o6h8r.Rv/DkZh9/ggBx33sKMipdfW', -- 'goncharov_son'
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'dostoevsky_prestup@coffeemail.com',
        '$2b$12$i/yqv65nfnvIFVJVi4NkCu9gjnqwIdg4.b98wAgNoMrkmjP/mqX7.', -- 'dostoevsky_nakaz'
        'Фёдор',
        'customer',
        NOW ()
    ),
    (
        'pushkin_evgeny@coffeemail.com',
        '$2b$12$fLgLEwFfL1D29wdS2k.osubyVafW1R5WjvBLqFV.fXa7FYuyhGh0G', -- 'pushkin_roman'
        'Александр',
        'customer',
        NOW ()
    ),
    (
        'griboedov_gore@coffeemail.com',
        '$2b$12$h9U6I8VJh33htY1gYdCYGOMmntQaP1RP1jVxkDp/zDA.D1qRrCQjq', -- 'griboedov_um'
        'Александр',
        'customer',
        NOW ()
    ),
    (
        'saltykov_shchedrin_guber@coffeemail.com',
        '$2b$12$srh/il7KW86osCm4Wq7ST.l0xEY2LZKXKWQTe9xJYLsQbQnDGyqHC', -- 'saltykov_satira'
        'Михаил',
        'customer',
        NOW ()
    ),
    (
        'leskov_levsha@coffeemail.com',
        '$2b$12$vkWR1OVxbM34gpjnBnMABeN2Jg0uoNmwaZG0sZ6WVSMxfS.OJOh9C', -- 'leskov_podkovka'
        'Николай',
        'customer',
        NOW ()
    ),
    (
        'blok_nochi@coffeemail.com',
        '$2b$12$Qiqd1f5V84HrgnrTLTaNduIZ07jT8wLlVw0dPJAxfQCM9UBGuhQO6', -- 'blok_stihi'
        'Александр',
        'customer',
        NOW ()
    ),
    (
        'esenin_rus@coffeemail.com',
        '$2b$12$Zv.CvRETvWBAp2VPiuaZv.8kVOaKVxvVYuf1UGlwY0gsiQq7r8AZy', -- 'esenin_bereza'
        'Сергей',
        'customer',
        NOW ()
    ),
    (
        'mayakovsky_lestnica@coffeemail.com',
        '$2b$12$rGp25KZRELaH9ck8ZuDJ5.WYU5FllIhgr8ugfABKlNg4iLKj5Wj2S', -- 'mayakovsky_krik'
        'Владимир',
        'customer',
        NOW ()
    ),
    (
        'bunin_temnie@coffeemail.com',
        '$2b$12$BcFpRUg5xSsDKrN9QUZXoux1alsXgBABNWjmNjlWJeO6AXkkCXMSO', -- 'bunin_alye'
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'sholohov_tihii@coffeemail.com',
        '$2b$12$uXB.y63gl1uFqhOlgeyGa.iCVahnqGQPawJLnsMaubXK1/fTANOQe', -- 'sholohov_don'
        'Михаил',
        'customer',
        NOW ()
    ),
    (
        'paustovsky_telefon@coffeemail.com',
        '$2b$12$mJU6iNOS65hTlXfbSFoLzOdVKY0x3xHtD8UQnDOY960P1TZShascO', -- 'paustovsky_rasskaz'
        'Константин',
        'customer',
        NOW ()
    ),
    (
        'turgenev_otci@coffeemail.com',
        '$2b$12$tUr2Hue5TJJqWGGwOQSdcehS3c69WNxYsN1vYSwi48i.R/iScFHWK', -- 'turgenev_deti'
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'goncharov_oblojka@coffeemail.com',
        '$2b$12$Qp16iLPIOLSjiAXEMsBh2.IOsIe5IrY1lkQvJyAHardwZMLdPRIQi', -- 'goncharov_roman'
        'Иван',
        'customer',
        NOW ()
    ),
    (
        'korolenko_deti@coffeemail.com',
        '$2b$12$aJXpz7PfW3guH38A9Um61O1mhPZKmg53Y4PoCrk.hEfiiwkTkfOxa', -- 'korolenko_sumrak'
        'Владимир',
        'customer',
        NOW ()
    );

-- Products
INSERT INTO
    products (
        name,
        description,
        image_url,
        price,
        product_type
    )
VALUES
    (
        'Эспрессо',
        'Насыщенный кофейный напиток',
        '/static/images/products/coffee/espresso.png',
        180,
        'coffee'
    ),
    (
        'Капучино',
        'Кофейный напиток на основе эспрессо с добавлением вспененного молока',
        '/static/images/products/coffee/capuchino.png',
        280,
        'coffee'
    ),
    (
        'Латте',
        'Кофе на основе эспрессо с большим количеством молока',
        '/static/images/products/coffee/latte.png',
        290,
        'coffee'
    ),
    (
        'Флэт уайт',
        'Кофе на основе двойного эспрессо и молока',
        '/static/images/products/coffee/capuchino.png',
        310,
        'coffee'
    ),
    (
        'Айс латте',
        'Охлаждённый латте со льдом и молочной пеной',
        '/static/images/products/coffee/ice_latte.png',
        330,
        'coffee'
    ),
    (
        'Фильтр-кофе',
        'Чёрный фильтр-кофе с насыщенным вкусом и ароматом',
        '/static/images/products/coffee/filter.png',
        220,
        'coffee'
    ),
    (
        'Чай Матча латте',
        'Напиток на основе зелёного японского чая матча с молоком',
        '/static/images/products/non_coffee/matcha.png',
        320,
        'non_coffee'
    ),
    (
        'Чай Матча латте',
        'Напиток на основе зелёного японского чая матча с молоком со льдом',
        '/static/images/products/non_coffee/ice_matcha.png',
        320,
        'non_coffee'
    ),
    (
        'Какао',
        'Натуральный какао с молоком',
        '/static/images/products/non_coffee/cacao.png',
        310,
        'non_coffee'
    ),
    (
        'Горячий шоколад',
        'Густой шоколад с молочной пеной',
        '/static/images/products/non_coffee/hotchoc.png',
        330,
        'non_coffee'
    ),
    (
        'Апельсиновый фреш',
        'Свежевыжатый сок из сочных апельсинов',
        '/static/images/products/non_coffee/orangejuice.png',
        250,
        'non_coffee'
    ),
    (
        'Бамбл-кофе',
        'Эспрессо с добавлением апельсинового фреша',
        '/static/images/products/coffee/bumble.png',
        300,
        'coffee'
    ),
    (
        'Чай эрл грей',
        'Чёрный чай с бергамотом',
        '/static/images/products/non_coffee/earl.png',
        240,
        'non_coffee'
    ),
    (
        'Клубничный матча-латте',
        'Чай матча-латте с клубничным пюре',
        '/static/images/products/non_coffee/strawberry_matcha.png',
        380,
        'non_coffee'
    ),
    (
        'Манго матча-латте',
        'Чай матча-латте с манговым пюре',
        '/static/images/products/non_coffee/mango_matcha.png',
        380,
        'non_coffee'
    ),
    (
        'Тыквенный пряный латте',
        'Кофейный напиток с тыквенным пюре и пряными спецями',
        '/static/images/products/coffee/pumpkin.png',
        350,
        'coffee'
    );




COPY orders(order_id, user_id, shop_id, total_amount,created_at ) 
FROM '/app/add_data/orders.csv'
DELIMITER ','
CSV HEADER;

COPY order_items(order_item_id, order_id, product_id, unit_price, quantity)
FROM '/app/add_data/order_items.csv'
DELIMITER ','
CSV HEADER;

COPY attribute_types(attribute_name ) 
FROM '/app/add_data/attribute_types.csv'
DELIMITER ','
CSV HEADER;

COPY product_attribute_options(attribute_type_id,value,extra_price)
FROM '/app/add_data/product_attribute_options.csv'
DELIMITER ','
CSV HEADER;

COPY product_attributes(product_id,option_id)
FROM '/app/add_data/product_attributes.csv'
DELIMITER ','
CSV HEADER;

COPY shop_menu(shop_id,product_id,is_available)
FROM '/app/add_data/shop_menu.csv'
DELIMITER ','
CSV HEADER;


SELECT setval('orders_order_id_seq', COALESCE((SELECT MAX(order_id) FROM orders), 0) + 1, false);
SELECT setval('order_items_order_item_id_seq', COALESCE((SELECT MAX(order_item_id) FROM order_items), 0) + 1, false);
SELECT setval('attribute_types_attribute_type_id_seq', COALESCE((SELECT MAX(attribute_type_id) FROM attribute_types), 0) + 1, false);
SELECT setval('product_attribute_options_option_id_seq', COALESCE((SELECT MAX(option_id) FROM product_attribute_options), 0) + 1, false);
