from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, IntegerField, DateField, DateTimeField, FloatField
from wtforms import validators
from app.models import User

all_users = User.query.with_entities(User.name).all()


class AddUser(FlaskForm):
    name = StringField('name', validators=[validators.length(min=3, max=100), validators.DataRequired()])
    gender = RadioField('gender', choices = ['male', 'female'])
    salary = IntegerField(validators=[validators.NumberRange(min=0), validators.DataRequired()])
    date_of_birth = DateField(format='%Y-%m-%d', validators=[validators.DataRequired()])



# class AddClaim(FlaskForm):
#     user = StringField('user', validators=[validators.length(min=3, max=100), validators.DataRequired()])
#     gender = RadioField('gender', choices = ['male', 'female'])
#     diagnosis = TextAreaField('diagnosis', validators=[validators.length(min=3, max=1000), validators.DataRequired()])
#     hmo = SelectField('hmo', choices=[('HMO1', 'HMO1'), ('HMO2', 'HMO2'), ('HMO3', 'HMO3'), ('HMO4', 'HMO4')], validators=[validators.DataRequired()])
#     age = IntegerField(validators=[validators.NumberRange(min=0), validators.DataRequired()])

#     service_date = DateField(format='%Y-%m-%d', validators=[validators.DataRequired()])
#     service_name = StringField('service_name', validators=[validators.length(min=3, max=100), validators.DataRequired()])
#     service_name = StringField('service_name', validators=[validators.length(min=3, max=100), validators.DataRequired()])
#     type = StringField('type', choices=[('Hematology', 'Hematology'), ('Microbiology', 'Microbiology'), ('Chemical Pathology', 'Chemical Pathology'), ('Hispathology', 'Hispathology'), ('HMO1', 'HMO1'), ('HMO2', 'HMO2'), ('HMO3', 'HMO3'), ('Immunology', 'Immunology')],validators=[validators.length(min=3, max=50), validators.DataRequired()])
    
#     provider_name = StringField('provider_name', validators=[validators.length(min=3, max=100), validators.DataRequired()])

#     source = StringField('source', validators=[validators.length(min=3, max=100), validators.DataRequired()])
#     cost_of_service = FloatField(validators=[validators.NumberRange(min=0), validators.DataRequired()])

class AddClaim(FlaskForm):
    user = SelectField('User', choices=all_users, validators=[validators.DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    diagnosis = TextAreaField('Diagnosis', validators=[validators.Length(min=3, max=1000), validators.DataRequired()])
    hmo = SelectField('HMO', choices=[('HMO1', 'HMO1'), ('HMO2', 'HMO2'), ('HMO3', 'HMO3'), ('HMO4', 'HMO4')], validators=[validators.DataRequired()])
    age = IntegerField('Age', validators=[validators.NumberRange(min=0), validators.DataRequired()])
    
    service_date = DateField('Service Date', format='%Y-%m-%d', validators=[validators.DataRequired()])
    service_name = StringField('Service Name', validators=[validators.Length(min=3, max=100), validators.DataRequired()])
    type = SelectField('Type', choices=[
        ('Hematology', 'Hematology'), 
        ('Microbiology', 'Microbiology'), 
        ('Chemical Pathology', 'Chemical Pathology'),
        ('Hispathology', 'Hispathology'),
        ('Immunology', 'Immunology')
    ], validators=[validators.DataRequired()])
    
    provider_name = StringField('Provider Name', validators=[validators.Length(min=3, max=100), validators.DataRequired()])
    source = StringField('Source', validators=[validators.Length(min=3, max=100), validators.DataRequired()])
    cost_of_service = FloatField('Cost of Service', validators=[validators.NumberRange(min=0), validators.DataRequired()])
    total_cost = FloatField('Total Cost', validators=[validators.NumberRange(min=0), validators.DataRequired()])
    service_charge = FloatField('Service Charge', validators=[validators.NumberRange(min=0), validators.DataRequired()])
    final_cost = FloatField('Final Cost', validators=[validators.NumberRange(min=0), validators.DataRequired()])
