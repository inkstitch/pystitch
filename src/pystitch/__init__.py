name = "pystitch"

# items available at the top level (e.g. pystitch.read)
from .EmbConstant import *
from .EmbFunctions import *
from .EmbMatrix import EmbMatrix
from .EmbPattern import EmbPattern
from .EmbThread import EmbThread
from .EmbCompress import compress, expand
import pystitch.GenericWriter as GenericWriter

# items available in a sub-heirarchy (e.g. pystitch.PecGraphics.get_graphic_as_string)
from .PecGraphics import get_graphic_as_string
from .pystitch import *

import pystitch.A10oReader as A10oReader
import pystitch.A100Reader as A100Reader
# pystitch.ArtReader as ArtReader
import pystitch.BroReader as BroReader
import pystitch.ColReader as ColReader
import pystitch.ColWriter as ColWriter
import pystitch.CsvReader as CsvReader
import pystitch.CsvWriter as CsvWriter
import pystitch.DatReader as DatReader
import pystitch.DsbReader as DsbReader
import pystitch.DstReader as DstReader
import pystitch.DstWriter as DstWriter
import pystitch.DszReader as DszReader
import pystitch.EdrReader as EdrReader
import pystitch.EdrWriter as EdrWriter
import pystitch.EmdReader as EmdReader
import pystitch.ExpReader as ExpReader
import pystitch.ExpWriter as ExpWriter
import pystitch.ExyReader as ExyReader
import pystitch.FxyReader as FxyReader
import pystitch.GcodeReader as GcodeReader
import pystitch.GcodeWriter as GcodeWriter
import pystitch.InkstitchGcodeWriter as InkstitchGcodeWriter
import pystitch.GtReader as GtReader
import pystitch.HusReader as HusReader
import pystitch.InbReader as InbReader
import pystitch.InfReader as InfReader
import pystitch.InfWriter as InfWriter
import pystitch.IqpReader as IqpReader
import pystitch.JefReader as JefReader
import pystitch.JefWriter as JefWriter
import pystitch.JpxReader as JpxReader
import pystitch.JsonReader as JsonReader
import pystitch.JsonWriter as JsonWriter
import pystitch.KsmReader as KsmReader
import pystitch.MaxReader as MaxReader
import pystitch.MitReader as MitReader
import pystitch.NewReader as NewReader
import pystitch.PcdReader as PcdReader
import pystitch.PcmReader as PcmReader
import pystitch.PcqReader as PcqReader
import pystitch.PcsReader as PcsReader
import pystitch.PecReader as PecReader
import pystitch.PecWriter as PecWriter
import pystitch.PesReader as PesReader
import pystitch.PesWriter as PesWriter
import pystitch.PhbReader as PhbReader
import pystitch.PhcReader as PhcReader
import pystitch.PltReader as PltReader
import pystitch.PltWriter as PltWriter
import pystitch.PmvReader as PmvReader
import pystitch.PmvWriter as PmvWriter
import pystitch.PngWriter as PngWriter
import pystitch.QccReader as QccReader
import pystitch.QccWriter as QccWriter
import pystitch.SewReader as SewReader
import pystitch.ShvReader as ShvReader
import pystitch.SpxReader as SpxReader
import pystitch.StcReader as StcReader
import pystitch.StxReader as StxReader
import pystitch.SvgWriter as SvgWriter
import pystitch.TapReader as TapReader
import pystitch.TbfReader as TbfReader
import pystitch.TbfWriter as TbfWriter
import pystitch.TxtWriter as TxtWriter
import pystitch.U01Reader as U01Reader
import pystitch.U01Writer as U01Writer
import pystitch.Vp3Reader as Vp3Reader
import pystitch.Vp3Writer as Vp3Writer
import pystitch.XxxReader as XxxReader
import pystitch.XxxWriter as XxxWriter
import pystitch.ZhsReader as ZhsReader
import pystitch.ZxyReader as ZxyReader


def read(filename, settings=None, pattern=None):
    """Reads file, assuming type by extension"""
    extension = EmbPattern.get_extension_by_filename(filename)
    extension = extension.lower()
    for file_type in supported_formats():
        if file_type["extension"] != extension:
            continue
        reader = file_type.get("reader", None)
        return EmbPattern.read_embroidery(reader, filename, settings, pattern)
    return None


