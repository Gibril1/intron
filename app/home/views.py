from flask import flash, jsonify, render_template, redirect, request, url_for

from app.models import Claim, Service, User
from . import home as home_blueprint
from app.forms import AddUser, AddClaim
from app import database
from datetime import datetime
import datetime as dt


@home_blueprint.route('/all/users', methods=['GET'])
def all_users():
    """
    List all Users
    """
    all_users = User.query.all()
    return render_template('home/home.html', users=all_users, title="Users")

@home_blueprint.route('/user/<int:id>', methods=['GET'])
def view_user(id):
    """
    A route that displays user details along with their claims and services.
    """
    user_data = User.query.get_or_404(id)
    
    # Fetch all claims related to the user
    claims = Claim.query.filter_by(user_id=id).all()
    
    return render_template('home/user_data.html', user_data=user_data, claims=claims)


@home_blueprint.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """
        A route for editing a user record
    """
    form = AddUser()

    user_data = User.query.get(int(id))

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        salary = request.form.get('salary')
        date_of_birth = request.form.get('date_of_birth')

        dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if form.validate_on_submit():
            user_data.name = name
            user_data.gender = gender
            user_data.salary = salary
            user_data.date_of_birth = dt_obj

            # Calculate new age
            new_age = dt.date.today().year - user_data.date_of_birth.year

            # Update all related claims with new age
            claims = Claim.query.filter_by(user_id=id).all()
            for claim in claims:
                claim.age = new_age

            database.session.commit()

            flash('User updated successfully.', 'success')
            return redirect(url_for('home.edit_user', id=user_data.id))

    return render_template('home/edit_user.html', user_data=user_data, form=form)

@home_blueprint.route('users/add', methods=['GET', 'POST'])
def add_user():
    """
        A route for adding users

    """
    form = AddUser()

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        salary = request.form.get('salary')
        date_of_birth = request.form.get('date_of_birth')

        dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if form.validate_on_submit():
            new_user = User(name=name, gender=gender, salary=salary, date_of_birth=dt_obj)
            database.session.add(new_user)
            database.session.commit()

            flash('User created successfully.', 'success')
            return redirect(url_for('home.all_users'))

        flash('You entered and invalid form data', 'danger')
        return render_template('home/create_user.html', form=form)
    else:
        
        return render_template('home/create_user.html', form=form)

@home_blueprint.route('/user/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """
        A route for deleting a user
    """
    user_data = User.query.get(int(id))
    database.session.delete(user_data)
    database.session.commit()

    flash('User deleted successfully.', 'success')
    return redirect(url_for('home.all_users'))


@home_blueprint.route('claim', methods=['GET'])
def claim():
    """
    List all Claims
    """
    all_claims = Claim.query.all()

    print("****all claims******", all_claims)
    return render_template('home/claim.html', claims=all_claims, title="Claims")

@home_blueprint.route('claim/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def claim_detail(id):
    """
        A route that allows claim officer fillout a form for a particular user
    """
    claim = Claim.query.get(int(id))
    if request.method == 'GET':
        return render_template('home/claim_detail.html', claim=claim)
    
    elif request.method == 'PUT':
        claim.diagnosis = request.form.get('diagnosis')
        claim.hmo = request.form.get('hmo')
        claim.age = request.form.get('age')
        claim.service_charge = request.form.get('service_charge')
        claim.total_cost = request.form.get('total_cost')
        claim.final_cost = request.form.get('final_cost')

        database.session.commit()
        flash('Claim updated successfully!', 'success')
        return redirect(url_for('home.claim', id=claim.id))
    
    elif request.method == 'DELETE':
        database.session.delete(claim)
        database.session.commit()
        flash('Claim deleted successfully!', 'danger')
        return redirect(url_for('home.claim')) 



@home_blueprint.route('/create_claim', methods=['GET', 'POST'])
def create_claim():
    """
    A route for a claim officer to make/create a claim.
    """ 

    form = AddClaim()
    all_users = User.query.with_entities(User.name).all()


    if request.method == "POST":
        user = request.form.get('user')
        diagnosis = request.form.get('diagnosis')
        hmo = request.form.get('hmo')
        age = request.form.get('age')

        total_cost = request.form.get('total_cost')
        service_charge = request.form.get('service_charge')
        final_cost = request.form.get('final_cost')

        user = User.query.filter_by(name=user).first()
        new_claim = Claim(
            user_id=user.id, 
            diagnosis=diagnosis, 
            hmo=hmo, 
            age=age,
            service_charge=service_charge,total_cost=total_cost, 
            final_cost=final_cost
        )
        database.session.add(new_claim)
        database.session.commit()

        # Get the form field values for service model insertion
        service_name = request.form.getlist('service_name')
        service_type = request.form.getlist('type')
        provider_name = request.form.getlist('provider_name')
        source = request.form.getlist('source')
        cost_of_service = request.form.getlist('cost_of_service')

        dates = request.form.getlist('service_date')

        # Formate dates
        service_date = []
        for d in dates:
            service_date.append(datetime.strptime(d, '%Y-%m-%d'))
        print("Service Dates", service_date)

        # Get the above claim as foreign key for services
        # claim = Claim.query.filter().last()
        claim = Claim.query.get(new_claim.id)

        # Loop to enter possible list of services
        for i in range(len(service_name)):
            new_service = Service(claim_id=claim.id, service_date=service_date[i], service_name=service_name[i], type=service_type[i], provider_name=provider_name[i], source=source[i], cost_of_service=cost_of_service[i])
            database.session.add(new_service)
            database.session.commit()

        flash('Claim created successfully.', 'success')
        return redirect(url_for('home.claim'))
    else:
        return render_template('home/create_claim.html', form=form, all_users=all_users)


@home_blueprint.route('create_claim/user_details/', methods=['POST'])
def user_age():
    """
    A route to get a user's birthdate and calculate their age 
    and return their gender.
    """
    if request.method == "POST":
        print(f'The request form is {request.form}')
        user_name = request.form.get("name", "").strip()

        # Retrieve user from the database
        user = User.query.filter_by(name=user_name).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Calculate age
        age = dt.date.today().year - user.date_of_birth.year
        print(f'The age of this user is {age}')

        # Log gender to check if it's retrieved
        print(f'User gender: {user.gender}')

        return jsonify({
            'age': age,
            'gender': user.gender  # Ensure the frontend gets the gender
        })

