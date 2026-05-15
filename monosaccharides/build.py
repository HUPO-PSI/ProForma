from datetime import datetime
from typing import TypedDict

import fastobo
import glypy
from fastobo.id import PrefixedIdent, UnprefixedIdent
from fastobo.pv import LiteralPropertyValue
from fastobo.syn import Synonym
from fastobo.term import (
    DefClause,
    IsAClause,
    NameClause,
    PropertyValueClause,
    SynonymClause,
    TermFrame,
)
from glypy.composition import formula
from glypy.io import glycoct, iupac, wurcs
from glypy.io.nomenclature import synonyms
from glypy.structure.glycan_composition import from_iupac_lite, to_iupac_lite


def make_accession(mono: glypy.MonosaccharideResidue, label: str, counter: int):
    chk = str(counter).zfill(8)
    return PrefixedIdent("MONO", chk)


def to_wurcs(mono):
    t = wurcs.dumps(mono)
    t = t.split("[")[1]
    t = t.split("]")[0]
    return t


def to_format(dialect, mono):
    try:
        return dialect(mono)
    except ValueError:
        return None


def make_generic_defn(scls: glypy.structure.SuperClass) -> str:
    return "A generic monosaccharide with %d backbone carbons" % scls.value


fancy_defns = {line.split("\t")[0]: line.split("\t")[1] for line in """Hex	Hexose
HexNAc	N-Acetyl Hexose
HexS	Hexose Sulfate
HexP	Hexose Phosphate
HexNAcS	N-Acetyl Hexose Sulfate
HexN	Hexosamine
HexNS	N-Sulfo Hexosamine
dHex	Deoxy-Hexose
aHex	Hexuronic Acid
en,aHex	Anhydro-Hexuronic Acid
Neu	Neuraminic acid
NeuAc	N-acetyl Neuraminic Acid / Sialic Acid
NeuGc	N-glycolyl Neuraminic Acid
Sug	Sugose
Tri	Triose
Tet	Tetrose
Pen	Pentose
Hep	Heptose
Oct	Octose
Non	Nonose
Dec	Decose
Fuc	Fucose, a stereochemical assignment of dHex abundant in mammals
Kdo	Ketodeoxyoctonic acid
Kdn	Ketodeoxynonulosonic acid
Sulfo	Sulfuric acid
Phospho	Phosphoric acid""".splitlines()}

class RecordType(TypedDict):
    name: str
    synonyms: list[str] | None
    defn: str | None
    tp: str | None
    parent: str | None
    source_name: str | None

    @classmethod
    def from_name(cls, name: str):
        if isinstance(name, dict):
            if 'source_name' not in name:
                name['source_name'] = name['name']
            if "synonyms" not in name:
                name['synonyms'] = []
            return name | {"tp": "monosaccharide"}
        return {"name": name, "synonyms": [], "tp": "monosaccharide", "defn": None, "source_name": name}

    @classmethod
    def from_superclass(cls, supercls: glypy.structure.SuperClass):
        return RecordType(
            {
                "name": supercls.name.title(),
                "synonyms": [],
                "tp": "superclass",
                "defn": make_generic_defn(supercls),
                "source_name": None,
            }
        )

    @classmethod
    def from_substituent(cls, subst_name: str, synonyms: list[str], source_name: str | None = None):
        return RecordType(
            {
                "name": subst_name,
                "source_name": source_name or subst_name,
                "synonyms": synonyms,
                "defn": None,
                "tp": "substituent",
            }
        )

def make_supercls_entry(record: RecordType, counter: int):
    name = record["name"]
    mono = from_iupac_lite(name)
    defn = record["defn"]
    synonyms_of = list(
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
                if to_format(dialect, mono) != name
            ],
        )
    )

    synonyms_of = [SynonymClause(Synonym(syn, "EXACT")) for syn in synonyms_of]

    is_a = []
    parent = record.get("parent")
    if parent:
        is_a.append(IsAClause(parent))

    clauses = [
        make_accession(mono, name, counter),
        NameClause(name),
        DefClause(defn if defn else str(mono)),
        *is_a,
        *synonyms_of,
        PropertyValueClause(
            LiteralPropertyValue(
                UnprefixedIdent("has_chemical_formula"),
                f"{formula(mono.total_composition())}",
                PrefixedIdent("xsd", "string"),
            )
        ),
        PropertyValueClause(
            LiteralPropertyValue(
                UnprefixedIdent("has_monoisotopic_mass"),
                f"{mono.mass():0.4f}",
                PrefixedIdent("xsd", "float"),
            )
        ),
    ]
    return TermFrame(clauses[0], clauses[1:])