def write(pattern, filename, settings=None):
    """Writes file, assuming type by extension"""
    extension = EmbPattern.get_extension_by_filename(filename)
    extension = extension.lower()
    supported_extensions = [file_type["extension"] for file_type in supported_formats()]

    if extension not in supported_extensions:
        raise IOError("Conversion to file type '{extension}' is not supported".format(extension=extension))

    ext_to_file_type_lookup = {file_type["extension"]: file_type for file_type in supported_formats()}
    writer = ext_to_file_type_lookup[extension].get("writer")

    if writer:
        EmbPattern.write_embroidery(writer, pattern, filename, settings)
    else:
        raise IOError("No supported writer found.")

def convert(filename_from, filename_to, settings=None):
    pattern = read(filename_from, settings)
    if pattern is None:
        return
    write(pattern, filename_to, settings)

def supported_formats():
    """Generates dictionary entries for supported formats. Each entry will
    always have description, extension, mimetype, and category. Reader
    will provide the reader, if one exists, writer will provide the writer,
    if one exists.

    Metadata gives a list of metadata read and/or written by that type.

    Options provides accepted options by the format and their accepted values.
    """
    # yield ({
    #     "description": "Art Embroidery Format",
    #     "extension": "art",
    #     "extensions": ("art",),
    #     "mimetype": "application/x-art",
    #     "category": "embroidery",
    #     "reader": ArtReader,
    #     "metadata": ("name")
    # })
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "pec",
            "extensions": ("pec",),
            "mimetype": "application/x-pec",
            "category": "embroidery",
            "reader": PecReader,
            "writer": PecWriter,
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
            "reader": PesReader,
            "writer": PesWriter,
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
            "reader": ExpReader,
            "writer": ExpWriter,
        }
    )
    # yield (
    #     {
    #         "description": "Melco Condensed Embroidery Format",
    #         "extension": "cnd",
    #         "extensions": ("cnd",),
    #         "mimetype": "application/x-cnd",
    #         "category": "embroidery",
    #         "reader": CndReader,
    #     }
    # )
    yield (
        {
            "description": "Tajima Embroidery Format",
            "extension": "dst",
            "extensions": ("dst",),
            "mimetype": "application/x-dst",
            "category": "embroidery",
            "reader": DstReader,
            "writer": DstWriter,
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
            "reader": JefReader,
            "writer": JefWriter,
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
            "reader": Vp3Reader,
            "writer": Vp3Writer,
        }
    )
    yield (
        {
            "description": "Scalable Vector Graphics",
            "extension": "svg",
            "extensions": ("svg", "svgz"),
            "mimetype": "image/svg+xml",
            "category": "vector",
            "writer": SvgWriter,
        }
    )
    yield (
        {
            "description": "Comma-separated values",
            "extension": "csv",
            "extensions": ("csv",),
            "mimetype": "text/csv",
            "category": "debug",
            "reader": CsvReader,
            "writer": CsvWriter,
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
            "reader": XxxReader,
            "writer": XxxWriter,
        }
    )
    yield (
        {
            "description": "Janome Embroidery Format",
            "extension": "sew",
            "extensions": ("sew",),
            "mimetype": "application/x-sew",
            "category": "embroidery",
            "reader": SewReader,
        }
    )
    yield (
        {
            "description": "Barudan Embroidery Format",
            "extension": "u01",
            "extensions": ("u00", "u01", "u02"),
            "mimetype": "application/x-u01",
            "category": "embroidery",
            "reader": U01Reader,
            "writer": U01Writer,
        }
    )
    yield (
        {
            "description": "Husqvarna Viking Embroidery Format",
            "extension": "shv",
            "extensions": ("shv",),
            "mimetype": "application/x-shv",
            "category": "embroidery",
            "reader": ShvReader,
        }
    )
    yield (
        {
            "description": "Toyota Embroidery Format",
            "extension": "10o",
            "extensions": ("10o",),
            "mimetype": "application/x-10o",
            "category": "embroidery",
            "reader": A10oReader,
        }
    )
    yield (
        {
            "description": "Toyota Embroidery Format",
            "extension": "100",
            "extensions": ("100",),
            "mimetype": "application/x-100",
            "category": "embroidery",
            "reader": A100Reader,
        }
    )
    yield (
        {
            "description": "Bits & Volts Embroidery Format",
            "extension": "bro",
            "extensions": ("bro",),
            "mimetype": "application/x-Bro",
            "category": "embroidery",
            "reader": BroReader,
        }
    )
    yield (
        {
            "description": "Sunstar or Barudan Embroidery Format",
            "extension": "dat",
            "extensions": ("dat",),
            "mimetype": "application/x-dat",
            "category": "embroidery",
            "reader": DatReader,
        }
    )
    yield (
        {
            "description": "Tajima(Barudan) Embroidery Format",
            "extension": "dsb",
            "extensions": ("dsb",),
            "mimetype": "application/x-dsb",
            "category": "embroidery",
            "reader": DsbReader,
        }
    )
    yield (
        {
            "description": "ZSK USA Embroidery Format",
            "extension": "dsz",
            "extensions": ("dsz",),
            "mimetype": "application/x-dsz",
            "category": "embroidery",
            "reader": DszReader,
        }
    )
    yield (
        {
            "description": "Elna Embroidery Format",
            "extension": "emd",
            "extensions": ("emd",),
            "mimetype": "application/x-emd",
            "category": "embroidery",
            "reader": EmdReader,
        }
    )
    yield (
        {
            "description": "Eltac Embroidery Format",
            "extension": "exy",  # e??, e01
            "extensions": ("e00", "e01", "e02"),
            "mimetype": "application/x-exy",
            "category": "embroidery",
            "reader": ExyReader,
        }
    )
    yield (
        {
            "description": "Fortron Embroidery Format",
            "extension": "fxy",  # f??, f01
            "extensions": ("f00", "f01", "f02"),
            "mimetype": "application/x-fxy",
            "category": "embroidery",
            "reader": FxyReader,
        }
    )
    yield (
        {
            "description": "Gold Thread Embroidery Format",
            "extension": "gt",
            "extensions": ("gt",),
            "mimetype": "application/x-exy",
            "category": "embroidery",
            "reader": GtReader,
        }
    )
    yield (
        {
            "description": "Inbro Embroidery Format",
            "extension": "inb",
            "extensions": ("inb",),
            "mimetype": "application/x-inb",
            "category": "embroidery",
            "reader": InbReader,
        }
    )
    yield (
        {
            "description": "Tajima Embroidery Format",
            "extension": "tbf",
            "extensions": ("tbf",),
            "mimetype": "application/x-tbf",
            "category": "embroidery",
            "reader": TbfReader,
            "writer": TbfWriter,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "ksm",
            "extensions": ("ksm",),
            "mimetype": "application/x-ksm",
            "category": "embroidery",
            "reader": KsmReader,
        }
    )
    yield (
        {
            "description": "Happy Embroidery Format",
            "extension": "tap",
            "extensions": ("tap",),
            "mimetype": "application/x-tap",
            "category": "embroidery",
            "reader": TapReader,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "spx",
            "extensions": ("spx"),
            "mimetype": "application/x-spx",
            "category": "embroidery",
            "reader": SpxReader,
        }
    )
    yield (
        {
            "description": "Data Stitch Embroidery Format",
            "extension": "stx",
            "extensions": ("stx",),
            "mimetype": "application/x-stx",
            "category": "embroidery",
            "reader": StxReader,
        }
    )
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "phb",
            "extensions": ("phb",),
            "mimetype": "application/x-phb",
            "category": "embroidery",
            "reader": PhbReader,
        }
    )
    yield (
        {
            "description": "Brother Embroidery Format",
            "extension": "phc",
            "extensions": ("phc",),
            "mimetype": "application/x-phc",
            "category": "embroidery",
            "reader": PhcReader,
        }
    )
    yield (
        {
            "description": "Ameco Embroidery Format",
            "extension": "new",
            "extensions": ("new",),
            "mimetype": "application/x-new",
            "category": "embroidery",
            "reader": NewReader,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "max",
            "extensions": ("max",),
            "mimetype": "application/x-max",
            "category": "embroidery",
            "reader": MaxReader,
        }
    )
    yield (
        {
            "description": "Mitsubishi Embroidery Format",
            "extension": "mit",
            "extensions": ("mit",),
            "mimetype": "application/x-mit",
            "category": "embroidery",
            "reader": MitReader,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcd",
            "extensions": ("pcd",),
            "mimetype": "application/x-pcd",
            "category": "embroidery",
            "reader": PcdReader,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcq",
            "extensions": ("pcq",),
            "mimetype": "application/x-pcq",
            "category": "embroidery",
            "reader": PcqReader,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcm",
            "extensions": ("pcm",),
            "mimetype": "application/x-pcm",
            "category": "embroidery",
            "reader": PcmReader,
        }
    )
    yield (
        {
            "description": "Pfaff Embroidery Format",
            "extension": "pcs",
            "extensions": ("pcs",),
            "mimetype": "application/x-pcs",
            "category": "embroidery",
            "reader": PcsReader,
        }
    )
    yield (
        {
            "description": "Janome Embroidery Format",
            "extension": "jpx",
            "extensions": ("jpx",),
            "mimetype": "application/x-jpx",
            "category": "embroidery",
            "reader": JpxReader,
        }
    )
    yield (
        {
            "description": "Gunold Embroidery Format",
            "extension": "stc",
            "extensions": ("stc",),
            "mimetype": "application/x-stc",
            "category": "embroidery",
            "reader": StcReader,
        }
    )
    yield ({
        "description": "Zeng Hsing Embroidery Format",
        "extension": "zhs",
        "extensions": ("zhs",),
        "mimetype": "application/x-zhs",
        "category": "embroidery",
        "reader": ZhsReader
    })
    yield (
        {
            "description": "ZSK TC Embroidery Format",
            "extension": "zxy",
            "extensions": ("z00", "z01", "z02"),
            "mimetype": "application/x-zxy",
            "category": "embroidery",
            "reader": ZxyReader,
        }
    )
    yield (
        {
            "description": "Brother Stitch Format",
            "extension": "pmv",
            "extensions": ("pmv",),
            "mimetype": "application/x-pmv",
            "category": "stitch",
            "reader": PmvReader,
            "writer": PmvWriter,
        }
    )
    yield (
        {
            "description": "PNG Format, Portable Network Graphics",
            "extension": "png",
            "extensions": ("png",),
            "mimetype": "image/png",
            "category": "image",
            "writer": PngWriter,
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
            "writer": TxtWriter,
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
            "reader": GcodeReader,
            "writer": InkstitchGcodeWriter,
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
            "reader": HusReader,
        }
    )
    yield(
        {
            "description": "Iqp - Intelliquilter Format",
            "extension": "iqp",
            "extensions": ("iqp",),
            "mimetype": "application/x-iqp",
            "category": "quilting",
            "reader": IqpReader,
        }
    )
    yield(
        {
            "description": "Plt - HPGL",
            "extension": "plt",
            "extensions": ("plt",),
            "mimetype": "text/plain",
            "category": "quilting",
            "reader": PltReader,
            "writer": PltWriter,
        }
    )
    yield(
        {
            "description": "Qcc - QuiltEZ",
            "extension": "qcc",
            "extensions": ("qcc",),
            "mimetype": "text/plain",
            "category": "quilting",
            "reader": QccReader,
            "writer": QccWriter,
        }
    )
    yield (
        {
            "description": "Edr Color Format",
            "extension": "edr",
            "extensions": ("edr",),
            "mimetype": "application/x-edr",
            "category": "color",
            "reader": EdrReader,
            "writer": EdrWriter,
        }
    )
    yield (
        {
            "description": "Col Color Format",
            "extension": "col",
            "extensions": ("col",),
            "mimetype": "application/x-col",
            "category": "color",
            "reader": ColReader,
            "writer": ColWriter,
        }
    )
    yield (
        {
            "description": "Inf Color Format",
            "extension": "inf",
            "extensions": ("inf",),
            "mimetype": "application/x-inf",
            "category": "color",
            "reader": InfReader,
            "writer": InfWriter,
        }
    )
    yield (
        {
            "description": "Json Export",
            "extension": "json",
            "extensions": ("json",),
            "mimetype": "application/json",
            "category": "debug",
            "reader": JsonReader,
            "writer": JsonWriter,
        }
    )

