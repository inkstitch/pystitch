# items available at the top level (e.g. pystitch.read)
from .EmbConstant import *
from .EmbFunctions import *
from .EmbMatrix import EmbMatrix as EmbMatrix
from .EmbPattern import EmbPattern
from .EmbThread import EmbThread as EmbThread
from .EmbCompress import compress as compress, expand as expand

# items available in a sub-heirarchy (e.g. pystitch.PecGraphics.get_graphic_as_string)
from .PecGraphics import get_graphic_as_string as get_graphic_as_string
from .pystitch import *

# Lazy-load readers/writers on first access
import importlib as _importlib

name = "pystitch"

_LAZY_MODULES = {
    'GenericWriter', 'A10oReader', 'A100Reader', 'BroReader',
    'ColReader', 'ColWriter', 'CsvReader', 'CsvWriter',
    'DatReader', 'DsbReader', 'DstReader', 'DstWriter',
    'DszReader', 'EdrReader', 'EdrWriter', 'EmdReader',
    'ExpReader', 'ExpWriter', 'ExyReader', 'FxyReader',
    'GcodeReader', 'GcodeWriter', 'InkstitchGcodeWriter',
    'GtReader', 'HusReader', 'InbReader', 'InfReader', 'InfWriter',
    'IqpReader', 'JefReader', 'JefWriter', 'JpxReader',
    'JsonReader', 'JsonWriter', 'KsmReader', 'MaxReader',
    'MitReader', 'NewReader', 'PcdReader', 'PcmReader',
    'PcqReader', 'PcsReader', 'PecReader', 'PecWriter',
    'PesReader', 'PesWriter', 'PhbReader', 'PhcReader',
    'PltReader', 'PltWriter', 'PmvReader', 'PmvWriter',
    'PngWriter', 'QccReader', 'QccWriter', 'SewReader',
    'ShvReader', 'SpxReader', 'StcReader', 'StxReader',
    'SvgWriter', 'TapReader', 'TbfReader', 'TbfWriter',
    'TxtWriter', 'U01Reader', 'U01Writer', 'Vp3Reader',
    'Vp3Writer', 'XxxReader', 'XxxWriter', 'ZhsReader', 'ZxyReader',
}


def __getattr__(name):
    if name in _LAZY_MODULES:
        mod = _importlib.import_module(f'.{name}', __name__)
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Extension-to-module mapping for fast read/write dispatch (no eager imports)
_EXT_READER = {
    'pec': 'PecReader', 'pes': 'PesReader', 'exp': 'ExpReader',
    'dst': 'DstReader', 'jef': 'JefReader', 'vp3': 'Vp3Reader',
    'csv': 'CsvReader', 'xxx': 'XxxReader', 'sew': 'SewReader',
    'u00': 'U01Reader', 'u01': 'U01Reader', 'u02': 'U01Reader',
    'shv': 'ShvReader', '10o': 'A10oReader', '100': 'A100Reader', 'a100': 'A100Reader',
    'bro': 'BroReader', 'dat': 'DatReader', 'dsb': 'DsbReader',
    'dsz': 'DszReader', 'emd': 'EmdReader',
    'e00': 'ExyReader', 'e01': 'ExyReader', 'e02': 'ExyReader',
    'exy': 'ExyReader',
    'f00': 'FxyReader', 'f01': 'FxyReader', 'f02': 'FxyReader',
    'fxy': 'FxyReader',
    'gt': 'GtReader', 'inb': 'InbReader', 'tbf': 'TbfReader',
    'ksm': 'KsmReader', 'tap': 'TapReader', 'spx': 'SpxReader',
    'stx': 'StxReader', 'phb': 'PhbReader', 'phc': 'PhcReader',
    'new': 'NewReader', 'max': 'MaxReader', 'mit': 'MitReader',
    'pcd': 'PcdReader', 'pcq': 'PcqReader', 'pcm': 'PcmReader',
    'pcs': 'PcsReader', 'jpx': 'JpxReader', 'stc': 'StcReader',
    'zhs': 'ZhsReader',
    'z00': 'ZxyReader', 'z01': 'ZxyReader', 'z02': 'ZxyReader',
    'zxy': 'ZxyReader',
    'pmv': 'PmvReader', 'gcode': 'GcodeReader', 'g-code': 'GcodeReader',
    'ngc': 'GcodeReader', 'nc': 'GcodeReader', '.g': 'GcodeReader',
    'hus': 'HusReader', 'iqp': 'IqpReader', 'plt': 'PltReader',
    'qcc': 'QccReader', 'edr': 'EdrReader', 'col': 'ColReader',
    'inf': 'InfReader', 'json': 'JsonReader',
}
_EXT_WRITER = {
    'pec': 'PecWriter', 'pes': 'PesWriter', 'exp': 'ExpWriter',
    'dst': 'DstWriter', 'jef': 'JefWriter', 'vp3': 'Vp3Writer',
    'svg': 'SvgWriter', 'svgz': 'SvgWriter', 'csv': 'CsvWriter',
    'xxx': 'XxxWriter', 'u00': 'U01Writer', 'u01': 'U01Writer',
    'u02': 'U01Writer', 'tbf': 'TbfWriter', 'pmv': 'PmvWriter',
    'png': 'PngWriter', 'txt': 'TxtWriter',
    'gcode': 'InkstitchGcodeWriter', 'g-code': 'InkstitchGcodeWriter',
    'ngc': 'InkstitchGcodeWriter', 'nc': 'InkstitchGcodeWriter',
    '.g': 'InkstitchGcodeWriter',
    'plt': 'PltWriter', 'qcc': 'QccWriter',
    'edr': 'EdrWriter', 'col': 'ColWriter', 'inf': 'InfWriter',
    'json': 'JsonWriter',
}

