REQUIREMENTS
------------
1. Python 3
2. Reddit account with Moderator privileges for a subreddit
3. Reddit Client ID and Secret for the account in #2
4. Twitch API Key

DEPENDENCIES
------------
1. [Pillow](https://pypi.python.org/pypi/Pillow/4.1.1) - Used to generate the spritesheets 
2. [Praw 4+](https://praw.readthedocs.io/en/latest/) - Used for all Reddit actions
3. [pyOpenSSL](https://pypi.python.org/pypi/pyOpenSSL) - Used to fix some SSL issues

You can install all of the above packages at once with `sudo pip install --upgrade Pillow praw pyopenssl`

Note that you must first have Python 3 installed before running the above command.

Configuring the script
----------
First and foremost, in order for this to work you *must* provide credentials that are tied to a Reddit account which has 
moderator access to the subreddit you run the script against. If you are unsure how to generate a Client-ID and Secret, 
login to the Reddit account to be authenticated with the script and go to Preferences>apps. Create a 'Personal Use Script'
and fill out the needed info. Since you will be registering a personal-use script, there won't be a need for a redirect-URI,
but Reddit still requires that you provide something here, so just 'http://localhost/reddit-oauth' will suffice.

After registering the application, your client_id will be underneath the name you gave it as seen [here](https://i.imgur.com/n3dKYcF.png),
and the client_secret will be next to the 'Secret:' label.

1. In `cfg/accounts.json` add the Reddit client_id, client_secret, username and password for the Reddit account you created the app under.
2. In `cfg/accounts.json` add your Twitch API key.
3. In `cfg/settings.json` add your subreddit name and the name of the primary bot reddit account (username).
4. An example sidebar template can be seen in `cfg/sidebar.txt`. The script uses the `__LIVESTREAMS__` text to replace with the stream list.
  * Note that this file is the template that is used every time you run the script. If you need to edit something in the sidebar outside of the streams list, you'll need to do so in this file, *NOT* on Reddit directly,
  or this will just overwrite it the next time it runs.
5. `cfg/templates.json` is the default template for the markdown that gets placed in the sidebar for each stream. You may edit this if you like, It's mainly used this way for our current styling on r/GlobalOffensive.

Running the script
------------------
Start the script *from within the top-most folder* by entering `python main.py` in CMD. 
**Note** - From your command prompt, you will need to `cd` (Change Directory command) into the directory where the script is saved. See the tip below if you don't know how to do this.

On Linux systems, you may automate the script every 5 minutes from a crontab. If you're unsure what a crontab/job is, Google is your friend. To create a simple cronjob that runs this
script every 5 minutes:

`*/5 * * * * python /path/to/scripts/main.py`

**TIP** - As a shortcut on Windows, you can open the folder containing the script and SHIFT + Right Click in the empty space,
then choose "Open command window here" if you don't want to have to CD to the correct directory, or if you're unsure how. 

Common Errors
---------------
If you have both Python 2 and 3 installed on your system and receive errors when starting the script with `python main.py`, 
run the script with `python3 main.py` instead. This can be the case if you only have one environment variable set for python 
on your system (pointing to python 2), but have both versions installed. If you have to do it this way, you'll also need to 
make sure you actually installed praw for python3 instead of 2. You can check which version its tied to with `pip show praw`.
If it got tossed in with python2, install it for python3 with `pip3 install praw`.

**HTTP 401 error (unauthorized)** - 
  * This typically means there's an issue with the Client-ID you supplied. When you go to preferences>apps and click 'edit' 
  under the application you created, your Client-ID will be [here](https://i.imgur.com/n3dKYcF.png)

**OAuthException: unauthorized_client error processing request (Only script apps may use password auth)** - 
  * If you see this error, it's likely you didn't create the application correctly under preferences>apps. When setting this up,
  there are 3 options to choose from: web app, installed app, script. You *must* register the app as a **script app** for this 
  to work. [Example](https://i.imgur.com/ZV30NVg.png)