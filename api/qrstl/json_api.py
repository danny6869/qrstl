#!/usr/bin/python3

import io
from api.qrstl.background_model import BackgroundModel
from api.qrstl.qrcode_stl import QRCodeSTL
import tempfile
import os
import uuid
import urllib.parse

from flask import Flask, jsonify, send_file, request
app = Flask(__name__)

class NotFoundException(Exception):
    pass
class InputValidationException(Exception):
    pass

def _output_exception_response(http_response_code,error):
    response = {
        'message': str(error),
        'exception_type': error.__class__.__name__,
        'response_code': http_response_code,
    }
    # XXX - this actually returns as 200 right now...fix that
    return jsonify(response)

@app.errorhandler(NotFoundException)
def handle_not_found_exception(error):
    return _output_exception_response(404,error)

@app.errorhandler(InputValidationException)
def handle_bad_request_exception(error):
    return _output_exception_response(400,error)

@app.errorhandler(Exception)
def handle_bad_request_exception(error):
    return _output_exception_response(500,error)

@app.route("/")
def main():
    return "<img src='https://pbs.twimg.com/media/DEjoivzXoAEoZXQ.jpg'></img>"

@app.route("/api")
def main_api():
    return jsonify( uri = [
        '/api/assets',
        '/api/qr',
        '/api/sample/qr',
        '/api/sample/image',
    ] )

@app.route("/api/assets")
def assets():
    model_list = []
    for model_obj in BackgroundModel.all():
        model_list.append({
                'name': model_obj.name,
                'description': model_obj.description,
                'create_uri': '/api/qr?name={}&data='.format(urllib.parse.quote_plus(model_obj.name)),
                'sample_stl_uri': '/api/sample/qr?name={}&data={}'.format(urllib.parse.quote_plus(model_obj.name),urllib.parse.quote_plus('http://qrstl.com')),
                'sample_image_uri': '/api/sample/image?name={}'.format(urllib.parse.quote_plus(model_obj.name)),
# XXX - Maybe something like this too!?
#                'attributes': {
#                    'dimensions': [40,40,5],
#                    'tags': ['magnet','logo','nfc']
#                },
        })
    return jsonify( model_list = model_list, )

@app.route("/api/qr")
def generate_qr():

    # Input...
    background_model_name = request.args.get("name")
    qr_data = request.args.get("data")

    # Complain about missing or bad input...
    if qr_data is None or qr_data == '':
        raise InputValidationException("Missing QR code \"data\" parameter value.  Refusing to create a blank QR code.")
    elif qr_data not in []:
        # TODO: Proper check for valid-ish QR code needed
        pass

    if background_model_name is None or background_model_name == '':
        raise InputValidationException("Missing background template \"name\" parameter value.  See assets for possible values.")

    qr_stl = QRCodeSTL.make_stl(background_model_name, qr_data)

# XXX - Make this work in-memory...having a hell of a time with this...not quite making sense right now...will come back to it...
    inmemory = False
    output_filehandle_or_filename = None
    if inmemory:
        # Create the STL "file" in memory...
        iob = io.BytesIO()
        qr_stl.save(qr_stl.background_model.filename,iob)
        output_filehandle_or_filename = iob
    else:
        # Create the STL file to a tempfile, and send it out from there...
        tf = tempfile.gettempdir()
        tf = uuid.uuid4()
        tf = os.path.join(tempfile.gettempdir(), "{}.{}".format(str(uuid.uuid4()),qr_stl.kind.lower()))
        qr_stl.save(tf)
        output_filehandle_or_filename = tf

    return send_file(
        output_filehandle_or_filename,
        attachment_filename=qr_stl.background_model.filename,
        as_attachment=True,
        #mimetype='application/octet-stream',
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2112)