def _get_reader(ext):
    name = _EXT_READER.get(ext)
    if name is None:
        return None
    mod = __getattr__(name)
    return mod

def _get_writer(ext):
    name = _EXT_WRITER.get(ext)
    if name is None:
        return None
    mod = __getattr__(name)
    return mod

def read(filename, settings=None, pattern=None):
    """Reads file, assuming type by extension"""
    extension = EmbPattern.get_extension_by_filename(filename)
    extension = extension.lower()
    reader = _get_reader(extension)
    if reader is not None:
        return EmbPattern.read_embroidery(reader, filename, settings, pattern)
    return None


def write(pattern, filename, settings=None):
    """Writes file, assuming type by extension"""
    extension = EmbPattern.get_extension_by_filename(filename)
    extension = extension.lower()
    writer = _get_writer(extension)
    if writer is not None:
        EmbPattern.write_embroidery(writer, pattern, filename, settings)
        return
    raise IOError("Conversion to file type '{extension}' is not supported".format(extension=extension))

def convert(filename_from, filename_to, settings=None):
    pattern = read(filename_from, settings)
    if pattern is None:
        return
    write(pattern, filename_to, settings)

_supported_formats_cache = None

def supported_formats():
    """Generates dictionary entries for supported formats. Each entry will
    always have description, extension, mimetype, and category. Reader
    will provide the reader, if one exists, writer will provide the writer,
    if one exists.

    Metadata gives a list of metadata read and/or written by that type.

    Options provides accepted options by the format and their accepted values.
    """
    global _supported_formats_cache
    if _supported_formats_cache is not None:
        return _supported_formats_cache
    _supported_formats_cache = list(_generate_supported_formats())
    return _supported_formats_cache

