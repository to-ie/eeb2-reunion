# Testing process

Below is a list of the tests that could be done in order to ensure the website 
works as expected. This list is not exhaustive and does not take into account
the admin capabilities. Coupling these admin manipulations with the other 
functions might underline some bugs. These will need to be documented and 
tested.

[ ] Visit the non-encrypted version of the site should redirect you to the 
    encrypted version: http://eeb2.t-o.ie/ redirects to https://eeb2.t-o.ie/

## As a non-logged in user: 

[ ] Check that all the links on the home page work. Try as many of the social 
    media sharing links, I am unable to test these fully.
[ ] Try accessing restricted pages, this should redirect you to the login page
    with a mention that the page is restricted. Examples of restricted pages 
    include: 
        - https://eeb2.t-o.ie/user/1
        - https://eeb2.t-o.ie/about
        - https://eeb2.t-o.ie/reconnect
        - https://eeb2.t-o.ie/memory-lane
        - https://eeb2.t-o.ie/admin/guests [admin only]
[ ] Try logging in with a bogus email address and password. You should see an 
    error message.
[ ] Try logging in by omitting to put in an email or password. You should get an
    error message.

## User registration:
[ ] Create a new account and check that you receive the verification email. Do 
    not click on the verification link at this stage.
[ ] Make sure the verification email displays correctly.
[ ] Without having verified the email address, try logging in. You should get 
    the relevant error message.
[ ] Verify the email address by clicking on the link that you received in your 
    inbox. You should be redirected to the login page, with the relevant 
    message.
[ ] Click on password reset and try resetting your password. You should receive 
    an email with instructions. 
[ ] Try logging in with your new credentials.

## As a logged in user:
[ ] When you first login, you should be prompted to fill in your profile. Fill 
    in the details as if you were a Graduate of 2005.
[ ] Upload a photo to your new profile.
[ ] Upload a new photo to your profile (different one). Check that the photo has
    been updated.
[ ] Update some of your social links.
[ ] Update your RSVP status (via the pen icon AND the 'Update your RSVP' button)
[ ] Click on the 'See your public profile' button. 
[ ] Head over to the reconnect page and find your name. You should see a blue 
    link next to it, pointing you to your public profile.
[ ] Head back over to your profile (Member's are > Profile) and reset your 
    profile (tiny link at the bottom right of the profile page). Check your 
    emails for the confirmation email.
[ ] Head back to the reconnect page and check your name. It should now show you 
    the invite link.
[ ] Go back to your profile and fill it in as if you were a friend of graduate.
[ ] Head over to the reconnect page and check that your name appears in the 
    'friends' tab.
[ ] Head over to the homepage and check the 'Be part of the celebrations' stats:
    They should be n+1 than before.
[ ] Reset your profile.
[ ] Go back to your profile and fill it in as if you were a friend of graduate.
[ ] Head over to the reconnect page and check that your name appears in the 
    'friends' tab.
[ ] Go back to your profile and fill it in as if you were a teacher.
[ ] Head over to the reconnect page and check that your name appears in the 
    'teachers' tab.
[ ] Go back to your profile and fill it in as if you were of the other category.
[ ] Head over to the reconnect page and check that your name appears in the 
    'other' tab.
[ ] Check out the about page. Try sending us an email via the get in touch link.
    Try putting in a wrong captcha. Try using any of the following options for 
    the captcha: '7','seven' or 'Seven'
[ ] Go back to the about page. Try updating your RSVP.
[ ] Play around with the reconnect page. See if you can break it. See if you can 
    find a specific person in the list. (search by name, sort by 'registered', 
    search for specific sections).
[ ] Check the 'Down memory lane' page. Try out the links.
[ ] Try accessing an admin page and see if you get the error message:
        - https://eeb2.t-o.ie/admin/guests
[ ] Logout, you are done. 
