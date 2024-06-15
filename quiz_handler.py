from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router = Router()
questions = [
    {
        "name": "Какой призовой фонд на Хакатоне?",
        "answers": {
            "1": "25,000 Опционов.",
            "2": "100,000 Опционов или 10,000 LA.",
            "3": "Только бесценный опыт.",
        },
        "correct_answers": {"3"},
    },
    {
        "name": "Что от вас ожидают на хакатоне в первую очередь?",
        "answers": {
            "1": "Показать мои способности узнавать новые технологии.",
            "2": "Показать работающий сервис.",
            "3": "Продемонстрировать навыки коммуникации и командной работы.",
        },
        "correct_answers": {"2"},
    },
    {
        "name": "Что из этого является преимуществом работы в Латокен?",
        "answers": {
            "1": "Быстрый рост через решение нетривиальных задач.",
            "2": "Передовые технологии AIxWEB3.",
            "3": "Глобальный рынок, клиенты в 200+ странах",
            "4": "Возможность совмещать с другой работой и хобби",
            "5": "Самая успешная компания из СНГ в WEB3",
            "6": "Удаленная работа, но без давншифтинга",
            "7": "Оплата в твердой валюте, без привязки к банкам",
            "8": "Опционы с 'откешиванием' криптолетом",
            "9": "Комфортная среда для свободы творчества",
        },
        "correct_answers": {"1", "2", "3", "6", "8", "9"},
    },
    {
        "name": "Какое расписание Хакатона корректнее?",
        "answers": {
            "1": "Пятница: 18:00 Разбор задач. Суббота: 18:00 Демо результатов, 19-00 объявление победителей, интервью и офферы.",
            "2": "Суббота: 12:00 Презентация компании, 18:00 Презентации результатов проектов.",
        },
        "correct_answers": {"1"},
    },
    {
        "name": "Каковы признаки 'Wartime CEO' согласно крупнейшему венчурному фонду a16z?",
        "answers": {
            "1": "Сосредотачивается на общей картине и дает сотрудникам принимать детальные решения на общей картине и дает команде возможность принимать детальные решения",
            "2": "Употребляет ненормативную лексику, кричит, редко говорит спокойным тоном",
            "3": "Не терпит отклонений от плана",
            "4": "Обучает своих сотрудников для обеспечения их удовлетворенности и карьерного развития",
            "5": "Тренерует сотрудников, так чтобы им не прострелили зад на поле боя",
        },
        "correct_answers": {"2", "3", "5"},
    },
    {
        "name": "Что Латокен ждет от каждого члена команды?",
        "answers": {
            "1": "Спокойной работы без излишнего стресса",
            "2": "Вникания в блокеры вне основного стека, чтобы довести свою задачу до прода",
            "3": "Тестирование продукта",
            "4": "Субординацию, и не вмешательство чужие дела",
            "5": "Вежливость и корректность в коммуникации",
            "6": "Измерение результатов",
            "7": "Демонстрацию результатов в проде каждую неделю",
        },
        "correct_answers": {"2", "3", "4", "6", "7"}
    },
    {
        "name": "Представьте вы на выпускном экзамене. Ваш сосед слева просит вас передать ответы от соседа справа. Вы поможете??",
        "answers": {
            "1": "Да",
            "2": "Да, но если преподаватель точно не увидит",
            "3": "Нет",
            "4": "Нет, если мне не дадут посмотреть эти ответы",
            "5": "Нет, если это может мне повредить",
        },
        "correct_answers": {"3"}
    },
    {
        "name": "Кирпич весит килограмм и еще пол-кирпича. Сколько весит кирпич?",
        "answers": {
            "1": "1 КГ",
            "2": "1.5 КГ",
            "3": "2 КГ",
            "4": "3 КГ",
        },
        "correct_answers": {"3"}
    },
]

users_storage = {
    "answers_count": len(questions)
}


class Form(StatesGroup):
    first_question = State()
    two_question = State()
    three_question = State()
    four_question = State()
    five_question = State()
    six_question = State()
    seven_question = State()
    eight_question = State()


@router.message(Command('quiz'), F.chat.type == "private")
async def start_quiz(message: Message, state: FSMContext):
    await message.answer("Quiz starting. Ответы дайте в таком формате: 1 2 3.")
    if message.from_user.id not in users_storage:
        users_storage[message.from_user.id] = 0
        await state.set_state(Form.first_question)
        question = questions[0]["name"]
        answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[0]["answers"].items()])
        await message.answer(text=question + "\n\n" + answers_str)

    else:
        await message.answer(
            f"Already! Tour points: {str(users_storage[message.from_user.id])}/{users_storage["answers_count"]}"
        )


@router.message(Form.first_question)
async def first_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[0]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.two_question)
    question = questions[1]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[1]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)


@router.message(Form.two_question)
async def two_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[1]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.three_question)
    question = questions[1]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[1]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)


@router.message(Form.three_question)
async def three_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[2]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.four_question)
    question = questions[2]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[2]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)


@router.message(Form.four_question)
async def four_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[3]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.five_question)
    question = questions[3]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[3]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)


@router.message(Form.five_question)
async def five_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[4]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.six_question)
    question = questions[4]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[4]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)


@router.message(Form.six_question)
async def six_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[5]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.seven_question)
    question = questions[5]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[5]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)

@router.message(Form.seven_question)
async def seven_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[6]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.set_state(Form.eight_question)
    question = questions[6]["name"]
    answers_str = "\n".join([f"{num}. {ans}" for num, ans in questions[6]["answers"].items()])
    await message.answer(text=question + "\n\n" + answers_str)


@router.message(Form.eight_question)
async def eight_question(message: Message, state: FSMContext):
    answers_user = set(message.text.split(' '))
    if questions[7]["correct_answers"] == answers_user:
        users_storage[message.from_user.id] += 1

    await state.clear()
    await message.answer("Quiz completed! Here are your results:")
    await message.answer(
        f"Correct answers: {users_storage[message.from_user.id]} out of {users_storage['answers_count']}"
    )
