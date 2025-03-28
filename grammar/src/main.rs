use std::{io::Read, process::exit};

use colored::Colorize;
use ebnf::{
    io::MarkableReader,
    parser::{Event, Parser},
    Error, Location, Syntax,
};
use toml::{Table, Value};

use crate::generate::generate;

mod generate;

fn main() {
    // Parse EBNF
    let mut definition_file = String::new();
    let _file = std::fs::File::open("proforma.ebnf")
        .unwrap()
        .read_to_string(&mut definition_file)
        .unwrap();
    let mut tests_file = String::new();
    let _file = std::fs::File::open("test.toml")
        .unwrap()
        .read_to_string(&mut tests_file)
        .unwrap();
    let syntax = ebnf::lex::parse_str("proforma.ebnf", &definition_file).unwrap_or_else(|e| {
        print_error(e, &definition_file, "Lexing error");
        exit(-1);
    });
    let config = ebnf::parser::graph::GraphConfig::new();
    let syntax = Syntax::new(syntax).unwrap_or_else(|e| {
        print_error(e, &definition_file, "Syntax error");
        exit(-2);
    });
    let graph = ebnf::parser::graph::LexGraph::compile(&syntax, &config);

    // Go over all tests
    let mut total_pos = 0;
    let mut total_neg = 0;
    let mut failed = 0;
    let mut generate = Vec::new();
    let tests = tests_file.parse::<Table>().unwrap();
    for (name, set) in tests {
        if let Value::Table(set) = set {
            let mut parser = Parser::new(&graph, &name).unwrap_or_else(|| {
                println!("The name '{name}' is not defined");
                exit(-3)
            });
            if let Some(set) = set.get("positive") {
                let mut positive = 0;
                let mut negative = 0;
                if let Value::Array(tests) = set {
                    total_pos += tests.len();
                    for test in tests {
                        if let Value::String(test) = test {
                            match parser.parse(&mut MarkableReader::new(test, test.as_str().into()))
                            {
                                Ok(_) => positive += 1,
                                Err(e) => {
                                    print_error(e, test, "Positive test failed");
                                    negative += 1;
                                    failed += 1;
                                }
                            }
                        } else {
                            panic!("The toml test file should be a string for '{name}' 'positive'");
                        }
                    }
                } else {
                    panic!("The toml test file should be a array for '{name}' 'positive'");
                }
                if negative > 0 {
                    println!(
                        "{} - {} positive tests, failed {}",
                        name.red(),
                        positive + negative,
                        negative
                    );
                    show_examples(&name, &syntax, 3);
                } else {
                    println!("{} - {} positive tests", name.green(), positive);
                }
            }
            if let Some(set) = set.get("negative") {
                let mut positive = 0;
                let mut negative = 0;
                if let Value::Array(tests) = set {
                    total_neg += tests.len();
                    for test in tests {
                        if let Value::String(test) = test {
                            match parser.parse(&mut MarkableReader::new(test, test.as_str().into()))
                            {
                                Ok(v) => {
                                    println!("   {}: '{test}'", "Negative test failed".red());
                                    print_match(test, &v);
                                    positive += 1;
                                    failed += 1;
                                }
                                Err(_) => {
                                    negative += 1;
                                }
                            }
                        } else {
                            panic!("The toml test file should be a string for '{name}' 'negative'");
                        }
                    }
                } else {
                    panic!("The toml test file should be a array for '{name}' 'negative'");
                }
                if positive > 0 {
                    println!(
                        "{} - {} negative tests, failed {}",
                        name.red(),
                        positive + negative,
                        positive
                    );
                    show_examples(&name, &syntax, 3);
                } else {
                    println!("{} - {} negative tests", name.green(), negative);
                }
            }
            if let Some(num) = set.get("generate") {
                if let Value::Integer(num) = num {
                    generate.push((name.clone(), *num));
                } else {
                    panic!("The toml test file should be an integer for '{name}' 'generate'");
                }
            }
        } else {
            panic!("The toml test file should be a table for '{name}'");
        }
    }
    println!();
    if failed == 0 {
        println!(
            "{} - {} positive and {} negative tests",
            "Passed".green(),
            total_pos,
            total_neg
        );
    } else {
        println!(
            "{} - {} failed tests out of {} positive and {} negative tests",
            "Failed".red(),
            failed,
            total_pos,
            total_neg
        );
    }

    // Go over generations
    for (name, num) in generate {
        show_examples(&name, &syntax, u64::try_from(num).unwrap());
    }
}

fn print_error(error: Error, text: &str, error_type: &str) {
    println!(
        "  {}: {}\n   | {}\n     {}{}\n  {}",
        error_type.red(),
        error.location.name,
        text.lines()
            .nth((error.location.lines - 1) as usize)
            .unwrap(),
        " ".repeat((error.location.columns - 1) as usize),
        "^".red(),
        error.message.blue(),
    )
}

fn show_examples(name: &str, syntax: &Syntax, num: u64) {
    for n in 0..num {
        println!(
            "  {} {n}: {}",
            "Example".blue(),
            generate(syntax.get_syntax_rule(name).unwrap(), syntax, n).yellow(),
        );
    }
    println!();
}

fn print_match(text: &str, events: &[Event]) {
    use std::fmt::Write;
    let mut start_of_line = true;
    for (index, ch) in text.chars().enumerate() {
        let mut first = true;
        let mut already_printed: Vec<&str> = Vec::new();
        let mut buffer = String::new();
        let index = index as u64 + 1;

        for e in events {
            match e {
                Event::Begin {
                    location: Location { columns, .. },
                    label,
                    ..
                } if *columns == index
                    && label.chars().next().is_some_and(|c| c.is_ascii_lowercase())
                    && !already_printed.contains(&label.as_str()) =>
                {
                    write!(
                        &mut buffer,
                        "{}{}",
                        if first { "" } else { ", " },
                        label.green()
                    )
                    .unwrap();
                    first = false;
                    already_printed.push(label.as_str());
                }
                _ => (),
            }
        }
        if !buffer.is_empty() {
            if !start_of_line {
                println!();
            }
            println!("┌ {buffer}");
        }
        print!("{}", ch.to_string().blue());
        start_of_line = false;

        buffer.clear();
        first = true;
        already_printed.clear();
        for e in events {
            match e {
                Event::End {
                    location: Location { columns, .. },
                    label,
                    ..
                } if *columns == index + 1
                    && label.chars().next().is_some_and(|c| c.is_ascii_lowercase())
                    && !already_printed.contains(&label.as_str()) =>
                {
                    write!(
                        &mut buffer,
                        "{}{}",
                        if first { "" } else { ", " },
                        label.red()
                    )
                    .unwrap();
                    first = false;
                    already_printed.push(label.as_str());
                }
                _ => (),
            }
        }
        if !buffer.is_empty() {
            if !start_of_line {
                println!();
            }
            println!("└ {buffer}");
            start_of_line = true;
        }
    }
}
