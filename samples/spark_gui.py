# under normal circumstances, this script would not be necessary. the
# sample_application would have its own setup.py and be properly installed;
# however since it is not bundled in the sdist package, we need some hacks
# to make it work

import os
import sys

sys.path.append(os.path.dirname(__name__))

from spark_gui import create_app

# create an app instance
app = create_app()

app.run(host='0.0.0.0', port=8080, debug=True)
