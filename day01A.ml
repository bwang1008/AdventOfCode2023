(** Run with "$ ocaml day01A.ml" **)

(** function to read input from file copied from https://stackoverflow.com/questions/5774934/how-do-i-read-in-lines-from-a-text-file-in-ocaml *)
let read_file (filename: string): string list =
    let ic: in_channel = open_in filename in
    let try_read_line (): string option =
        try Some (input_line ic) with End_of_file -> None
    in
    let rec read_all_lines (acc: string list): string list =
        match try_read_line () with
        | Some s -> read_all_lines (s::acc)
        | None -> close_in ic; List.rev acc
    in
    read_all_lines []
in
let main () : int =
    let input: string list = read_file "inputs/day01.txt" in
    let process_line (line: string): int =
        let rec process_line_helper (line: string) (first_digit: int) (last_digit: int) (found_first_digit: bool): int =
            match String.length line with
            | 0 -> 10 * first_digit + last_digit
            | _ -> (
                let first_char: char = String.get line 0 in
                let remaining_line: string = String.sub line 1 ((String.length line) - 1) in
                match (Char.compare '0' first_char) <= 0 && (Char.compare first_char '9') <= 0 with
                | false -> process_line_helper remaining_line first_digit last_digit found_first_digit
                | true -> (
                    let digit: int = (Char.code first_char) - (Char.code '0') in
                    match found_first_digit with
                    | true -> process_line_helper remaining_line first_digit digit found_first_digit
                    | false -> process_line_helper remaining_line digit digit true
                )
            )
        in
        process_line_helper line 0 0 false
    in
    let rec process_all_lines (input: string list): int =
        match input with
        | [] -> 0
        | line::tail -> (process_line line) + process_all_lines tail
    in
    process_all_lines input
in
let answer: int = main () in
Printf.printf "answer = %d\n" answer;

(* 53080 *)
