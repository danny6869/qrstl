import os
import settings

import logging
log = logging.getLogger(__name__)

class BackgroundModel(object):

    # Set the directory our STL files are in to our file path /assets/background_models
    _background_directory = settings.BACKGROUND_FILE_DIRECTORY
    _background_extension = '.stl'

    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs.keys():
            setattr(self,key,kwargs[key])

    @classmethod
    def get_config(cls,filename):

        # Make sure we can actually read the file...
        if os.path.isfile(filename):

            # Setup our filename info bits into our initial config variables...
            extracted_file_path      = os.path.dirname(filename)
            extracted_file_extension = os.path.splitext(filename)[-1]
            extracted_filename       = filename[len(extracted_file_path) + 1:]
            extracted_name           = filename[len(extracted_file_path) + 1:-len(extracted_file_extension)]
            config_variables = {
                'full_path_filename' : filename,
                'directory'          : extracted_file_path,
                'extension'          : extracted_file_extension,
                'filename'           : extracted_filename,
                'name'               : extracted_name,
            }

            # Update our config variables with our settings...
            file_config = settings.BACKGROUND_FILE_ATTRIBUTES.get(extracted_name,None)
            if file_config:
                config_variables.update(settings.BACKGROUND_FILE_ATTRIBUTES.get('_DEFAULT'))
                config_variables.update(file_config)
                return config_variables
        else:
            log.error("File \"{}\" not found, or could not be accessed.".format(filename))

        log.error("No configuration found for \"{}\"".format(filename))
        return None

    @classmethod
    def from_full_path_filename(cls,full_path_filename):
        config = cls.get_config(full_path_filename)
        if config is None:
            return None
        new_obj = cls(**config)
        return new_obj

    @classmethod
    def from_filename(cls,filename):
        new_obj = cls.from_full_path_filename(os.path.join(cls._background_directory,filename))
        return new_obj

    @classmethod
    def get_by_name(cls,name):
        return cls.from_filename("{}{}".format(name,cls._background_extension))

    @classmethod
    def all(cls):

        object_list = []

        for filename in sorted(os.listdir(cls._background_directory)):
            if filename.endswith(cls._background_extension):
                new_obj = cls.from_filename(filename)
                if new_obj is not None:
                    object_list.append(new_obj)

        return object_list
