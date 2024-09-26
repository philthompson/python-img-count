
A quick python script for counting blobs (like birds) in JPG images.

#### Running

        $ python3 -m venv python-venv
        $ source python-venv/bin/activate
        $ python3 -m pip install -r python-requirements.txt
        # !! see tips/info at the top of count.py !!
        $ python3 count.py /path/to/image.jpg

#### Python pip

To install python dependencies:

        $ python3 -m venv python-venv
        $ source python-venv/bin/activate
        $ python3 -m pip install -r python-requirements.txt
        $ deactivate

To install new dependencies:

        $ source python-venv/bin/activate
        $ python3 -m pip install ...
        $ python3 -m pip freeze > python-requirements.txt

To update python dependencies if the `python-requirements.txt` file is updated:

        $ source python-venv/bin/activate
        $ python3 -m pip install --ignore-installed -r python-requirements.txt

