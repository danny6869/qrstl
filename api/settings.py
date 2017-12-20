import os

BACKGROUND_FILE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'background_models')
SAMPLE_STL_FILE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'samples', 'stl')
SAMPLE_PNG_FILE_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'samples', 'png')

BACKGROUND_FILE_ATTRIBUTES = {
    # NOTE: All units below are in mm unless otherwise noted
    '_DEFAULT': {
        'display_name': '(none)',
        'description': '(none)',
        'tags': [],
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
        # Youtube video of timelapse
        'video_url': None,
        # Any notes to display for this model...
        'notes': [],
    },

    '30mm_keychain': {
        'display_name': '3cm keychain',
        'description': 'A basic 3cm x 3cm keychain.  Nothing fancy.',
        'tags': ['keychain'],
        'qr_size_x': 24,
        'qr_size_y': 24,
        'qr_size_z': 2,
        'no_draw_position': 'bottomright',
        'no_draw_x': 3,
        'no_draw_y': 3,
        'change_filament_height': 1.6,
        'notes': [
        ],
    },
    '40mm_keychain_with_nfc': {
        'display_name': '4cm keychain with embedded nfc',
        'description': 'A basic 3cm x 3cm keychain with an embedded nfc tag.',
        'tags': ['keychain','nfc'],
        'qr_size_x': 32,
        'qr_size_y': 32,
        'qr_size_z': 0.7,
        'offset_z': 2.8,
        'no_draw_position': 'bottomright',
        'no_draw_x': 4,
        'no_draw_y': 4,
        'change_filament_height': 3.1,
        'video_url': 'https://youtu.be/uQjJb_PdHbY',
        'notes': [
            'This model is designed to accept a 3cm diameter (1mm thick) nfc tag.',
            'Set your slicer to stop at the height of 1.82mm so you can insert the nfc tag.',
        ],
    },
    '50mm_magnet_with_nfc': {
        'display_name': '5cm magnet with embedded nfc',
        'description': 'A basic 5cm x 5cm keychain with an embedded nfc tag.',
        'tags': ['magnet','nfc'],
        'qr_size_x': 38,
        'qr_size_y': 38,
        'qr_size_z': 0.7,
        'offset_z': 4.3,
        'no_draw_position': 'center',
        'no_draw_x': 6,
        'no_draw_y': 6,
        'change_filament_height': 4.6,
        'video_url': 'https://youtu.be/6vTxt_XBr8U',
        'notes': [
            'This model is designed to accept a 3cm diameter (1mm thick) nfc tag, and a 10mm diameter (2mm thick) magnet.',
            'Set your slicer to stop at the height of 2.0mm so you can insert the nfc tag.',
            'The magnet should be able to easily be inserted once the print is complete.',
        ],
    },
    '50mm_magnet_no_nfc': {
        'display_name': '5cm magnet with embedded nfc',
        'description': 'A basic 5cm x 5cm keychain with an embedded nfc tag.',
        'tags': ['magnet'],
        'qr_size_x': 38,
        'qr_size_y': 38,
        'qr_size_z': 0.7,
        'offset_z': 4.3,
        'change_filament_height': 4.6,
        'video_url': None,
        'notes': [
            'This model is designed to accept a 10mm diameter (2mm thick) magnet.',
            'The magnet should be able to easily be inserted once the print is complete.',
        ],
    },
    # # TODO: From here down have not quite been vetted yet... still working on them.  Move above as they become "official".
    # '35mm_keychain_with_nfc': {
    #     'display_name': '',
    #     'description': '3.5cm keychain (nfc snap-together)',
    #     'tags': ['keychain','nfc'],
    #     'qr_size_x': 29,
    #     'qr_size_y': 29,
    #     'qr_size_z': 1.75,
    #     'no_draw_position': 'bottomright',
    #     'no_draw_x': 4,
    #     'no_draw_y': 4,
    #     'change_filament_height': 2.6,
    # },
    #  # XXX - Not really finalized from here down
    # '5cm_coaster_no_nfc': {
    #     'display_name': '',
    #     'description': '5cm QR coaster (no NFC)',
    #     'tags': ['coaster'],
    #     'qr_size_x': 40,
    #     'qr_size_y': 40,
    #     'qr_size_z': 5,
    #     'change_filament_height': 3.0,
    # },
    # '5cm_coaster_nfc': {
    #     'display_name': '',
    #     'description': '5cm QR coaster (with NFC)',
    #     'tags': ['coaster'],
    #     'qr_size_x': 40,
    #     'qr_size_y': 40,
    #     'qr_size_z': 5,
    #     'no_draw_position': 'bottomright',
    #     'no_draw_x': 10,
    #     'no_draw_y': 12,
    #     'change_filament_height': 3.0,
    # },
    # '5cm_coaster_nfc_no_logo': {
    #     'display_name': '',
    #     'description': '5cm QR coaster (with NFC - no logo)',
    #     'tags': ['coaster'],
    #     'qr_size_x': 40,
    #     'qr_size_y': 40,
    #     'qr_size_z': 5,
    #     'change_filament_height': 3.0,
    # },
    # # TODO: Add these...
    # # 5cm refrigerator magnet with NFC
    # # 5cm refrigerator magnet with NFC (no logo)
    # # 5cm refrigerator magnet with no NFC
    # # XXX - From here down are temporary samples to play with
    # 'QRSurround (9cm)': {
    #     'display_name': '',
    #     'description': 'Standard blah blah blah',
    #     'qr_size_x': 80,
    #     'qr_size_y': 80,
    #     'qr_size_z': 3,
    #     'no_draw_position': 'center',
    #     'no_draw_x': 35,
    #     'no_draw_y': 35,
    #     'change_filament_height': 3.1,
    # },
    # 'QRSurround (10cm)': {
    #     'display_name': '',
    #     'description': 'Standard blah blah blah',
    #     'qr_size_x': 100,
    #     'qr_size_y': 100,
    #     'qr_size_z': 3,
    #     'no_draw_position': 'center',
    #     'no_draw_x': 35,
    #     'no_draw_y': 35,
    #     'change_filament_height': 3.1,
    # },
    # 'QRSurround (12cm)': {
    #     'display_name': '',
    #     'description': 'Standard blah blah blah',
    #     'qr_size_x': 100,
    #     'qr_size_y': 100,
    #     'qr_size_z': 3,
    #     'no_draw_position': 'center',
    #     'no_draw_x': 35,
    #     'no_draw_y': 35,
    #     'change_filament_height': 3.1,
    # },
}
