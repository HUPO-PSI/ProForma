use ebnf::{
    lex::{DefinitionList, SingleDefinition, SyntacticPrimary, SyntacticTerm, SyntaxRule},
    Syntax,
};
use rand::{rngs::StdRng, Rng, SeedableRng};
use std::fmt::Write;

pub fn generate(rule: &SyntaxRule, syntax: &Syntax, seed: u64) -> String {
    let mut buffer = String::new();
    let mut rng = StdRng::seed_from_u64(seed);

    rule.definition_list.generate(&mut buffer, &mut rng, syntax);
    buffer
}

trait Generate {
    fn generate(&self, buffer: &mut String, rng: &mut StdRng, syntax: &Syntax);
}

impl Generate for DefinitionList {
    fn generate(&self, buffer: &mut String, rng: &mut StdRng, syntax: &Syntax) {
        self.0[rng.gen_range(0..self.0.len())].generate(buffer, rng, syntax);
    }
}

impl Generate for SingleDefinition {
    fn generate(&self, buffer: &mut String, rng: &mut StdRng, syntax: &Syntax) {
        for element in &self.syntactic_terms {
            element.generate(buffer, rng, syntax);
        }
    }
}

impl Generate for SyntacticTerm {
    fn generate(&self, buffer: &mut String, rng: &mut StdRng, syntax: &Syntax) {
        for _ in 0..self.syntactic_factor.repetition {
            match &self.syntactic_factor.syntactic_primary {
                SyntacticPrimary::EmptySequence(_) => (),
                SyntacticPrimary::MetaIdentifier(_, name) => syntax
                    .get_syntax_rule(name)
                    .unwrap()
                    .definition_list
                    .generate(buffer, rng, syntax),
                SyntacticPrimary::TerminalString(_, text) => write!(buffer, "{}", text).unwrap(),
                SyntacticPrimary::SpecialSequence(_, text) => write!(buffer, "{}", text).unwrap(),
                SyntacticPrimary::OptionalSequence(_, def) => {
                    if rng.gen() {
                        def.generate(buffer, rng, syntax)
                    }
                }
                SyntacticPrimary::GroupedSequence(_, def) => {
                    def.0[rng.gen_range(0..def.0.len())].generate(buffer, rng, syntax);
                }
                SyntacticPrimary::RepeatedSequence(_, def) => {
                    for _ in 0..rng.gen_range(0..3) {
                        def.generate(buffer, rng, syntax)
                    }
                }
            }
        }
    }
}