def read_dst(f, settings=None, pattern=None):
    """Reads fileobject as DST file"""
    return EmbPattern.read_embroidery(DstReader, f, settings, pattern)

def read_pec(f, settings=None, pattern=None):
    """Reads fileobject as PEC file"""
    return EmbPattern.read_embroidery(PecReader, f, settings, pattern)

def read_pes(f, settings=None, pattern=None):
    """Reads fileobject as PES file"""
    return EmbPattern.read_embroidery(PesReader, f, settings, pattern)

def read_exp(f, settings=None, pattern=None):
    """Reads fileobject as EXP file"""
    return EmbPattern.read_embroidery(ExpReader, f, settings, pattern)

def read_vp3(f, settings=None, pattern=None):
    """Reads fileobject as VP3 file"""
    return EmbPattern.read_embroidery(Vp3Reader, f, settings, pattern)

def read_jef(f, settings=None, pattern=None):
    """Reads fileobject as JEF file"""
    return EmbPattern.read_embroidery(JefReader, f, settings, pattern)

def read_u01(f, settings=None, pattern=None):
    """Reads fileobject as U01 file"""
    return EmbPattern.read_embroidery(U01Reader, f, settings, pattern)

def read_csv(f, settings=None, pattern=None):
    """Reads fileobject as CSV file"""
    return EmbPattern.read_embroidery(CsvReader, f, settings, pattern)

