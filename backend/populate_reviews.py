import requests
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

usernames = [
    "AlexeyPetrov",
    "DmitrySokolov",
    "SergeyKuznetsov",
    "AndreyIvanov",
    "NikolaySmirnov",
    "VladimirKiselev",
    "MikhailPopov",
    "ArtemMorozov",
    "RomanVolkov",
    "EgorNikolaev",
    "KonstantinLebedev",
    "IlyaOrlov",
    "PavelVasiliev",
    "TimurFedorov",
    "YuriGavrilov",
    "KirillZaitsev",
    "OlegSemenov",
    "VictorMakarov",
    "MaximAndreev",
    "AntonAlexandrov",
]

reviews = {
    "Очень красивая работа, но не для всех.": 4.7,
    "Отличная режиссура, рекомендую к просмотру.": 4.6,
    "Фильм не без недостатков, но смотреть можно.": 4.0,
    "Не впечатлило, слишком предсказуемо.": 4.9,
    "Понравилась игра актёров, но сюжет банальный.": 4.9,
    "Очень атмосферный, но сюжет не цепляет.": 4.4,
    "Мне понравилось, особенно концовка!": 3.8,
    "Достойный фильм, но не шедевр.": 4.8,
    "Фильм хороший, но второй раз не посмотрю.": 3.4,
    "Очень понравилась игра главного актёра.": 4.6,
    "Слишком много клише, но посмотреть можно.": 5.0,
    "Хороший фильм, но немного затянут.": 4.6,
    "Актёры справились хорошо, но сценарий подкачал.": 4.8,
    "Неплохое кино, но пересматривать точно не буду.": 4.3,
    "Не хватило глубины в сюжете.": 4.3,
    "Фильм довольно хороший, но не идеальный.": 3.1,
    "Слишком затянуто, но в целом нормально.": 4.0,
    "Просто отличный фильм, рекомендую всем!": 4.7,
    "Оставил много вопросов, но зацепил!": 4.1,
    "Актёры молодцы, но сам фильм не зашёл.": 3.7,
    "Оставляет смешанные чувства, 50/50.": 4.5,
    "Рекомендую, хотя есть свои недостатки.": 4.0,
    "Много диалогов, но общая задумка понравилась.": 3.1,
    "Было бы лучше, если бы сократили длительность.": 4.3,
    "Фильм с глубоким смыслом, мне понравилось.": 3.4,
    "Много затянутых сцен, но общая идея интересная.": 4.9,
    "Тяжеловатый для восприятия, но качественный.": 3.3,
    "Лёгкий фильм для одного просмотра.": 4.5,
    "Сценарий слабоват, но визуал на высоте.": 3.7,
    "Нормальный фильм, но есть куда расти.": 4.7,
    "Отличный фильм для вечернего просмотра.": 3.6,
    "Красиво снято, но безэмоционально.": 3.0,
}


base_url = "http://localhost:8080"
default_password = os.getenv("DEFAULT_USER_PASSWORD")

usernames_tokens = {}

random.seed(time.time())

# fake users authentication
for username in usernames:
    auth_json = {"username": username, "password": default_password}
    print(f"Authenticating {username}")
    auth_req = requests.post(base_url + "/api/token", json=auth_json)
    if auth_req.status_code != 202:
        print(f"\tCreating user {username}")
        requests.post(base_url + "/api/user", json=auth_json)
    auth_req = requests.post(base_url + "/api/token", json=auth_json)
    if auth_req.status_code == 202:
        print(f"User {username} authenticated")
        usernames_tokens.update({username: auth_req.json()})
    print()
print()

# getting movies
print("Getting movies list")
movies = requests.get(base_url + "/api/movie").json()
print()

# making reviews
for movie in movies:
    movie_title = movie["title"]
    movie_id = movie["id"]
    print(f"Processing movie {movie_title} : {movie_id}")
    usernames_to_leave_review = random.sample(usernames, 10)
    print(f"Users selected to leave review: {usernames_to_leave_review}")
    for username in usernames_to_leave_review:
        user_token = usernames_tokens[username]
        review_content, review_rating = random.choice(list(reviews.items()))
        print(f"Selected review {review_content} with rating {review_rating}")
        review_req = requests.post(
            base_url + f"/api/movie/{movie_id}/review",
            json={"content": review_content, "rating": review_rating},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        if review_req.status_code == 201:
            print(f"User {username} left review for movie {movie_id}")
    print()
