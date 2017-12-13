#!/usr/bin/python3

import io
from api.qrstl.background_model import BackgroundModel
from api.qrstl.qrcode_stl import QRCodeSTL
import api.settings as settings
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

@app.route("/test")
def main_test():
    # XXX - Until I get some things more finalized...I don't care if people see this while I am working on it.
    return send_file(
        '../../site/index.html'
        # attachment_filename=qr_stl.background_model.filename,
        # as_attachment=True,
        # mimetype='application/octet-stream',
    )

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
    tag_list = []

    for model_obj in BackgroundModel.all():
        model_info = {
            'name': model_obj.name,
            'display_name': model_obj.display_name,
            'description': model_obj.description,
            'tags': model_obj.tags,
            'notes': model_obj.notes,
            'change_filament_height': model_obj.change_filament_height,
            'create_uri': '/api/qr?name={}&data='.format(urllib.parse.quote_plus(model_obj.name)),
            'sample_stl_uri': '/api/sample/qr?name={}&data={}'.format(urllib.parse.quote_plus(model_obj.name),urllib.parse.quote_plus('http://qrstl.com')),
            'sample_image_uri': '/api/sample/image?name={}'.format(urllib.parse.quote_plus(model_obj.name)),
        }

        # Add some notes automatically if needed...
        if model_obj.change_filament_height:
            model_info['notes'] = model_info['notes'] + [
                "For dual-color support, set your slicing software to stop for a filament change at the height of {}mm".format(model_obj.change_filament_height)
            ]

        # Add this model to our list...
        model_list.append(model_info)

        # Keep a list of all possible tags to communicate out...
        tag_list = tag_list + model_obj.tags

    tag_list = list(set(tag_list))
    return jsonify( model_list = model_list, tag_list = tag_list )

@app.route("/api/sample/image")
def sample_image():

    # Input...
    background_model_name = request.args.get("name")

    # Complain about missing or bad input...
    if background_model_name is None or background_model_name == '':
        raise InputValidationException(
            "Missing background template \"name\" parameter value.  See assets for possible values.")

    # Serve up our sample image file from the dir we keep them in...
    tf = os.path.join(settings.SAMPLE_PNG_FILE_DIRECTORY, "{}.png".format(background_model_name))

    if not os.path.isfile(tf):
        tf = os.path.join(settings.SAMPLE_PNG_FILE_DIRECTORY, "_blank.png")

    return send_file(
        tf,
    )


@app.route("/api/qr")
@app.route("/api/sample/qr")
def generate_qr():

    # Input...
    background_model_name = request.args.get("name")
    qr_data = request.args.get("data")

    # Complain about missing or bad input...
    if background_model_name is None or background_model_name == '':
        raise InputValidationException("Missing background template \"name\" parameter value.  See assets for possible values.")

    if qr_data is None or qr_data == '':
        raise InputValidationException("Missing QR code \"data\" parameter value.  Refusing to create a blank QR code.")
    elif qr_data not in []:
        # TODO: Proper check for valid-ish QR code needed
        pass

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