def read_json(f, settings=None, pattern=None):
    """Reads fileobject as JSON file"""
    return EmbPattern.read_embroidery(JsonReader, f, settings, pattern)

def read_gcode(f, settings=None, pattern=None):
    """Reads fileobject as GCode file"""
    return EmbPattern.read_embroidery(GcodeReader, f, settings, pattern)

def read_xxx(f, settings=None, pattern=None):
    """Reads fileobject as XXX file"""
    return EmbPattern.read_embroidery(XxxReader, f, settings, pattern)

def read_tbf(f, settings=None, pattern=None):
    """Reads fileobject as TBF file"""
    return EmbPattern.read_embroidery(TbfReader, f, settings, pattern)

def read_iqp(f, settings=None, pattern=None):
    """Reads fileobject as IQP file"""
    pattern = EmbPattern.read_embroidery(IqpReader, f, settings, pattern)
    return pattern

def read_plt(f, settings=None, pattern=None):
    """Reads fileobject as PLT file"""
    pattern = EmbPattern.read_embroidery(PltReader, f, settings, pattern)
    return pattern

def read_qcc(f, settings=None, pattern=None):
    """Reads fileobject as QCC file"""
    pattern = EmbPattern.read_embroidery(QccReader, f, settings, pattern)
    return pattern

