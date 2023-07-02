use std::error::Error;
use std::io::{self, Write};

fn main() -> Result<(), Box<dyn Error>> {
    loop {
        let input = match read()? {
            Some(s) => s,
            None => break,
        };
        let ret = eval(&input);
        print(&ret);
    }
    Ok(())
}

fn read() -> Result<Option<String>, io::Error> {
    print!("user> ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    if io::stdin().read_line(&mut input)? == 0 {
        Ok(None)
    } else {
        Ok(Some(input))
    }
}

fn eval(s: &str) -> String {
    s.to_string()
}

fn print(s: &str) {
    println!("{}", s);
}
