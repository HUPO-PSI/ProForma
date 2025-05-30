# HUPO-PSI ProForma specification

*Describe compound peptidoform ion attributes*

## Properties

- <a id="properties/fixed_modifications"></a>**`fixed_modifications`** *(array)*
  - <a id="properties/fixed_modifications/items"></a>**Items** *(object)*: A fixed modification. Cannot contain additional properties.
    - <a id="properties/fixed_modifications/items/properties/modification"></a>**`modification`**: Fixed modifications cannot be cross-linked or ambiguous. Refer to *[#/$defs/tags](#%24defs/tags)*.
    - <a id="properties/fixed_modifications/items/properties/position_rules"></a>**`position_rules`** *(array)*
      - <a id="properties/fixed_modifications/items/properties/position_rules/items"></a>**Items**: Refer to *[#/$defs/position_rule](#%24defs/position_rule)*.
- <a id="properties/isotope_replacement"></a>**`isotope_replacement`** *(array)*
  - <a id="properties/isotope_replacement/items"></a>**Items** *(object)*: A global isotope replacement, 'D' is also allowed to be written as a shortcut, but this is encoded as 2H. Cannot contain additional properties.
    - <a id="properties/isotope_replacement/items/properties/element"></a>**`element`**: Refer to *[#/$defs/element](#%24defs/element)*.
    - <a id="properties/isotope_replacement/items/properties/isotope"></a>**`isotope`**: Nucleon count. Refer to *[#/$defs/positive_integer](#%24defs/positive_integer)*.
- <a id="properties/name"></a>**`name`** *(string)*: The compound peptidoform ion name, expressed with (>>>name) in ProForma 2.1.
- <a id="properties/peptidoform_ions"></a>**`peptidoform_ions`** *(array, required)*
  - <a id="properties/peptidoform_ions/items"></a>**Items** *(object)*: A peptidoform ion. Cannot contain additional properties.
    - <a id="properties/peptidoform_ions/items/properties/charge"></a>**`charge`**: Refer to *[#/$defs/global_charge](#%24defs/global_charge)*.
    - <a id="properties/peptidoform_ions/items/properties/name"></a>**`name`** *(string)*: The peptidoform ion name, expressed with (>>name) in ProForma 2.1.
    - <a id="properties/peptidoform_ions/items/properties/peptidoforms"></a>**`peptidoforms`** *(array, required)*
      - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items"></a>**Items** *(object)*: A Peptidoform. Cannot contain additional properties.
        - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/c_term_modifications"></a>**`c_term_modifications`** *(array)*
          - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/c_term_modifications/items"></a>**Items**: Refer to *[#/$defs/modification](#%24defs/modification)*.
        - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/labile_modifications"></a>**`labile_modifications`** *(array)*: Labile modifications cannot be cross-linked or ambiguous.
          - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/labile_modifications/items"></a>**Items**: Refer to *[#/$defs/tags](#%24defs/tags)*.
        - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/n_term_modifications"></a>**`n_term_modifications`** *(array)*
          - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/n_term_modifications/items"></a>**Items**: Refer to *[#/$defs/modification](#%24defs/modification)*.
        - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/name"></a>**`name`** *(string)*: The peptidoform name, expressed with (>name) in ProForma 2.1.
        - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/sequence"></a>**`sequence`** *(array, required)*
          - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/sequence/items"></a>**Items**: Refer to *[#/$defs/sequence](#%24defs/sequence)*.
        - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/unlocalised_modifications"></a>**`unlocalised_modifications`** *(array)*
          - <a id="properties/peptidoform_ions/items/properties/peptidoforms/items/properties/unlocalised_modifications/items"></a>**Items**: Refer to *[#/$defs/modification_ambiguous](#%24defs/modification_ambiguous)*.
## Definitions

- <a id="%24defs/amino_acid"></a>**`amino_acid`**: An amino acid including unconventional ones (U/O) and ambiguous ones (X/J/B/Z). Must be one of: `["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]`.
- <a id="%24defs/charged_formula"></a>**`charged_formula`** *(object)*: A formula that can be charged, expressed in ProForma as Formula:C2H6:z+2. Can contain additional properties.
  - <a id="%24defs/charged_formula/properties/charge"></a>**`charge`** *(integer)*: The charge state for this formula.
  - <a id="%24defs/charged_formula/properties/formula"></a>**`formula`**: Refer to *[#/$defs/formula](#%24defs/formula)*.
- <a id="%24defs/CV"></a>**`CV`**: One of the five supported controlled vocabularies. Must be one of: `["Unimod", "PSI-MOD", "RESID", "GNOme", "XL-MOD"]`.
- <a id="%24defs/element"></a>**`element`**: All elements. Must be one of: `["He", "Li", "Be", "Ne", "Na", "Mg", "Al", "Si", "Cl", "Ar", "Ca", "Sc", "Ti", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og", "U", "W", "I", "Y", "V", "K", "S", "B", "C", "N", "O", "F", "H", "P"]`.
- <a id="%24defs/formula"></a>**`formula`** *(array)*: A molecular formula.
  - <a id="%24defs/formula/items"></a>**Items** *(object)*: Cannot contain additional properties.
    - <a id="%24defs/formula/items/properties/element"></a>**`element`**: Refer to *[#/$defs/element](#%24defs/element)*.
    - <a id="%24defs/formula/items/properties/isotope"></a>**`isotope`**: Nucleon count. Refer to *[#/$defs/positive_integer](#%24defs/positive_integer)*.
    - <a id="%24defs/formula/items/properties/occurance"></a>**`occurance`** *(integer, required)*: The number of times this part occurs.
- <a id="%24defs/global_charge"></a>**`global_charge`**
  - **Any of**
    - <a id="%24defs/global_charge/anyOf/0"></a>*integer*
    - <a id="%24defs/global_charge/anyOf/1"></a>: Refer to *[#/$defs/global_charge_carriers](#%24defs/global_charge_carriers)*.
- <a id="%24defs/global_charge_carriers"></a>**`global_charge_carriers`** *(array)*
  - <a id="%24defs/global_charge_carriers/items"></a>**Items** *(object)*: Cannot contain additional properties.
    - <a id="%24defs/global_charge_carriers/items/properties/charged_formula"></a>**`charged_formula`**: Refer to *[#/$defs/charged_formula](#%24defs/charged_formula)*.
    - <a id="%24defs/global_charge_carriers/items/properties/occurance"></a>**`occurance`** *(number, required)*
- <a id="%24defs/modification"></a>**`modification`**: A modification, could be ambiguous, cross-linked, or just a single modification (which might be defined multiple times).
  - **Any of**
    - <a id="%24defs/modification/anyOf/0"></a>: Refer to *[#/$defs/modification_ambiguous](#%24defs/modification_ambiguous)*.
    - <a id="%24defs/modification/anyOf/1"></a>: Refer to *[#/$defs/modification_cross_linker](#%24defs/modification_cross_linker)*.
    - <a id="%24defs/modification/anyOf/2"></a>: Refer to *[#/$defs/tags](#%24defs/tags)*.
- <a id="%24defs/modification_ambiguous"></a>**`modification_ambiguous`**
  - **Any of**
    - <a id="%24defs/modification_ambiguous/anyOf/0"></a>: Refer to *[#/$defs/modification_ambiguous_primary](#%24defs/modification_ambiguous_primary)*.
    - <a id="%24defs/modification_ambiguous/anyOf/1"></a>: Refer to *[#/$defs/modification_ambiguous_secondary](#%24defs/modification_ambiguous_secondary)*.
- <a id="%24defs/modification_ambiguous_primary"></a>**`modification_ambiguous_primary`** *(object)*: The primary definition of an ambiguous modification. Cannot contain additional properties.
  - <a id="%24defs/modification_ambiguous_primary/properties/comkp"></a>**`comkp`** *(bool)*: ColocaliseModificationsOfKnownPosition: this controls if this modification of unknown position can be placed on a location where a placed modification is located. By default this is not allowed.
  - <a id="%24defs/modification_ambiguous_primary/properties/comup"></a>**`comup`** *(bool)*: ColocaliseModificationsOfUnknownPosition: this control if this modification of unknown position can coexist at the same location as any other modifications of unknown position. By default this is not allowed.
  - <a id="%24defs/modification_ambiguous_primary/properties/label"></a>**`label`** *(string, required)*: The part after the #. Length must be at least 1.
  - <a id="%24defs/modification_ambiguous_primary/properties/limit"></a>**`limit`**: The maximal number of this modification of unknown position on one position. If this value is not specified a default value of 1 is used. This setting can only be applied on modifications of unknown position with a specified occurrence. Refer to *[#/$defs/positive_integer](#%24defs/positive_integer)*.
  - <a id="%24defs/modification_ambiguous_primary/properties/position"></a>**`position`** *(array)*: A list of positions where this modification is allowed. The positions are written the same as global modifications.
    - <a id="%24defs/modification_ambiguous_primary/properties/position/items"></a>**Items**: Refer to *[#/$defs/position_rule](#%24defs/position_rule)*.
  - <a id="%24defs/modification_ambiguous_primary/properties/score"></a>**`score`** *(number)*: The score for this location of this ambiguous modification. Minimum: `0`. Maximum: `1`.
  - <a id="%24defs/modification_ambiguous_primary/properties/tags"></a>**`tags`**: Refer to *[#/$defs/tags](#%24defs/tags)*.
- <a id="%24defs/modification_ambiguous_secondary"></a>**`modification_ambiguous_secondary`** *(object)*: A reference to an ambiguous modification. Cannot contain additional properties.
  - <a id="%24defs/modification_ambiguous_secondary/properties/label"></a>**`label`** *(string, required)*: The part after the #. Length must be at least 1.
  - <a id="%24defs/modification_ambiguous_secondary/properties/score"></a>**`score`** *(number)*: The score for this location of this ambiguous modification. Minimum: `0`. Maximum: `1`.
- <a id="%24defs/modification_cross_linker"></a>**`modification_cross_linker`** *(object)*: A cross-linked modification, if the tags are missing this is a reuse of a modification that should be defined in another place, if the label is missing this indicates that this is a #BRANCH, and not a #XL<name>. Cannot contain additional properties.
  - <a id="%24defs/modification_cross_linker/properties/label"></a>**`label`** *(string)*: The part after the #XL, or if this is a #BRANCH this entire property is missing. Length must be at least 1.
  - <a id="%24defs/modification_cross_linker/properties/tags"></a>**`tags`**: Refer to *[#/$defs/tags](#%24defs/tags)*.
- <a id="%24defs/monosaccharide"></a>**`monosaccharide`**: A monosaccharide. Must be one of: `["Sulfate", "Phosphate", "Fuc", "NeuAc", "NeuGc", "Neu5Ac", "Neu5Gc", "Neu", "D-Hex", "en,A-Hex", "A-Hex", "HexNAc", "S", "HexNAc", "HexNS", "HexS", "HexP", "HexN", "Hex", "Sug", "Tri", "Tet", "Pen", "Hep", "Oct", "Non", "Dec"]`.
- <a id="%24defs/position_rule"></a>**`position_rule`** *(object)*: Cannot contain additional properties.
  - <a id="%24defs/position_rule/properties/amino_acid"></a>**`amino_acid`**: Refer to *[#/$defs/amino_acid](#%24defs/amino_acid)*.
  - <a id="%24defs/position_rule/properties/terminal"></a>**`terminal`**: Must be one of: `["Anywhere", "NTerm", "CTerm"]`.
- <a id="%24defs/positive_integer"></a>**`positive_integer`** *(integer)*
- <a id="%24defs/sequence"></a>**`sequence`**: A region in a peptide sequence.
  - **Any of**
    - <a id="%24defs/sequence/anyOf/0"></a>: Refer to *[#/$defs/sequence_ambiguous](#%24defs/sequence_ambiguous)*.
    - <a id="%24defs/sequence/anyOf/1"></a>: Refer to *[#/$defs/sequence_element](#%24defs/sequence_element)*.
    - <a id="%24defs/sequence/anyOf/2"></a>: Refer to *[#/$defs/sequence_region](#%24defs/sequence_region)*.
- <a id="%24defs/sequence_ambiguous"></a>**`sequence_ambiguous`** *(array)*
  - <a id="%24defs/sequence_ambiguous/items"></a>**Items**: Refer to *[#/$defs/sequence_element](#%24defs/sequence_element)*.
- <a id="%24defs/sequence_element"></a>**`sequence_element`** *(object)*: Cannot contain additional properties.
  - <a id="%24defs/sequence_element/properties/amino_acid"></a>**`amino_acid`**: Refer to *[#/$defs/amino_acid](#%24defs/amino_acid)*.
  - <a id="%24defs/sequence_element/properties/modifications"></a>**`modifications`** *(array)*
    - <a id="%24defs/sequence_element/properties/modifications/items"></a>**Items**: Refer to *[#/$defs/modification](#%24defs/modification)*.
- <a id="%24defs/sequence_region"></a>**`sequence_region`** *(object)*: Cannot contain additional properties.
  - <a id="%24defs/sequence_region/properties/modifications"></a>**`modifications`** *(array, required)*
    - <a id="%24defs/sequence_region/properties/modifications/items"></a>**Items**: Refer to *[#/$defs/modification](#%24defs/modification)*.
  - <a id="%24defs/sequence_region/properties/sequence"></a>**`sequence`** *(array, required)*
    - <a id="%24defs/sequence_region/properties/sequence/items"></a>**Items**: Refer to *[#/$defs/sequence_element](#%24defs/sequence_element)*.
- <a id="%24defs/tag_accession"></a>**`tag_accession`** *(object)*: The accession for a modification. Cannot contain additional properties.
  - <a id="%24defs/tag_accession/properties/accession"></a>**`accession`** *(string, required)*: The accession number, or for GNOme and RESID the string. Length must be at least 1.
  - <a id="%24defs/tag_accession/properties/cv"></a>**`cv`**: Refer to *[#/$defs/CV](#%24defs/CV)*.
- <a id="%24defs/tag_formula"></a>**`tag_formula`**: A Formula:xxx modification. Refer to *[#/$defs/charged_formula](#%24defs/charged_formula)*.
- <a id="%24defs/tag_glycan"></a>**`tag_glycan`** *(array)*: A glycan composition modification.
  - <a id="%24defs/tag_glycan/items"></a>**Items** *(object)*: Cannot contain additional properties.
    - <a id="%24defs/tag_glycan/items/properties/monosaccharide"></a>**`monosaccharide`**: Refer to *[#/$defs/monosaccharide](#%24defs/monosaccharide)*.
    - <a id="%24defs/tag_glycan/items/properties/occurance"></a>**`occurance`** *(integer, required)*: The number of times this part occurs.
- <a id="%24defs/tag_info"></a>**`tag_info`** *(string)*: A INFO tag modification.
- <a id="%24defs/tag_mass"></a>**`tag_mass`** *(object)*: A mass modification. Cannot contain additional properties.
  - <a id="%24defs/tag_mass/properties/cv"></a>**`cv`**: Refer to *[#/$defs/CV](#%24defs/CV)*.
  - <a id="%24defs/tag_mass/properties/mass"></a>**`mass`** *(number, required)*
- <a id="%24defs/tag_name"></a>**`tag_name`** *(object)*: A named modification. Cannot contain additional properties.
  - <a id="%24defs/tag_name/properties/cv"></a>**`cv`**: Refer to *[#/$defs/CV](#%24defs/CV)*.
  - <a id="%24defs/tag_name/properties/name"></a>**`name`** *(string, required)*: Length must be at least 1.
- <a id="%24defs/tags"></a>**`tags`** *(array)*: A single modification which could consist of multiple definitions.
  - <a id="%24defs/tags/items"></a>**Items**
    - **Any of**
      - <a id="%24defs/tags/items/anyOf/0"></a>: Refer to *[#/$defs/tag_accession](#%24defs/tag_accession)*.
      - <a id="%24defs/tags/items/anyOf/1"></a>: Refer to *[#/$defs/tag_formula](#%24defs/tag_formula)*.
      - <a id="%24defs/tags/items/anyOf/2"></a>: Refer to *[#/$defs/tag_glycan](#%24defs/tag_glycan)*.
      - <a id="%24defs/tags/items/anyOf/3"></a>: Refer to *[#/$defs/tag_info](#%24defs/tag_info)*.
      - <a id="%24defs/tags/items/anyOf/4"></a>: Refer to *[#/$defs/tag_mass](#%24defs/tag_mass)*.
      - <a id="%24defs/tags/items/anyOf/5"></a>: Refer to *[#/$defs/tag_name](#%24defs/tag_name)*.
