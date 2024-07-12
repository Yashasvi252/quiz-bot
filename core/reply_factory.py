
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
    # Retrieve question data based on current_question_id
    question_data = PYTHON_QUESTION_LIST[current_question_id]

    # Retrieve correct answer from question data
    correct_answer = question_data['correct_answer']

    # Validate user's answer
    if answer == correct_answer:
        # Store answer in session
        if 'answers' not in session:
            session['answers'] = {}
        session['answers'][current_question_id] = answer
        return True, ""
    else:
        # Return error message if answer is incorrect
        error_message = "Incorrect answer. Please try again."
        return False, error_message


def get_next_question(current_question_id):
    # Ensure current_question_id is within bounds
    if current_question_id < len(PYTHON_QUESTION_LIST) - 1:
        # Increment current_question_id to fetch next question
        next_question_id = current_question_id + 1
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
        return next_question, next_question_id
    else:
        # Return None if all questions have been asked
        return None, current_question_id



    return "dummy result"
