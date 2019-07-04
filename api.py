from stackapi import StackAPI

questionKeyword = 'how to replace fragment on activity'
SITE = StackAPI('stackoverflow')
SITE.page_size = 1


class Answer:
    def __init__(self, content, question_url):
        self.content = content
        self.question_url = question_url

    def __str__(self):
        return self.content

    def __repr__(self):
        return f'<Answer {self}>'


def get_answers():

    question_urls = {}

    def is_valid_question(question):
        return question['is_answered']

    def process_and_get_question(question):
        question_urls[question['question_id']] = question['link']
        return question

    def get_questions():
        questions = SITE.fetch('search/advanced', q=questionKeyword, sort='votes')['items']
        return [process_and_get_question(question) for question in questions if is_valid_question(question)]

    def is_valid_answer(answer):
        return answer['is_accepted']

    def fetch_answers(question_ids):
        return SITE.fetch('questions/{ids}/answers', ids=question_ids, sort='votes')['items']

    def get_answers_metadata():
        question_ids = [question['question_id'] for question in get_questions()]
        return [answer for answer in fetch_answers(question_ids) if is_valid_answer(answer)]

    def create_answer(answer):
        return Answer(answer['body'], question_urls[answer['question_id']])

    answers_ids = [answer['answer_id'] for answer in get_answers_metadata()]
    return [create_answer(answer) for answer in SITE.fetch('answers', ids=answers_ids, filter='withBody')['items']]

