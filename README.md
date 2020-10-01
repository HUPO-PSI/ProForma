# ProForma (Proteoform and Peptidoform Notation)

Protein and peptide sequences are usually represented using a string of amino acids using a well-known one letter code endorsed by the IUPAC. However, there is still no clear consensus about how to represent ‘proteoforms’ and ‘peptidoforms’, meaning all possible variations of a protein/peptide sequence, including protein modifications, both artefactual and post-translational modifications (PTMs). There are indeed multiple ways of encoding mass modifications and extended discussion has taken place to achieve a consensus. A standard notation for proteoforms and peptidoforms is then required for the community, so that it can be embedded in many relevant PSI (and potentially other) file formats.

The PSI has developed a format called [PEFF (PSI Extended FASTA Format)](http://www.psidev.info/peff) that can be used to represent proteoforms. Additionally, the Consortium for Top Down Proteomics [CTDP](http://topdownproteomics.org) developed a notation format called [ProForma v1](https://topdownproteomics.github.io/ProteoformNomenclatureStandard/), aiming to represent proteoforms.    

This format specification represents the consensus for the standard representation of proteoforms and peptidoforms.  This notation aims to support the main proteomics approaches, including bottom-up (focused on peptides/peptidoforms) and top-down (focused on proteins/proteoforms) approaches.

## Use cases supported (with examples)
The ProForma notation is a string of characters that represent linearly one or more peptidoform/proteoform primary structures with possibilities to link peptidic chains together. It is not meant to represent secondary or tertiary structures. 

##### Canonical [IUPAC amino acids](http://publications.iupac.org/pac/1984/pdf/5605x0595.pdf)
* `EMEVEESPEK`
##### PTMs using common ontologies or controlled vocabularies (e.g. [Unimod](http://www.unimod.org/), [PSI-MOD](https://www.ebi.ac.uk/ols/ontologies/mod), and [RESID](https://proteininformationresource.org/resid/))
* `EM[UNIMOD:35]EVEES[UNIMOD:21]PEK`
* `EM[L-methionine sulfoxide]EVEES[O-phospho-L-serine]PEK`
##### Cross-linkers using the [XL-MOD](https://raw.githubusercontent.com/HUPO-PSI/mzIdentML/master/cv/XLMOD.obo) ontology
* `EMEVTK[XLMOD:02001#XL1]SESPEK[#XL1]`
* `EVTSEKC[L-cystine (cross-link)#XL1]LEMSC[#XL1]EFD`
##### Glycans using the [GNO (Glycan Naming Ontology)](https://www.ebi.ac.uk/ols/ontologies/gno) ontology
* `YPVLN[GNO:G62765YT]VTMPN[GNO:G02815KT]NSNGKFDK`
##### Arbitrary mass shifts and unknown mass gaps
* `EM[+15.9949]EVEES[-79.9663]PEK`
* `RTAAX[+367.0537]WT`
##### Elemental formulas and [Glycan compositions](./monosaccharides/mono.obo)
* `SEQUEN[Formula:C12H20O2]CE`
* `SEQUEN[Glycan:HexNAc1Hex 2]CE`
##### Terminal and Labile Modifications
* `[iTRAQ4plex]-EMEVNESPEK-[Methyl]`
* `{Glycan:Hex}EMEVNESPEK`
##### Ambiguity of modification position (completely unlocalised, _n_ possible sites, or a range of sites)
* `[Phospho]?EMEVTSESPEK`
* `EMEVT[#g1]S[#g1]ES[Phospho#g1]PEK`
* `PROT(EOSFORMS)[+19.0523]ISK`
##### Global modifications (e.g. isotopic labeling or fixed protein modifications)
* `<13C>ATPEILTVNSIGQLK`
* `<[S-carboxamidomethyl-L-cysteine]@C>ATPEILTCNSIGCLK`
##### Additional user-supplied textual information
* `ELV[info:AnyString]IS`