# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from vendors.forms import UserForm, UserProfileForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from vendors.models import UserProfile



def registration(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially.  Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #if the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
        # Invalid form for forms - mistake or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the tempalte depending on the context.
    return render_to_response(
        'web/registration.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},context
    )

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attemp to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided.  So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP Post, so display the login form.
    # This scenario would mostlike to be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictioanry object...
        return render_to_response('web/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def profile(request):
    # Get the context of the request
    context = RequestContext(request)

    #A boolean field for detecting whether adding an address or not
    edited = False

    # If it's a HTTP POST, we will be processing the data
    if request.method == 'POST':
        # Attemp to grab information from the raw form information.
        # Note we make use of both UserForm and UserProfileForm.
        profileupdate_form = ProfileUpdateForm(data=request.POST)

        # If the two forms are valid...
        if profileupdate_form.is_valid():
            # Save the user's form data to the database.
            user = User.objects.get(username=request.user)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            try:
                profile = UserProfile.objects.get(user_id=request.user.id)
                profile.company = request.POST['company']
                profile.map_lon = request.POST['map_lon']
                profile.map_lat = request.POST['map_lat']
                profile.save()
            except UserProfile.DoesNotExist:
                newprofile = UserProfile(user_id=request.user.id, company=request.POST['company'], map_lon=request.POST['map_lon'], map_lat=request.POST['map_lat'])
                newprofile.save()


            return HttpResponse("Thanks!")
        else:
            return HttpResponse(profileupdate_form.errors)

    else:
        profileupdate_form = ProfileUpdateForm()
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            profile = None
    # Render the template
    return render_to_response(
        'web/profile.html',
        {'form': profileupdate_form, 'profile': profile, 'edited': edited}, context
    )