from flask import Flask
from flask import render_template, redirect, request, session, url_for, jsonify
from UserManager import app, fenix_blueprint


@app.route('/')
#@app.route('/login')
def home_page():
    # The access token is generated everytime the user authenticates into FENIX
    print(fenix_blueprint.session.authorized)
    print("Access token: "+ str(fenix_blueprint.session.access_token))
    #redirect(url_for("fenix-example.login"))
    return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)


@app.route('/logout')
def logout():
    # this clears all server information about the access token of this connection
    res = str(session.items())
    print(res)
    session.clear()
    res = str(session.items())
    print(res)
    # when the browser is redirected to home page it is not logged in anymore
    return redirect(url_for("home_page"))

    

@app.route('/private')
def private_page():
    #this page can only be accessed by a authenticated user

    # verification of the user is  logged in
    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return redirect(url_for("fenix-example.login"))
    else:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #res contains the responde made to /api/fenix/vi/person (information about current user)
        data = resp.json() 
        print(resp.json())
        return render_template("privPage.html", username=data['username'], name=data['name'])
