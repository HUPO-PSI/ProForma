import io
import sys
import datetime
import zlib

import glypy
from glypy.structure.glycan_composition import from_iupac_lite, to_iupac_lite
from glypy.io import glycoct, iupac, wurcs
from glypy.composition import formula
from glypy.io.nomenclature import synonyms

from psims.controlled_vocabulary import (
    obo,
    ControlledVocabulary,
    obj_to_xsdtype,
)

def make_accession(mono):
    src = str(mono) + formula(mono.total_composition())
    byte_src = src.encode('ascii')
    sys.stderr.write(f"{src} {zlib.crc32(byte_src)}\n")
    chk = hex(abs(zlib.crc32(byte_src))).upper()[2:].zfill(8)
    return "MONO:%s" % chk


def to_wurcs(mono):
    t = wurcs.dumps(mono)
    t = t.split("[")[1]
    t = t.split("]")[0]
    return t


parser = obo.OBOParser(io.BytesIO())
parser.term_type = 'term'

seen = set()
for lab, scls in glypy.structure.SuperClass:
    if scls.value and scls.value < 11 and scls not in seen:
        seen.add(scls)

supercls_entities = sorted(seen)
supercls_to_id = {}
for t in supercls_entities:
    if t.name != "x":
        mono = from_iupac_lite(t.name.title())
        mono_tp = {
            "id": make_accession(mono),
            "name": to_iupac_lite(mono),
            "def": "A generic monosaccharide with %d backbone carbons"
            % (mono.superclass.value),
            "synonyms": [
                dialect(mono)
                for dialect in [glycoct.dumps, iupac.dumps, to_wurcs, to_iupac_lite]
            ],
            "property_value": [
                'has_chemical_formula "%s" %s'
                % (
                    formula(mono.total_composition()),
                    obj_to_xsdtype(str(formula(mono.total_composition()))),
                ),
                'has_monoisotopic_mass "%s" %s'
                % (mono.mass(), obj_to_xsdtype(mono.mass())),
            ],
        }
        supercls_to_id[mono.superclass] = mono_tp["id"]
        parser.current_term = mono_tp
        parser.pack()

seen = set()
handled_monos = set()

def to_format(dialect, mono):
    try:
        return dialect(mono)
    except ValueError:
        return None


for label in [
    "dHex",
    "Fuc",
    "HexN",
    "HexNAc",
    "HexS",
    "HexP",
    "HexNAc(S)",
    "NeuAc",
    "NeuGc",
    "Neu",
    "HexNS",
    "aHex",
    "en,aHex",
    "Kdn",
    "Kdo",
]:
    try:
        mono = from_iupac_lite(label)
        mono_tp = {
            "id": make_accession(mono),
            "name": label,
            "def": str(mono),
            "synonyms": list(
                filter(
                    bool,
                    [
                        to_format(dialect, mono)
                        for dialect in [
                            glycoct.dumps,
                            iupac.dumps,
                            to_wurcs,
                            to_iupac_lite,
                        ]
                        if to_format(dialect, mono) != label
                    ],
                )
            )
            + [
                s for s in synonyms.monosaccharides.get(str(mono), []) if s != str(mono)
            ],
            "property_value": [
                f'has_chemical_formula "{formula(mono.total_composition())}" {obj_to_xsdtype(str(formula(mono.total_composition())))}',
                f'has_monoisotopic_mass "{mono.mass():0.10f}" {obj_to_xsdtype(mono.mass())}',
            ],
        }
        parser.current_term = mono_tp
        parser.pack()
    except iupac.IUPACError as err:
        print(err, file=sys.stderr)

for label, synonyms_ in [("sulfate", ["S", "Sulfo"]), ("phosphate", ["P", "Phospho"])]:
    try:
        subst = from_iupac_lite(label)
        mono_tp = {
            "id": make_accession(subst),
            "name": str(subst).replace("@", ""),
            "def": str(subst).replace("@", ""),
            "synonyms": synonyms_,
            "property_value": [
                f'has_chemical_formula "{formula(mono.total_composition())}" {obj_to_xsdtype(str(formula(mono.total_composition())))}',
                f'has_monoisotopic_mass "{mono.mass():0.10f}" {obj_to_xsdtype(mono.mass())}',
            ],
        }
        parser.current_term = mono_tp
        parser.pack()
    except iupac.IUPACError as err:
        print(err, file=sys.stderr)


parser._connect_parents()
parser._simplify_header_information()

cv = ControlledVocabulary(parser.terms)

def write_header(self, header, stream):
    for key, value in header:
        stream.write(("%s: %s\n" % (key, value)).encode('utf8'))
    stream.write(b"\n")
    stream.write(b"\n")


def write_term(self, term, stream):
    stream.write(
        ('[Term]\nid: %s\nname: %s\ndef: "%s"\n' % (term.id, term.name, term.definition)).encode('utf8')
    )
    #     for xref in term.get('xref', []):
    #         stream.write("xref: ")
    seen = set()
    for syn in term.get("synonyms", []):
        if syn in seen:
            continue
        seen.add(syn)
        stream.write(('synonym: "%s" EXACT\n' % str(syn).replace("\n", "\\n")).encode('utf8'))
    for prop in term.get("property_value", []):
        stream.write(("property_value: %s\n" % prop).encode('utf8'))
    stream.write(b"\n")


buff = io.BytesIO()

header = [
    ("format-version", "1.2"),
    ("date", str(datetime.datetime.now())),
    ("remark", "namespace: MONO"),
    ("remark", "creator: Joshua Klein <jaklein <-at-> bu.edu>"),
    ("ontology", "MONO"),
]


write_header(None, header, buff)

for key, term in sorted(
    cv.items(),
    key=lambda x: ("generic" not in x[1].definition, x[1].has_monoisotopic_mass),
):
    write_term(None, term, buff)

sys.stdout.buffer.write(buff.getvalue())
