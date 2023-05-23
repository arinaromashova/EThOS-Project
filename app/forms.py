from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_query = StringField(validators=[DataRequired()])
    number_of_results = SelectField(
        "Choose how many results you need   ?",
        choices=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    )
    submit = SubmitField("Submit")


class SubmitFeedbackForm(FlaskForm):
    user_feedback = StringField(
        "Please provide any comments on the sematic search result"
    )
    user_score = SelectField(
        "Select your score", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    submit = SubmitField("Submit your feedback and score")
