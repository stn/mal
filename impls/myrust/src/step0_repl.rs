use std::io::{self, Write};

fn main() {
    loop {
        match read() {
            Some(input) => {
                let ret = eval(&input);
                print(&ret);
            },
            None => break,
        }
    }
}

fn read() -> Option<String> {
    print!("user> ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    match io::stdin().read_line(&mut input) {
        Ok(n_bytes) => {
            if n_bytes == 0 {
                None
            } else {
                Some(input)
            }
        },
        Err(e) => {
            eprintln!("error: {}", e);
            None
        },
    }
}

fn eval(s: &str) -> String {
    s.to_string()
}

fn print(s: &str) {
    println!("{}", s);
}
