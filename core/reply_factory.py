
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
    
    question_data = PYTHON_QUESTION_LIST[current_question_id]
    correct_answer = question_data['correct_answer']
    if answer == correct_answer:
        if 'answer' not in session:
            session['answers'] = {}
        session['answers'][currect_question_id] = answer

    '''
    Validates and stores the answer for the current question to django session.
    '''
    return True, ""
else:
error_message = "Incorrect answer. Please try again."
return False , error_message

def get_next_question(current_question_id):
    if current_question_id < len(PYTHON_QUESTION_LIST)-1:
        next_question_id = current_question_id + 1 
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
        return next_question,next_question_id
    else:
        return None , current_question_id
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    return "dummy question", -1


def generate_final_response(session):
    if 'answer' not in session :
        return "No abswer recorded. Please complete the quiz"
    user_answer = session['answer']

    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    for question_id, user_answer in user_answers.items():
        correct_answer = PYTHON_QUESTION_LIST[question_id]['correct_answer']
        if user_answer == correct_answer:
            correct_answers += 1

    # Calculate score percentage
    score_percentage = (correct_answers / total_questions) * 100

    # Generate final response message
    final_response = f"You have completed the quiz.\n"
    final_response += f"Total questions: {total_questions}\n"
    final_response += f"Correct answers: {correct_answers}\n"
    final_response += f"Score: {score_percentage:.2f}%"

    return final_response
    
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    return "dummy result"
