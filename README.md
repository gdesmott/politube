# Politu.be

Easy to use website to browse and watch plenary sessions of the Belgian
Chamber of Representatives.

# Installation

You need pip and virtualenv (or buildout).

Under debian based distributions:

    sudo apt-get install python-pip python-virtualenv

Once this is done create a virtualenv, for example:

    virtualenv --distribute --no-site-packages ve

Then activate it:

    source ve/bin/activate

Now, install the dependencies (this can take a little bit of time):

    pip install -r requirements.txt

And install the indices:

    python manage.py syncdb

# Usage

To launch the scraping (this is *long*, do this in a screen):

    python manage.py update-politube-db

To launch the dev server:

    python manage.py runserver

# Public instance

http://www.politu.be

# Licence

agplv3+
