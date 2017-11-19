#!/usr/bin/python3

import os
import numpy
import qrcode
import qrcode.image.base
from stl.mesh import Mesh
from stl.stl import Mode

from api.qrstl.background_model import BackgroundModel

class BackgroundNotFound(Exception):
    pass

class QRCodeSTL(qrcode.image.base.BaseImage):

    kind = "STL"
    allowed_kinds = ("STL")

    def __init__(self, *args, **kwargs):
        self._vertice_set = []
        # Initialize an empty mesh...
        self._mesh = None
        self.background_model = kwargs.pop('background_model',None)
        super().__init__(*args, **kwargs)

    @property
    def mesh(self):
        if self._mesh is None:
            self._mesh = Mesh.from_file(self.background_model.full_path_filename)
        return self._mesh

    @mesh.setter
    def mesh(self,mesh):
        self._mesh = mesh

    def drawrect(self,row,col):

        # Inversion to make the QR code come out as if x,y 0,0, is in the
        # top left corner rather than the lower left...
        invert_y_axis = True
        if invert_y_axis:
            row = (self.width - 1) - row

        # Individual pixel "cube" size...
        cube_size_x_mm = self.background_model.qr_size_x / self.width
        cube_size_y_mm = self.background_model.qr_size_y / self.width
        cube_size_z_mm = self.background_model.qr_size_z

        # ...and the exact start/end position of the pixel (in 3D space)...
        x_start = col * cube_size_x_mm
        x_end = x_start + cube_size_x_mm
        y_start = row * cube_size_y_mm
        y_end = y_start + cube_size_y_mm
        z_start = 0
        z_end = z_start + cube_size_z_mm

        # Calculation, and check for if this "pixel" is going to be within our reserved space for logo...
        if self.background_model.no_draw_position is not None:
            if self.background_model.no_draw_position == 'center':
                no_draw_start_x_mm = self.background_model.qr_size_x / 2 - self.background_model.no_draw_x / 2
                no_draw_end_x_mm = self.background_model.qr_size_x / 2 + self.background_model.no_draw_x / 2
                no_draw_start_y_mm = self.background_model.qr_size_y / 2 - self.background_model.no_draw_y / 2
                no_draw_end_y_mm = self.background_model.qr_size_y / 2 + self.background_model.no_draw_y / 2
            elif self.background_model.no_draw_position == 'centerleft':
                no_draw_start_x_mm = 0
                no_draw_end_x_mm = self.background_model.no_draw_x
                no_draw_start_y_mm = self.background_model.qr_size_y / 2 - self.background_model.no_draw_y / 2
                no_draw_end_y_mm = self.background_model.qr_size_y / 2 + self.background_model.no_draw_y / 2
            elif self.background_model.no_draw_position == 'centerright':
                no_draw_start_x_mm = self.background_model.qr_size_x - self.background_model.no_draw_x
                no_draw_end_x_mm = self.background_model.qr_size_x
                no_draw_start_y_mm = self.background_model.qr_size_y / 2 - self.background_model.no_draw_y / 2
                no_draw_end_y_mm = self.background_model.qr_size_y / 2 + self.background_model.no_draw_y / 2
            elif self.background_model.no_draw_position == 'topcenter':
                no_draw_start_x_mm = self.background_model.qr_size_x / 2 - self.background_model.no_draw_x / 2
                no_draw_end_x_mm = self.background_model.qr_size_x / 2 + self.background_model.no_draw_x / 2
                no_draw_start_y_mm = self.background_model.qr_size_y - self.background_model.no_draw_y
                no_draw_end_y_mm = self.background_model.qr_size_y
            elif self.background_model.no_draw_position == 'bottomcenter':
                no_draw_start_x_mm = self.background_model.qr_size_x / 2 - self.background_model.no_draw_x / 2
                no_draw_end_x_mm = self.background_model.qr_size_x / 2 + self.background_model.no_draw_x / 2
                no_draw_start_y_mm = 0
                no_draw_end_y_mm = self.background_model.no_draw_y
            elif self.background_model.no_draw_position == 'topleft':
                no_draw_start_x_mm = 0
                no_draw_end_x_mm = self.background_model.no_draw_x
                no_draw_start_y_mm = self.background_model.qr_size_y - self.background_model.no_draw_y
                no_draw_end_y_mm = self.background_model.qr_size_y
            elif self.background_model.no_draw_position == 'topright':
                no_draw_start_x_mm = self.background_model.qr_size_x - self.background_model.no_draw_x
                no_draw_end_x_mm = self.background_model.qr_size_x
                no_draw_start_y_mm = self.background_model.qr_size_y - self.background_model.no_draw_y
                no_draw_end_y_mm = self.background_model.qr_size_y
            elif self.background_model.no_draw_position == 'bottomleft':
                no_draw_start_x_mm = 0
                no_draw_end_x_mm = self.background_model.no_draw_x
                no_draw_start_y_mm = 0
                no_draw_end_y_mm = self.background_model.no_draw_y
            elif self.background_model.no_draw_position == 'bottomright':
                no_draw_start_x_mm = self.background_model.qr_size_x - self.background_model.no_draw_x
                no_draw_end_x_mm = self.background_model.qr_size_x
                no_draw_start_y_mm = 0
                no_draw_end_y_mm = self.background_model.no_draw_y
            else:
                raise Exception("Unknown self.background_model.no_draw_position: {}".format(self.background_model.no_draw_position))

            # If this pixel is being drawm in our no-draw area, then return, without doing anything...
            if ( ( x_start > no_draw_start_x_mm ) or ( x_end > no_draw_start_x_mm ) ) and ( ( x_start < no_draw_end_x_mm ) or ( x_end < no_draw_end_x_mm ) ):
                if ( ( y_start > no_draw_start_y_mm ) or ( y_end > no_draw_start_y_mm ) ) and ( ( y_start < no_draw_end_y_mm ) or ( y_end < no_draw_end_y_mm ) ):
                    return

        # Define the 12 triangles composing the cube
        double_triangle_cube_face = numpy.array([
            [0, 3, 1],
            [1, 3, 2],
            [0, 4, 7],
            [0, 7, 3],
            [4, 5, 6],
            [4, 6, 7],
            [5, 1, 2],
            [5, 2, 6],
            [2, 3, 6],
            [3, 7, 6],
            [0, 1, 5],
            [0, 5, 4]
        ])

        # Define the 8 vertices of the cube
        cube_vertices = numpy.array([
            [self.background_model.offset_x + x_start, self.background_model.offset_y + y_start, self.background_model.offset_z + z_start],
            [self.background_model.offset_x + x_end,   self.background_model.offset_y + y_start, self.background_model.offset_z + z_start],
            [self.background_model.offset_x + x_end,   self.background_model.offset_y + y_end,   self.background_model.offset_z + z_start],
            [self.background_model.offset_x + x_start, self.background_model.offset_y + y_end,   self.background_model.offset_z + z_start],
            [self.background_model.offset_x + x_start, self.background_model.offset_y + y_start, self.background_model.offset_z + z_end],
            [self.background_model.offset_x + x_end,   self.background_model.offset_y + y_start, self.background_model.offset_z + z_end],
            [self.background_model.offset_x + x_end,   self.background_model.offset_y + y_end,   self.background_model.offset_z + z_end],
            [self.background_model.offset_x + x_start, self.background_model.offset_y + y_end,   self.background_model.offset_z + z_end]
        ])

        # Create the mesh
        cube = Mesh(numpy.zeros(double_triangle_cube_face.shape[0], dtype=Mesh.dtype))
        for i, f in enumerate(double_triangle_cube_face):
            for j in range(len(double_triangle_cube_face[i])):
                cube.vectors[i][j] = cube_vertices[f[j], :]

        combined = Mesh(numpy.concatenate([self.mesh.data,cube.data]))
        self.mesh = combined

    def save(self, filename, fh=None, mode=Mode.BINARY, update_normals=True):
        self.mesh.save(filename,fh=fh,mode=mode,update_normals=update_normals)

    @classmethod
    def _generate_stl(cls, background_model_obj, data):

        qr_engine_obj = qrcode.QRCode(
            image_factory=QRCodeSTL,
        )

        qr_engine_obj.add_data(data)
        qr_stl_mesh_obj = qr_engine_obj.make_image(background_model=background_model_obj)

        return qr_stl_mesh_obj

    @classmethod
    def make_stl(cls, background_name, data):

        background_model = BackgroundModel.get_by_name(background_name)

        if background_model is None:
            raise BackgroundNotFound('Could not find specfified background model \"{}\"'.format(background_name))

        return cls._generate_stl(background_model,data)


# Running this file directly will output sample files...
if __name__ == '__main__':

    # Main execution...
    qr_data = 'http://www.qrstl.com'

    SAMPLE_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'samples')

    print("Generating samples for all known models to \"{}\"...".format(SAMPLE_OUTPUT_DIRECTORY))

    try:
        os.makedirs(SAMPLE_OUTPUT_DIRECTORY)
    except FileExistsError as ex:
        pass

    for x in BackgroundModel.all():
        print("Generating sample QR for \"{}\"...".format(x.name))
        qr_stl = QRCodeSTL.make_stl(x.name, qr_data)
        qr_stl.save('{}\\{}.stl'.format(SAMPLE_OUTPUT_DIRECTORY,x.name))
