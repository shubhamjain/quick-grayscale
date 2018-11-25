## Quick Grayscale

Quick Grayscale lets you easily toggle mac's grayscale mode from the status bar. It's a wrapper around couple of Applescripts that automate the process of going in settings and toggling the "Use Grayscale" checkbox (since Apple doesn't provide any API to handle it programmatically). To download the application, [head here](https://shubhamjain.co/quick-grayscale/).

## Running
Quick Grayscale has been developed with RUMPS library which is a wrapper over PyObjC. To run it, install all dependencies via:

`pip3 install -r requirements.txt`

and then, run the main source file:

`python3 quick-gray.py`

## Building
The application package can be build by using py2app. 

`python3 setup.py py2app`

## License
MIT.