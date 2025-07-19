import unittest
from unittest.mock import patch
from .. import prompts

class TestPrompts(unittest.TestCase):

    @patch('django_celere.prompts.questionary')
    def test_get_frontend_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "HTMX & Alpine.js"
        self.assertEqual(prompts.get_frontend_choice(), '1')

    @patch('django_celere.prompts.questionary')
    def test_get_component_library_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "DaisyUI"
        self.assertEqual(prompts.get_component_library_choice(), '1')

    @patch('django_celere.prompts.questionary')
    def test_get_database_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "PostgreSQL (Local Docker)"
        self.assertEqual(prompts.get_database_choice(), '2')

    @patch('django_celere.prompts.questionary')
    def test_get_linter_formatter_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "Black & isort (Python) + Prettier (JS/CSS)"
        self.assertEqual(prompts.get_linter_formatter_choice(), '1')

    @patch('django_celere.prompts.questionary')
    def test_get_typescript_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "TypeScript"
        self.assertEqual(prompts.get_typescript_choice(), '2')

    @patch('django_celere.prompts.questionary')
    def test_get_app_choices(self, mock_questionary):
        mock_questionary.checkbox.return_value.ask.return_value = ["Users App (with custom User model)", "Blog App"]
        self.assertEqual(prompts.get_app_choices(), ['1', '2'])

    @patch('django_celere.prompts.questionary')
    def test_get_ci_cd_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "GitLab CI/CD"
        self.assertEqual(prompts.get_ci_cd_choice(), '2')

    @patch('django_celere.prompts.questionary')
    def test_get_server_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "Uvicorn (ASGI)"
        self.assertEqual(prompts.get_server_choice(), '2')

    @patch('django_celere.prompts.questionary')
    def test_get_pre_commit_choice(self, mock_questionary):
        mock_questionary.select.return_value.ask.return_value = "Yes"
        self.assertEqual(prompts.get_pre_commit_choice(), '1')

if __name__ == '__main__':
    unittest.main()