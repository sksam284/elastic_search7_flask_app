import os
from builtins import len

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_bootstrap import Bootstrap

from forms.city import CityForm, EditCityForm
from forms.country import CountryForm, EditCountryForm
from forms.state import StateForm, EditStateForm
from models.country import Country
from models.state import State
from models.city import City

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(12).hex()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dd")
def dd():
    return render_template("dependent_dropdown.html")


@app.route("/get_country", methods=['GET'])
def get_country():
    country_data = Country.list()
    if len(country_data) > 0:
        return jsonify({"country": country_data}), 200
    else:
        return jsonify({"error": True, "message": "No data present for countries"}), 200


@app.route("/get_state", methods=['GET'])
def get_state():
    country = request.args.get("country", type=str)
    if not country:
        return jsonify({"message": "Please set the country field"}), 400
    state_data = State.list(country)
    if len(state_data) > 0:
        return jsonify({"state": state_data}), 200
    else:
        return jsonify({"error": True, "message": "No state data present for country - " + country}), 200


@app.route("/get_city", methods=['GET'])
def get_city():
    state = request.args.get("state", type=str)
    if not state:
        return jsonify({"message": "Please set the state field"}), 400
    city_data = City.list(state)
    if len(city_data) > 0:
        return jsonify({"city": city_data}), 200
    else:
        return jsonify({"error": True, "message": "No city data present for state - " + state}), 200


@app.route("/country", methods=['GET'])
def country():
    return render_template("crud/country/list.html", countries=Country.list())


@app.route("/country/create", methods=['GET', 'POST'])
def country_create():
    country_form = CountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/create.html', form=country_form)
        else:
            result = Country.create(request.form["name"])
            if result:
                flash('Country created successfully!!!')
                return redirect(url_for('country'))
            else:
                flash('Unable to create country.')
                return render_template('crud/country/create.html', form=country_form)
    else:
        return render_template('crud/country/create.html', form=country_form)


@app.route("/country/edit/<id>", methods=['GET', 'POST'])
def country_edit(id):
    country_form = EditCountryForm()
    if request.method == 'POST':
        if not country_form.validate():
            flash('All fields are required.')
            return render_template('crud/country/edit.html', form=country_form)
        else:
            result = Country.edit_country(request.form["id"], request.form["name"])
            if result:
                flash('Country edited successfully!!!')
                return redirect(url_for('country'))
            else:
                flash('Unable to edit country.')
                return render_template('crud/country/edit.html', form=country_form)
    else:
        country = Country.get(id)
        if not country:
            return redirect(url_for('country'))
        country_form.name.data = country["name"]
        country_form.id.data = country["id"]
        return render_template('crud/country/edit.html', form=country_form)


@app.route("/counrty/delete/<id>", methods=['POST'])
def country_delete(id):
    result = Country.delete(id)
    if result:
        flash('Country deleted successfully!!!')
    return redirect(url_for('country'))


@app.route("/state", methods=['GET'])
def state():
    return render_template("crud/state/list.html", states=State.list(""))


@app.route("/state/create", methods=['GET', 'POST'])
def state_create():
    state_form = StateForm()
    if request.method == 'POST':
        if not state_form.validate():
            flash('All fields are required.')
            return render_template('crud/state/create.html', form=state_form)
        else:
            result = State.create(request.form["name"], request.form["country"])
            if result:
                flash('State created successfully!!!')
                return redirect(url_for('state'))
            else:
                flash('Unable to create state.')
                return render_template('crud/state/create.html', form=state_form)
    else:
        return render_template('crud/state/create.html', form=state_form)

@app.route("/state/edit/<id>/", methods=['GET', 'POST'])
@app.route("/state/edit/<id>/<country>", methods=['GET', 'POST'])
def state_edit(id, country=None):
    state_form = EditStateForm()
    if request.method == 'POST':
        if not state_form.validate():
            flash('All fields are required.')
            return render_template('crud/state/edit.html', form=state_form)
        else:
            result = State.edit(request.form["id"], request.form["name"], request.form["country"])
            if result:
                flash('State edited successfully!!!')
                return redirect(url_for('state'))
            else:
                flash('Unable to edit state.')
                return render_template('crud/state/edit.html', form=state_form)
    else:
        state = State.get(id)
        country = Country.get(state["country_id"])
        if not state:
            return redirect(url_for('state'))
        state_form.name.data = state["name"]
        state_form.id.data = state["id"]
        state_form.country_id.data = state["country_id"]
        state_form.country.data = country["name"]

        return render_template('crud/state/edit.html', form=state_form)


@app.route("/state/delete/<id>/", methods=['POST'])
def state_delete(id):
    result = State.delete(id)
    if result:
        flash('State deleted successfully!!!')
    return redirect(url_for('state'))


@app.route("/city", methods=['GET'])
def city():
    return render_template("crud/city/list.html", cities=City.list(""))


@app.route("/city/create", methods=['GET', 'POST'])
def city_create():
    city_form = CityForm()
    if request.method == 'POST':
        if not city_form.validate():
            flash('All fields are required.')
            return render_template('crud/city/create.html', form=city_form)
        else:
            result = City.create(request.form["name"], request.form["state"])
            if result:
                flash('City created successfully!!!')
                return redirect(url_for('city'))
            else:
                flash('Unable to create city.')
                return render_template('crud/city/create.html', form=city_form)
    else:
        return render_template('crud/city/create.html', form=city_form)


@app.route("/city/edit/<id>/", methods=['GET', 'POST'])
def city_edit(id):
    city_form = EditCityForm()
    if request.method == 'POST':
        if not city_form.validate():
            flash('All fields are required.')
            return render_template('crud/city/edit.html', form=city_form)
        else:
            result = City.edit(request.form["id"], request.form["name"], request.form["state"])
            if result:
                flash('City edited successfully!!!')
                return redirect(url_for('city'))
            else:
                flash('Unable to edit city.')
                return render_template('crud/city/edit.html', form=city_form)
    else:
        city = City.get(id)
        state = State.get(city['state_id'])
        if not city:
            return redirect(url_for('state'))
        city_form.name.data = city["name"]
        city_form.state.data = state["name"]
        city_form.id.data = city["id"]
        city_form.state_id.data = city["state_id"]
        return render_template('crud/city/edit.html', form=city_form)


@app.route("/city/delete/<id>/<state>", methods=['POST'])
def city_delete(id, state):
    result = City.delete(id, state)
    if result:
        flash('City deleted successfully!!!')
    return redirect(url_for('city'))


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
