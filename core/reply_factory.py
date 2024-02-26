
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # print(f"python question List: {PYTHON_QUESTION_LIST}")
    # print(f"bot welcome message:{BOT_WELCOME_MESSAGE}")

    print(PYTHON_QUESTION_LIST[current_question_id])
    correct_ans = PYTHON_QUESTION_LIST[current_question_id]['answer']

    if answer == correct_ans:
        session['answers'][current_question_id] = answer
        return True, ""
    
    else:
        return False, "Your answer is incorrect. please try again"


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
        return next_question, next_question_id

    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_count = 0

    for qustion_id, qustion_data in enumerate(PYTHON_QUESTION_LIST):

        correct_ans = qustion_data['answer']

        user_ans = session.get('answers',{}).get(qustion_id)

        if user_ans == correct_ans:
            correct_count += 1

    score = (correct_count/total_questions)*100

    response = f"you have completed the quiz, Your score is {score}%"\
                    f"({correct_count} out of {total_questions} correct)."

    return response
