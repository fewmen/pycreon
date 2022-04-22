use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() -> io::Result<()> {
    let f = File::open("C:\\eBest\\xingAPI\\res\\CDPCQ04700.res")?;
    let reader = BufReader::new(f);

    for line in reader.lines() {
        println!("The bytes: {:?}", line?);
    }


    Ok(())
}