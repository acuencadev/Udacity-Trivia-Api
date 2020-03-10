import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.db_user = os.environ.get('DB_USERNAME')
        self.db_password = os.environ.get('DB_PASSWORD')
        
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_user,
                                                  self.db_password,
                                                  'localhost:5432',
                                                  self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
            categories = [
                Category(type='Science'),
                Category(type='Art'),
                Category(type='Geography'),
                Category(type='History'),
                Category(type='Entertainment'),
                Category(type='Sports'),
            ]
            
            self.db.session.bulk_save_objects(categories)
            self.db.session.commit()
            
            questions = [
                Question(question="Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                         answer='Maya Angelou',category=4,
                         difficulty=2),
                Question(question="What boxer's original name is Cassius Clay?",
                         answer="Muhammad Ali",
                         difficulty=1,
                         category=4),
                Question(question="What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
                         answer="Apollo 13",
                         difficulty=4,
                         category=5),
                Question(question="What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
                         answer="Tom Cruise",
                         difficulty=4,
                         category=5),
                Question(question="What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
                         answer="Edward Scissorhands",
                         difficulty=3,
                         category=5),
                Question(question="Which is the only team to play in every soccer World Cup tournament?",
                         answer="Brazil",
                         difficulty=3,
                         category=6),
                Question(question="Which country won the first ever soccer World Cup in 1930?",
                         answer="Uruguay",
                         difficulty=4,
                         category=6),
                Question(question="Who invented Peanut Butter?",
                         answer="George Washington Carver",
                         difficulty=2,
                         category=4),
                Question(question="What is the largest lake in Africa?",
                         answer="Lake Victoria",
                         difficulty=2,
                         category=3),
                Question(question="In which royal palace would you find the Hall of Mirrors?",
                         answer="The Palace of Versailles",
                         difficulty=3,
                         category=3),
                Question(question="The Taj Mahal is located in which Indian city?",
                         answer="Agra",
                         difficulty=2,
                         category=3),
                Question(question="Which Dutch graphic artist–initials M C was a creator of optical illusions?",
                         answer="Escher",
                         difficulty=1,
                         category=2)
            ]
            
            self.db.session.bulk_save_objects(questions)
            self.db.session.commit()
            
        self.new_question = {
            'question': 'Who is the best?',
            'answer': 'You are!',
            'category': 1,
            'difficulty': 1
        }

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.session.query(Category).delete()
            self.db.session.query(Question).delete()
            self.db.session.execute("ALTER SEQUENCE categories_id_seq RESTART WITH 1")
            self.db.session.execute("ALTER SEQUENCE questions_id_seq RESTART WITH 1")
            self.db.session.commit()

    def test_get_all_categories_return_200_and_empty_result(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        
    def test_get_questions_without_page_returns_200(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 12)
        self.assertEqual(len(data['questions']), 10)
        
    def test_get_questions_with_page_returns_200(self):
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 12)
        self.assertEqual(len(data['questions']), 2)
        
    def test_get_questions_with_empty_page_returns_200_but_no_questions(self):
        res = self.client().get('/api/questions?page=3')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 12)
        self.assertEqual(len(data['questions']), 0)
    
    def test_delete_existing_question_returns_200(self):
        res = self.client().delete('/api/questions/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
    
    def test_delete_non_existing_question_returns_404(self):
        res = self.client().delete('/api/questions/13')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        
    def test_create_question_without_params_returns_error(self):
        res = self.client().post('/api/questions', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
    
    def test_create_question_without_param_returns_200(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_search_questions_with_matching_term_returns_list_of_questions(self):
        res = self.client().post('/api/questions/search', json={
            'searchTerm': 'What'
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 5)
        
    
    def test_search_questions_with_not_matching_term_returns_empty_list(self):
        res = self.client().post('/api/questions/search', json={
            'searchTerm': 'Parangaricutirimicuaro'
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
        
    def test_get_questions_by_not_existing_category_returns_empty_list(self):
        res = self.client().get('/api/categories/27/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
    
    def test_get_questions_by_existing_category_returns_list_of_questions(self):
        res = self.client().get('/api/categories/4/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 3)
        
    def test_get_next_question_with_params_returns_a_valid_question(self):
        form_data = {
            'previous_questions': [1, 2, 3, 4, 5],
            'quiz_category': {'type': 'Science', 'id': 4}
        }
        
        res = self.client().post('/api/quizzes', json=form_data)
                
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
    
    def test_get_next_question_without_params_returns_error(self):
        res = self.client().post('/api/quizzes', json={})
                
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()