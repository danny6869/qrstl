import os

BACKGROUND_FILE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'background_models')

BACKGROUND_FILE_ATTRIBUTES = {
    # NOTE: All units below are in mm unless otherwise noted
    '_DEFAULT': {
        'description': '(none)',
        # QR drawing area bounding cube
        'qr_size_x': 0,
        'qr_size_y': 0,
        'qr_size_z': 0,
        # Starting position...
        'offset_x': 0,
        'offset_y': 0,
        'offset_z': 0,
        # Size of the center area that is reserved for a logo (so we don't add our QR "pixels" in that area)...
        # no_draw_position = center|topleft|topright|bottomleft|bottomright|topcenter|bottomcenter|centerleft|centerright
        'no_draw_position': None,
        'no_draw_x': 0,
        'no_draw_y': 0,
        # Height at which the instructions should show to change filament
        'change_filament_height': 0,
    },
    '5cm_coaster_no_nfc': {
        'description': '5cm QR coaster (no NFC)',
        'qr_size_x': 40,
        'qr_size_y': 40,
        'qr_size_z': 5,
        'change_filament_height': 3.0,
    },
    '5cm_coaster_nfc': {
        'description': '5cm QR coaster (with NFC)',
        'qr_size_x': 40,
        'qr_size_y': 40,
        'qr_size_z': 5,
        'no_draw_position': 'bottomright',
        'no_draw_x': 10,
        'no_draw_y': 12,
        'change_filament_height': 3.0,
    },
    '5cm_coaster_nfc_no_logo': {
        'description': '5cm QR coaster (with NFC - no logo)',
        'qr_size_x': 40,
        'qr_size_y': 40,
        'qr_size_z': 5,
        'change_filament_height': 3.0,
    },
    # XXX - List to add
    # 5cm refrigerator magnet with NFC
    # 5cm refrigerator magnet with NFC (no logo)
    # 5cm refrigerator magnet with no NFC
    # XXX - From here down are temporary samples to play with
    'QRSurround (9cm)': {
        'description': 'Standard blah blah blah',
        'qr_size_x': 80,
        'qr_size_y': 80,
        'qr_size_z': 3,
        'no_draw_position': 'center',
        'no_draw_x': 35,
        'no_draw_y': 35,
        'change_filament_height': 3.1,
    },
    'QRSurround (10cm)': {
        'description': 'Standard blah blah blah',
        'qr_size_x': 100,
        'qr_size_y': 100,
        'qr_size_z': 3,
        'no_draw_position': 'center',
        'no_draw_x': 35,
        'no_draw_y': 35,
        'change_filament_height': 3.1,
    },
    'QRSurround (12cm)': {
        'description': 'Standard blah blah blah',
        'qr_size_x': 100,
        'qr_size_y': 100,
        'qr_size_z': 3,
        'no_draw_position': 'center',
        'no_draw_x': 35,
        'no_draw_y': 35,
        'change_filament_height': 3.1,
    },
}
