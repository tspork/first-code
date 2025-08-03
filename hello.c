// HOWTO:
//
// C program files are named SOMETHING.c.
// A "compiler" named "cc" compiles SOMETHING.c into SOMETHING.exe.
//
// Compile to create program ./hello.exe:
// $ cc hello.c -o ./hello.exe
//
// Run w/ 0 arguments:
// $ ./hello.exe
//
// Run w/ 1 argument:
// $ ./hello.exe Tau

#include <stdio.h>

int main(int number_of_words, char** words) {
  if ( number_of_words == 2 ) {      // why 2?
    printf("Hello, %s!\n", words[1]);
  } else {
    printf("Hello, %s!\n", "STRANGER");
  }
  return 0;}