def _generate_supported_formats():
    # Helper to lazy-resolve reader/writer modules
    def _r(name):
        g = globals()
        if name not in g:
            __getattr__(name)
        return g[name]
    # yield ({
    #     "description": "Art Embroidery Format",
    #     "extension": "art",
    #     "extensions": ("art",),
    #     "mimetype": "application/x-art",
    #     "category": "embroidery",
    #     "reader": _r('ArtReader'),
    #     "metadata": ("name")
    # })
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "pec",
            "extensions": ("pec",),
            "mimetype": "application/x-pec",
            "category": "embroidery",
            "reader": _r('PecReader'),
            "writer": _r('PecWriter'),
            "metadata": ("name"),
        }
    )
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "pes",
            "extensions": ("pes",),
            "mimetype": "application/x-pes",
            "category": "embroidery",
            "reader": _r('PesReader'),
            "writer": _r('PesWriter'),
            "versions": ("1", "6", "1t", "6t"),
            "metadata": ("name", "author", "category", "keywords", "comments"),
        }
    )
    yield (
        {
            "description": "Melco Expanded Embroidery Format",
            "extension": "exp",
            "extensions": ("exp",),
            "mimetype": "application/x-exp",
            "category": "embroidery",
            "reader": _r('ExpReader'),
            "writer": _r('ExpWriter'),
        }
    )
    # yield (
    #     {
    #         "description": "Melco Condensed Embroidery Format",
    #         "extension": "cnd",
    #         "extensions": ("cnd",),
    #         "mimetype": "application/x-cnd",
    #         "category": "embroidery",
    #         "reader": _r('CndReader'),
    #     }
    # )
    yield (
        {
            "description": "Tajima Embroidery Format",
            "extension": "dst",
            "extensions": ("dst",),
            "mimetype": "application/x-dst",
            "category": "embroidery",
            "reader": _r('DstReader'),
            "writer": _r('DstWriter'),
            "read_options": {
                "trim_distance": (None, 3.0, 50.0),
                "trim_at": (2, 3, 4, 5, 6, 7, 8),
                "clipping": (True, False),
            },
            "write_options": {"trim_at": (2, 3, 4, 5, 6, 7, 8)},
            "versions": ("default", "extended"),
            "metadata": ("name", "author", "copyright"),
        }
    )
    yield (
        {
            "description": "Janome Embroidery Format",
            "extension": "jef",
            "extensions": ("jef",),
            "mimetype": "application/x-jef",
            "category": "embroidery",
            "reader": _r('JefReader'),
            "writer": _r('JefWriter'),
            "read_options": {
                "trim_distance": (None, 3.0, 50.0),
                "trims": (True, False),
                "trim_at": (2, 3, 4, 5, 6, 7, 8),
                "clipping": (True, False),
            },
            "write_options": {
                "trims": (True, False),
                "trim_at": (2, 3, 4, 5, 6, 7, 8),
            },
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "vp3",
            "extensions": ("vp3",),
            "mimetype": "application/x-vp3",
            "category": "embroidery",
            "reader": _r('Vp3Reader'),
            "writer": _r('Vp3Writer'),
        }
    )
    yield (
        {
            "description": "Scalable Vector Graphics",
            "extension": "svg",
            "extensions": ("svg", "svgz"),
            "mimetype": "image/svg+xml",
            "category": "vector",
            "writer": _r('SvgWriter'),
        }
    )
    yield (
        {
            "description": "Comma-separated values",
            "extension": "csv",
            "extensions": ("csv",),
            "mimetype": "text/csv",
            "category": "debug",
            "reader": _r('CsvReader'),
            "writer": _r('CsvWriter'),
            "versions": ("default", "delta", "full"),
        }
    )
    yield (
        {
            "description": "Singer Embroidery Format",
            "extension": "xxx",
            "extensions": ("xxx",),
            "mimetype": "application/x-xxx",
            "category": "embroidery",
            "reader": _r('XxxReader'),
            "writer": _r('XxxWriter'),
        }
    )
    yield (
        {
            "description": "Janome Embroidery Format",
            "extension": "sew",
            "extensions": ("sew",),
            "mimetype": "application/x-sew",
            "category": "embroidery",
            "reader": _r('SewReader'),
        }
    )
    yield (
        {
            "description": "Barudan Embroidery Format",
            "extension": "u01",
            "extensions": ("u00", "u01", "u02"),
            "mimetype": "application/x-u01",
            "category": "embroidery",
            "reader": _r('U01Reader'),
            "writer": _r('U01Writer'),
        }
    )
    yield (
        {
            "description": "Husqvarna Viking Embroidery Format",
            "extension": "shv",
            "extensions": ("shv",),
            "mimetype": "application/x-shv",
            "category": "embroidery",
            "reader": _r('ShvReader'),
        }
    )
    yield (
        {
            "description": "Toyota Embroidery Format",
            "extension": "10o",
            "extensions": ("10o",),
            "mimetype": "application/x-10o",
            "category": "embroidery",
            "reader": _r('A10oReader'),
        }
    )
    yield (
        {
            "description": "Toyota Embroidery Format",
            "extension": "100",
            "extensions": ("100",),
            "mimetype": "application/x-100",
            "category": "embroidery",
            "reader": _r('A100Reader'),
        }
    )
    yield (
        {
            "description": "Bits & Volts Embroidery Format",
            "extension": "bro",
            "extensions": ("bro",),
            "mimetype": "application/x-Bro",
            "category": "embroidery",
            "reader": _r('BroReader'),
        }
    )
    yield (
        {
            "description": "Sunstar or Barudan Embroidery Format",
            "extension": "dat",
            "extensions": ("dat",),
            "mimetype": "application/x-dat",
            "category": "embroidery",
            "reader": _r('DatReader'),
        }
    )
    yield (
        {
            "description": "Tajima(Barudan) Embroidery Format",
            "extension": "dsb",
            "extensions": ("dsb",),
            "mimetype": "application/x-dsb",
            "category": "embroidery",
            "reader": _r('DsbReader'),
        }
    )
    yield (
        {
            "description": "ZSK USA Embroidery Format",
            "extension": "dsz",
            "extensions": ("dsz",),
            "mimetype": "application/x-dsz",
            "category": "embroidery",
            "reader": _r('DszReader'),
        }
    )
    yield (
        {
            "description": "Elna Embroidery Format",
            "extension": "emd",
            "extensions": ("emd",),
            "mimetype": "application/x-emd",
            "category": "embroidery",
            "reader": _r('EmdReader'),
        }
    )
    yield (
        {
            "description": "Eltac Embroidery Format",
            "extension": "exy",  # e??, e01
            "extensions": ("e00", "e01", "e02"),
            "mimetype": "application/x-exy",
            "category": "embroidery",
            "reader": _r('ExyReader'),
        }
    )
    yield (
        {
            "description": "Fortron Embroidery Format",
            "extension": "fxy",  # f??, f01
            "extensions": ("f00", "f01", "f02"),
            "mimetype": "application/x-fxy",
            "category": "embroidery",
            "reader": _r('FxyReader'),
        }
    )
    yield (
        {
            "description": "Gold Thread Embroidery Format",
            "extension": "gt",
            "extensions": ("gt",),
            "mimetype": "application/x-exy",
            "category": "embroidery",
            "reader": _r('GtReader'),
        }
    )
    yield (
        {
            "description": "Inbro Embroidery Format",
            "extension": "inb",
            "extensions": ("inb",),
            "mimetype": "application/x-inb",
            "category": "embroidery",
            "reader": _r('InbReader'),
        }
    )
    yield (
        {
            "description": "Tajima Embroidery Format",
            "extension": "tbf",
            "extensions": ("tbf",),
            "mimetype": "application/x-tbf",
            "category": "embroidery",
            "reader": _r('TbfReader'),
            "writer": _r('TbfWriter'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "ksm",
            "extensions": ("ksm",),
            "mimetype": "application/x-ksm",
            "category": "embroidery",
            "reader": _r('KsmReader'),
        }
    )
    yield (
        {
            "description": "Happy Embroidery Format",
            "extension": "tap",
            "extensions": ("tap",),
            "mimetype": "application/x-tap",
            "category": "embroidery",
            "reader": _r('TapReader'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "spx",
            "extensions": ("spx"),
            "mimetype": "application/x-spx",
            "category": "embroidery",
            "reader": _r('SpxReader'),
        }
    )
    yield (
        {
            "description": "Data Stitch Embroidery Format",
            "extension": "stx",
            "extensions": ("stx",),
            "mimetype": "application/x-stx",
            "category": "embroidery",
            "reader": _r('StxReader'),
        }
    )
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "phb",
            "extensions": ("phb",),
            "mimetype": "application/x-phb",
            "category": "embroidery",
            "reader": _r('PhbReader'),
        }
    )
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "phc",
            "extensions": ("phc",),
            "mimetype": "application/x-phc",
            "category": "embroidery",
            "reader": _r('PhcReader'),
        }
    )
    yield (
        {
            "description": "Ameco Embroidery Format",
            "extension": "new",
            "extensions": ("new",),
            "mimetype": "application/x-new",
            "category": "embroidery",
            "reader": _r('NewReader'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "max",
            "extensions": ("max",),
            "mimetype": "application/x-max",
            "category": "embroidery",
            "reader": _r('MaxReader'),
        }
    )
    yield (
        {
            "description": "Mitsubishi Embroidery Format",
            "extension": "mit",
            "extensions": ("mit",),
            "mimetype": "application/x-mit",
            "category": "embroidery",
            "reader": _r('MitReader'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcd",
            "extensions": ("pcd",),
            "mimetype": "application/x-pcd",
            "category": "embroidery",
            "reader": _r('PcdReader'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcq",
            "extensions": ("pcq",),
            "mimetype": "application/x-pcq",
            "category": "embroidery",
            "reader": _r('PcqReader'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcm",
            "extensions": ("pcm",),
            "mimetype": "application/x-pcm",
            "category": "embroidery",
            "reader": _r('PcmReader'),
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcs",
            "extensions": ("pcs",),
            "mimetype": "application/x-pcs",
            "category": "embroidery",
            "reader": _r('PcsReader'),
        }
    )
    yield (
        {
            "description": "Janome Embroidery Format",
            "extension": "jpx",
            "extensions": ("jpx",),
            "mimetype": "application/x-jpx",
            "category": "embroidery",
            "reader": _r('JpxReader'),
        }
    )
    yield (
        {
            "description": "Gunold Embroidery Format",
            "extension": "stc",
            "extensions": ("stc",),
            "mimetype": "application/x-stc",
            "category": "embroidery",
            "reader": _r('StcReader'),
        }
    )
    yield ({
        "description": "Zeng Hsing Embroidery Format",
        "extension": "zhs",
        "extensions": ("zhs",),
        "mimetype": "application/x-zhs",
        "category": "embroidery",
        "reader": _r('ZhsReader')
    })
    yield (
        {
            "description": "ZSK TC Embroidery Format",
            "extension": "zxy",
            "extensions": ("z00", "z01", "z02"),
            "mimetype": "application/x-zxy",
            "category": "embroidery",
            "reader": _r('ZxyReader'),
        }
    )
    yield (
        {
            "description": "Brother Stitch Format",
            "extension": "pmv",
            "extensions": ("pmv",),
            "mimetype": "application/x-pmv",
            "category": "stitch",
            "reader": _r('PmvReader'),
            "writer": _r('PmvWriter'),
        }
    )
    yield (
        {
            "description": "PNG Format, Portable Network Graphics",
            "extension": "png",
            "extensions": ("png",),
            "mimetype": "image/png",
            "category": "image",
            "writer": _r('PngWriter'),
            "write_options": {
                "background": (0x000000, 0xFFFFFF),
                "linewidth": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            },
        }
    )
    yield (
        {
            "description": "txt Format, Text File",
            "extension": "txt",
            "extensions": ("txt",),
            "mimetype": "text/plain",
            "category": "debug",
            "writer": _r('TxtWriter'),
            "versions": ("default", "embroidermodder"),
        }
    )
    yield (
        {
            "description": "gcode Format, Text File",
            "extension": "gcode",
            "extensions": ("gcode", "g-code", "ngc", "nc", ".g"),
            "mimetype": "text/plain",
            "category": "embroidery",
            "reader": _r('GcodeReader'),
            "writer": _r('InkstitchGcodeWriter'),
            "write_options": {
                "flip_x": (True, False),
                "flip_y": (True, False),
                "alternate_z": (True, False),
                "stitch_z_travel": (int),
            },
        }
    )
    yield (
        {
            "description": "Husqvarna Embroidery Format",
            "extension": "hus",
            "extensions": ("hus",),
            "mimetype": "application/x-hus",
            "category": "embroidery",
            "reader": _r('HusReader'),
        }
    )
    yield(
        {
            "description": "Iqp - Intelliquilter Format",
            "extension": "iqp",
            "extensions": ("iqp",),
            "mimetype": "application/x-iqp",
            "category": "quilting",
            "reader": _r('IqpReader'),
        }
    )
    yield(
        {
            "description": "Plt - HPGL",
            "extension": "plt",
            "extensions": ("plt",),
            "mimetype": "text/plain",
            "category": "quilting",
            "reader": _r('PltReader'),
            "writer": _r('PltWriter'),
        }
    )
    yield(
        {
            "description": "Qcc - QuiltEZ",
            "extension": "qcc",
            "extensions": ("qcc",),
            "mimetype": "text/plain",
            "category": "quilting",
            "reader": _r('QccReader'),
            "writer": _r('QccWriter'),
        }
    )
    yield (
        {
            "description": "Edr Color Format",
            "extension": "edr",
            "extensions": ("edr",),
            "mimetype": "application/x-edr",
            "category": "color",
            "reader": _r('EdrReader'),
            "writer": _r('EdrWriter'),
        }
    )
    yield (
        {
            "description": "Col Color Format",
            "extension": "col",
            "extensions": ("col",),
            "mimetype": "application/x-col",
            "category": "color",
            "reader": _r('ColReader'),
            "writer": _r('ColWriter'),
        }
    )
    yield (
        {
            "description": "Inf Color Format",
            "extension": "inf",
            "extensions": ("inf",),
            "mimetype": "application/x-inf",
            "category": "color",
            "reader": _r('InfReader'),
            "writer": _r('InfWriter'),
        }
    )
    yield (
        {
            "description": "Json Export",
            "extension": "json",
            "extensions": ("json",),
            "mimetype": "application/json",
            "category": "debug",
            "reader": _r('JsonReader'),
            "writer": _r('JsonWriter'),
        }
    )

def read_dst(f, settings=None, pattern=None):
    """Reads fileobject as DST file"""
    return EmbPattern.read_embroidery(__getattr__('DstReader'), f, settings, pattern)

def read_pec(f, settings=None, pattern=None):
    """Reads fileobject as PEC file"""
    return EmbPattern.read_embroidery(__getattr__('PecReader'), f, settings, pattern)

def read_pes(f, settings=None, pattern=None):
    """Reads fileobject as PES file"""
    return EmbPattern.read_embroidery(__getattr__('PesReader'), f, settings, pattern)

def read_exp(f, settings=None, pattern=None):
    """Reads fileobject as EXP file"""
    return EmbPattern.read_embroidery(__getattr__('ExpReader'), f, settings, pattern)

def read_vp3(f, settings=None, pattern=None):
    """Reads fileobject as VP3 file"""
    return EmbPattern.read_embroidery(__getattr__('Vp3Reader'), f, settings, pattern)

def read_jef(f, settings=None, pattern=None):
    """Reads fileobject as JEF file"""
    return EmbPattern.read_embroidery(__getattr__('JefReader'), f, settings, pattern)

def read_u01(f, settings=None, pattern=None):
    """Reads fileobject as U01 file"""
    return EmbPattern.read_embroidery(__getattr__('U01Reader'), f, settings, pattern)

def read_csv(f, settings=None, pattern=None):
    """Reads fileobject as CSV file"""
    return EmbPattern.read_embroidery(__getattr__('CsvReader'), f, settings, pattern)

def read_json(f, settings=None, pattern=None):
    """Reads fileobject as JSON file"""
    return EmbPattern.read_embroidery(__getattr__('JsonReader'), f, settings, pattern)

def read_gcode(f, settings=None, pattern=None):
    """Reads fileobject as GCode file"""
    return EmbPattern.read_embroidery(__getattr__('GcodeReader'), f, settings, pattern)

def read_xxx(f, settings=None, pattern=None):
    """Reads fileobject as XXX file"""
    return EmbPattern.read_embroidery(__getattr__('XxxReader'), f, settings, pattern)

def read_tbf(f, settings=None, pattern=None):
    """Reads fileobject as TBF file"""
    return EmbPattern.read_embroidery(__getattr__('TbfReader'), f, settings, pattern)

def read_iqp(f, settings=None, pattern=None):
    """Reads fileobject as IQP file"""
    pattern = EmbPattern.read_embroidery(__getattr__('IqpReader'), f, settings, pattern)
    return pattern

def read_plt(f, settings=None, pattern=None):
    """Reads fileobject as PLT file"""
    pattern = EmbPattern.read_embroidery(__getattr__('PltReader'), f, settings, pattern)
    return pattern

def read_qcc(f, settings=None, pattern=None):
    """Reads fileobject as QCC file"""
    pattern = EmbPattern.read_embroidery(__getattr__('QccReader'), f, settings, pattern)
    return pattern

def write_dst(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    EmbPattern.write_embroidery(__getattr__('DstWriter'), pattern, stream, settings)

def write_pec(pattern, stream, settings=None):
    """Writes fileobject as PEC file"""
    EmbPattern.write_embroidery(__getattr__('PecWriter'), pattern, stream, settings)

def write_pes(pattern, stream, settings=None):
    """Writes fileobject as PES file"""
    EmbPattern.write_embroidery(__getattr__('PesWriter'), pattern, stream, settings)

def write_exp(pattern, stream, settings=None):
    """Writes fileobject as EXP file"""
    EmbPattern.write_embroidery(__getattr__('ExpWriter'), pattern, stream, settings)

def write_vp3(pattern, stream, settings=None):
    """Writes fileobject as Vp3 file"""
    EmbPattern.write_embroidery(__getattr__('Vp3Writer'), pattern, stream, settings)

def write_jef(pattern, stream, settings=None):
    """Writes fileobject as JEF file"""
    EmbPattern.write_embroidery(__getattr__('JefWriter'), pattern, stream, settings)

def write_u01(pattern, stream, settings=None):
    """Writes fileobject as U01 file"""
    EmbPattern.write_embroidery(__getattr__('U01Writer'), pattern, stream, settings)

def write_csv(pattern, stream, settings=None):
    """Writes fileobject as CSV file"""
    EmbPattern.write_embroidery(__getattr__('CsvWriter'), pattern, stream, settings)

def write_json(pattern, stream, settings=None):
    """Writes fileobject as JSON file"""
    EmbPattern.write_embroidery(__getattr__('JsonWriter'), pattern, stream, settings)

def write_txt(pattern, stream, settings=None):
    """Writes fileobject as CSV file"""
    EmbPattern.write_embroidery(__getattr__('TxtWriter'), pattern, stream, settings)

def write_gcode(pattern, stream, settings=None):
    """Writes fileobject as Gcode file"""
    EmbPattern.write_embroidery(__getattr__('GcodeWriter'), pattern, stream, settings)

def write_xxx(pattern, stream, settings=None):
    """Writes fileobject as XXX file"""
    EmbPattern.write_embroidery(__getattr__('XxxWriter'), pattern, stream, settings)

def write_tbf(pattern, stream, settings=None):
    """Writes fileobject as TBF file"""
    EmbPattern.write_embroidery(__getattr__('TbfWriter'), pattern, stream, settings)

def write_plt(pattern, stream, settings=None):
    """Writes fileobject as PLT file"""
    EmbPattern.write_embroidery(__getattr__('PltWriter'), pattern, stream, settings)

def write_qcc(pattern, stream, settings=None):
    """Writes fileobject as QCC file"""
    EmbPattern.write_embroidery(__getattr__('QccWriter'), pattern, stream, settings)

def write_svg(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    EmbPattern.write_embroidery(__getattr__('SvgWriter'), pattern, stream, settings)

def write_png(pattern, stream, settings=None):
    """Writes fileobject as PNG file"""
    EmbPattern.write_embroidery(__getattr__('PngWriter'), pattern, stream, settings)
