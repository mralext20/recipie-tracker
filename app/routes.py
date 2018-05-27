from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.forms import SignupForm, LoginForm, RecipeForm
from app.models import Recipe, Chef
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.query.all()
    if request.path == "/":
        return render_template('home.html', recipies=recipes)
    else:
        return render_template('index.html', title="Index", recipies=recipes)


@app.route('/submit', methods=["GET","POST"])
@login_required
def submit():
    """submit a recipe"""
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
                        title=form.title.data,
                        ingredients=form.ingredients.data,
                        instructions=form.instructions.data,
                        author=current_user)
        db.session.add(recipe)
        db.session.commit()
        return redirect(f'/recipe/{recipe.id}')
    return render_template('submit.html', title="submit", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = Chef.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')

        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = Chef(username=form.username.data, displayname=form.displayname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Register', form=form)


@app.route('/recipe/<int:rid>')
def recipe_route(rid):
    target = Recipe.query.filter_by(id=rid).one_or_none()
    if target is None:
        flash('that recipe doesnt exist!')
        return redirect('/')
    return render_template('recipe.html', title=target.title, recipe=target)


@app.route('/chef/<int:uid>')
def chef(uid):
    target = Chef.query.filter_by(id=uid).one_or_none()
    if target is None:
        flash("that chef doesnt exist")
        return redirect('/')
    recipies = target.recipies
    return render_template('chef.html', title=f"Chef {target.displayname}",chef=target, recipies=recipies)


@app.route('/delete/chef/<int:uid>', methods=["POST"])
def delete_chef(uid):
    target = Chef.query.filter_by(id=uid).one_or_none()
    if target is None:
        flash("that Chef doesnt exist?")
        return redirect('/')
    if current_user.admin or current_user == target:
        if current_user == target:
            logout_user()
        [db.session.delete(recipe) for recipe in target.recipies]
        db.session.delete(target)
        db.session.commit()
        flash("successfully deleted user")
    else:
        flash('you arent allowed to access this')
    return redirect('/')


@app.route('/delete/recipe/<int:rid>')
def delete_recipe(rid):
    target = Recipe.query.filter_by(id=rid).one_or_none()
    if target is None:
        flash("that recipe doesnt exist?")
        return redirect('/')
    if current_user.admin or target.author == current_user:
        db.session.delete(target)
        db.session.commit()
        flash("successfully deleted recipe")
    else:
        flash('you arent allowed to access this')
    return redirect('/')


@app.route('/edit/<int:rid>', methods=["GET", "POST"])
def edit_recipe(rid):
    target = Recipe.query.filter_by(id=rid).one_or_none()

    if (current_user.admin or target.author == current_user) or target is None:
        form = RecipeForm()
        if form.validate_on_submit():
            target.title = form.title.data
            target.instructions = form.instructions.data
            target.ingredients = form.ingredients.data
            db.session.add(target)
            db.session.commit()
            flash(f'successfully edited {target.title}')
            return redirect(f'/recipe/{rid}')

    else:
        flash('you do not have permission to edit this recipe')
        redirect('/')
    form = RecipeForm(title=target.title,
                      ingredients=target.ingredients,
                      instructions=target.instructions)
    return render_template('submit.html', title=f'Editing {target.title}', form=form)


@app.route('/chef/<int:uid>/make_admin', methods=["POST"])
def make_admin(uid):
    target = Chef.query.filter_by(id=uid).one_or_none()
    if target is None:
        flash('That user does not exist!')
        return redirect('/')
    if current_user.admin:
        target.admin = True
        db.session.add(target)
        db.session.commit()
        flash(f'made {target.displayname} an Admin!')
    else:
        flash("you are not allowed to make people admins")
    return redirect(f'/chef/{uid}')


@app.route('/chef/<int:uid>/take_admin', methods=["POST"])
def take_admin(uid):
    target = Chef.query.filter_by(id=uid).one_or_none()
    if target is None:
        flash('That user does not exist!')
        return redirect('/')
    if current_user.admin:
        target.admin = False
        db.session.add(target)
        db.session.commit()
        flash(f'Took admin from {target.displayname}')
    else:
        flash("you are not allowed to take admin from people")
    return redirect(f'/chef/{uid}')
