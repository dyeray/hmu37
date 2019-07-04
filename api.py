import json
from stackapi import StackAPI


class StackOverflowApi:

    def __init__(self, page_size=1):
        self.SITE = StackAPI('stackoverflow')
        self.SITE.page_size = page_size

    def get_answers(self, question_keyword):

        question_urls = {}

        def is_valid_question(question):
            return question['is_answered']

        def process_and_get_question(question):
            question_urls[question['question_id']] = question['link']
            return question

        def get_questions():
            questions = self.SITE.fetch('search/advanced', q=question_keyword, sort='votes')['items']
            return [process_and_get_question(question) for question in questions if is_valid_question(question)]

        def is_valid_answer(answer):
            return answer['is_accepted']

        def fetch_answers(question_ids):
            return self.SITE.fetch('questions/{ids}/answers', ids=question_ids, sort='votes')['items']

        def get_answers_metadata():
            question_ids = [question['question_id'] for question in get_questions()]
            return [answer for answer in fetch_answers(question_ids) if is_valid_answer(answer)]

        def create_answer(answer):
            return {
                'content': answer['body'],
                'question_url': question_urls[answer['question_id']],
            }

        def get_answer_bodies(answer_ids):
            return self.SITE.fetch('answers', ids=answer_ids, filter='withBody')['items']

        answers_ids = [answer['answer_id'] for answer in get_answers_metadata()]
        return json.dumps([create_answer(answer) for answer in get_answer_bodies(answers_ids)])