def write_dst(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    EmbPattern.write_embroidery(DstWriter, pattern, stream, settings)

def write_pec(pattern, stream, settings=None):
    """Writes fileobject as PEC file"""
    EmbPattern.write_embroidery(PecWriter, pattern, stream, settings)

def write_pes(pattern, stream, settings=None):
    """Writes fileobject as PES file"""
    EmbPattern.write_embroidery(PesWriter, pattern, stream, settings)

def write_exp(pattern, stream, settings=None):
    """Writes fileobject as EXP file"""
    EmbPattern.write_embroidery(ExpWriter, pattern, stream, settings)

def write_vp3(pattern, stream, settings=None):
    """Writes fileobject as Vp3 file"""
    EmbPattern.write_embroidery(Vp3Writer, pattern, stream, settings)

def write_jef(pattern, stream, settings=None):
    """Writes fileobject as JEF file"""
    EmbPattern.write_embroidery(JefWriter, pattern, stream, settings)

def write_u01(pattern, stream, settings=None):
    """Writes fileobject as U01 file"""
    EmbPattern.write_embroidery(U01Writer, pattern, stream, settings)

def write_csv(pattern, stream, settings=None):
    """Writes fileobject as CSV file"""
    EmbPattern.write_embroidery(CsvWriter, pattern, stream, settings)

def write_json(pattern, stream, settings=None):
    """Writes fileobject as JSON file"""
    EmbPattern.write_embroidery(JsonWriter, pattern, stream, settings)

def write_txt(pattern, stream, settings=None):
    """Writes fileobject as CSV file"""
    EmbPattern.write_embroidery(TxtWriter, pattern, stream, settings)

def write_gcode(pattern, stream, settings=None):
    """Writes fileobject as Gcode file"""
    EmbPattern.write_embroidery(GcodeWriter, pattern, stream, settings)

def write_xxx(pattern, stream, settings=None):
    """Writes fileobject as XXX file"""
    EmbPattern.write_embroidery(XxxWriter, pattern, stream, settings)

def write_tbf(pattern, stream, settings=None):
    """Writes fileobject as TBF file"""
    EmbPattern.write_embroidery(TbfWriter, pattern, stream, settings)

def write_plt(pattern, stream, settings=None):
    """Writes fileobject as PLT file"""
    EmbPattern.write_embroidery(PltWriter, pattern, stream, settings)

def write_qcc(pattern, stream, settings=None):
    """Writes fileobject as QCC file"""
    EmbPattern.write_embroidery(QccWriter, pattern, stream, settings)

def write_svg(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    EmbPattern.write_embroidery(SvgWriter, pattern, stream, settings)

def write_png(pattern, stream, settings=None):
    """Writes fileobject as PNG file"""
    EmbPattern.write_embroidery(PngWriter, pattern, stream, settings)