def make_monosaccharide_entry(record: RecordType, counter: int):
    name = record["name"]
    mono = from_iupac_lite(record["source_name"])

    synonyms_of = (
        list(
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
                    if to_format(dialect, mono) != name
                ],
            )
        )
        + [s for s in synonyms.monosaccharides.get(str(mono), []) if s != str(mono) and s != name]
        + record.get("synonyms", [])
    )

    synonyms_of = [SynonymClause(Synonym(syn, "EXACT")) for syn in synonyms_of]

    is_a = []
    parent = record.get("parent")
    if parent:
        is_a.append(IsAClause(parent))

    defn = record.get('defn')
    if not defn:
        if name in fancy_defns:
            defn = fancy_defns[name]
        else:
            defn = str(mono)

    clauses = [
        make_accession(mono, name, counter),
        NameClause(name),
        DefClause(defn),
        *is_a,
        *synonyms_of,
        PropertyValueClause(
            LiteralPropertyValue(
                UnprefixedIdent("has_chemical_formula"),
                f"{formula(mono.total_composition())}",
                PrefixedIdent("xsd", "string"),
            )
        ),
        PropertyValueClause(
            LiteralPropertyValue(
                UnprefixedIdent("has_monoisotopic_mass"),
                f"{mono.mass():0.4f}",
                PrefixedIdent("xsd", "float"),
            )
        ),
    ]
    return TermFrame(clauses[0], clauses[1:])


def make_substituent_entry(record: RecordType, counter: int):
    name = record["name"]
    subst = from_iupac_lite(record['source_name'])

    synonyms_of = [
        SynonymClause(Synonym(syn, "EXACT")) for syn in record.get("synonyms", [])
    ]

    if record['source_name'] != name:
        synonyms_of.append(SynonymClause(Synonym(record['source_name'], 'EXACT')))

    defn = record.get("defn")
    if not defn:
        if name in fancy_defns:
            defn = fancy_defns[name]
        else:
            defn = str(subst)[1:]

    clauses = [
        make_accession(subst, name, counter),
        NameClause(name),
        DefClause(defn),
        *synonyms_of,
        PropertyValueClause(
            LiteralPropertyValue(
                UnprefixedIdent("has_chemical_formula"),
                f"{formula(subst.total_composition())}",
                PrefixedIdent("xsd", "string"),
            )
        ),
        PropertyValueClause(
            LiteralPropertyValue(
                UnprefixedIdent("has_monoisotopic_mass"),
                f"{subst.mass():0.4f}",
                PrefixedIdent("xsd", "float"),
            )
        ),
    ]
    return TermFrame(clauses[0], clauses[1:])


def render(self: RecordType, counter: int):
    if self["tp"] == "superclass":
        return make_supercls_entry(self, counter)
    elif self["tp"] == "monosaccharide":
        return make_monosaccharide_entry(self, counter)
    elif self["tp"] == "substituent":
        return make_substituent_entry(self, counter)
    else:
        raise NotImplementedError()



## CREATE INITIAL FROZEN ENTRIES, DO NOT MODIFY

seen = set()
for lab, scls in glypy.structure.SuperClass:
    if scls.value and scls.value < 11 and scls not in seen:
        seen.add(scls)

supercls_entities = sorted(seen)
supercls_recs = list(map(RecordType.from_superclass, supercls_entities))

monosaccharide_recs = list(
    map(
        RecordType.from_name,
        [
            "dHex",
            "Fuc",
            "HexN",
            "HexNAc",
            "HexS",
            "HexP",
            {"name": "HexNAcS", "source_name": "HexNAc(S)"},
            "NeuAc",
            "NeuGc",
            "Neu",
            "HexNS",
            {"name": "aHex", "synonyms": ["HexA"]},
            {"name": "en,aHex", "synonyms": ["dHexA"]},
            "Kdn",
            "Kdo",
        ],
    )
)


substituent_recs = list(
    map(
        lambda x: RecordType.from_substituent(*x),
        [
            (
                "Sulfo",
                [
                    "S",
                ],
                "sulfate",
            ),
            ("Phospho", ["P", ], "phosphate"),
        ],
    )
)

records = supercls_recs + monosaccharide_recs + substituent_recs

## ADD NEW RECORDS HERE

terms = []
for i, record in enumerate(records):
    term = render(record, i)
    terms.append(term)



header_recs = fastobo.header.HeaderFrame(
    [
        fastobo.header.FormatVersionClause("1.2"),
        fastobo.header.DefaultNamespaceClause("MONO"),
        fastobo.header.RemarkClause("creator: Joshua Klein <jaklein <-at-> bu.edu>"),
        fastobo.header.DateClause(datetime.now()),
        fastobo.header.OntologyClause("MONO"),
    ]
)

doc = fastobo.doc.OboDoc(header_recs, terms)
print(doc)